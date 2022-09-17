import asyncio
import logging

import httpx
import uvicorn
from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator

import config
import exceptions
import logger_setup

logger_setup.init_logging()
logger = logging.getLogger('main')

# Starting an app
app = FastAPI(
    title='BloomreachExponeaApi',
    docs_url='/',
    on_shutdown=[lambda: logger.info('Server shutting down.')]
)


# Prometheus middleware
@app.on_event("startup")
async def startup_event():
    logger.info('Server starting up.')
    logger.info('Prometheus Instrumentator initializing')
    Instrumentator().instrument(app).expose(app)


# Async client that performs all calls
async_client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_keepalive_connections=int(config.MAX_KEEP_ALIVE_CONNECTIONS),
        max_connections=int(config.MAX_CONNECTIONS)
    )
)


def get_result_from_task(task: asyncio.Future) -> dict | None:
    result = task.result()
    return result


def find_first_completed(tasks: [asyncio.Future]) -> dict | None:
    for task in tasks:
        result = get_result_from_task(task)
        if result is not None:
            return result
    return None


async def fetch_exponea_api(timeout: float) -> dict | None:
    """
    Performs an Async operation and awaits for selected timeout
    :param timeout: timeout for request
    :return: JSON if request was successful
    """
    try:
        response = await async_client.get(config.EXPONEA_URL, timeout=timeout)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise exceptions.UpstreamServerException("Incorrect status code from ExponeaAPI.")
    except exceptions.UpstreamServerException as e:
        logger.debug(e)
        return None
    except httpx.ReadTimeout as e:
        logger.debug(f'Timed out from user-timeout. {e}')
        return None
    except httpx.PoolTimeout as e:
        logger.debug(f'Timed out waiting to acquire a connection from the pool. {e}')
        return None
    except httpx.ConnectTimeout as e:
        logger.debug(f'Timed out while connecting to the host. {e}')
        return None


async def perform_request_chain(timeout: float) -> dict | None:
    """
    Sends first request to exponea, and if it was unsuccessful,prepares another two.
    Returns either first completed request, or None if all the requests failed due to timeout or exponea api issues.
    :param timeout: should be lower than real timeout to account for small deviations
    :return: JSON or None if all requests failed
    """
    task_time = 0.0

    # Creating async task to fetch for
    first_fetch = [asyncio.create_task(fetch_exponea_api(float(config.FIRST_REQUEST_TIMEOUT)), name=f'Try_0')]
    first_finished, first_unfinished = await asyncio.wait(
        first_fetch, timeout=float(config.FIRST_REQUEST_TIMEOUT),
        return_when=asyncio.FIRST_COMPLETED
    )

    if len(first_finished) != 0:
        task = first_finished.pop()
        result = get_result_from_task(task)
        logger.debug(f'{result=}')
        if result is not None:
            return result
    else:
        task_time += float(config.FIRST_REQUEST_TIMEOUT)

    logger.debug(f'First request didnt finish in time. Starting 2 other. Timeout for them: {timeout - task_time}')

    tasks = [asyncio.create_task(fetch_exponea_api(timeout - task_time), name=f'Additional_{x}') for x in range(2)]
    second_finished, second_unfinished = await asyncio.wait(
        tasks + list(first_unfinished),
        timeout=timeout - task_time,
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in tasks + list(first_unfinished):
        logger.debug(f'Task {task.get_name()}. Status: {task.done()}.')
        task.cancel()

    result = find_first_completed(second_finished)
    return result


def recalculate_timeout(user_timeout: int) -> float:
    """
    Transforms client-set timeout into true timeout, to account for 'hidden' time loss
    Percentage must be set in config file
    :param user_timeout: Timeout in milliseconds as requested by client
    :return: Timeout in seconds
    """
    return round((user_timeout / 1000) * float(config.TIMEOUT_SAFETY_PERCENT), 5)


@app.get("/api/smart", status_code=200)
async def fetch_exponea_smart(response: Response, timeout: int = int(config.DEFAULT_REQUEST_TIMEOUT)) -> dict:
    """
    Endpoint for fetching exponea api
    :param response: Passed automatically, part of fastAPI
    :param timeout: timeout in ms, default value set in settings
    :return: JSON with either a message, or time value received from fetching exponea
    """
    logger.debug(f'Received request on /api/smart, {timeout=}')
    if timeout < int(config.MINIMAL_SAFE_TIMEOUT):
        response.status_code = status.HTTP_400_BAD_REQUEST
        response = {'message': 'Timeout cannot be set lower then 300ms. '}
        return response

    recalculated_timeout = recalculate_timeout(timeout)
    result = await perform_request_chain(recalculated_timeout)

    if result is None:
        logger.debug('All results are None or timed out')
        response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
        response = {'message': 'Failed to fetch requests in given timeout, or all of them were unsuccessful.'}
        return response
    else:
        return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(config.PORT))
