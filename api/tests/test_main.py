import logging

from fastapi.testclient import TestClient

from api.source.main import app

client = TestClient(app)
logging.basicConfig(
    filename='tests.log',
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


def test_openapi_present():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    logger.info(f'Test: test_openapi_present. Success.')
