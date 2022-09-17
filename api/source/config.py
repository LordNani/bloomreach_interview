import logging
import os

PORT = os.getenv('PORT', 8000)

# URL to fetch in every request
EXPONEA_URL = os.getenv('UPSTREAM_URL', 'https://exponea-engineering-assignment.appspot.com/api/work')

# Time in seconds to wait for first request to finish before firing extra two
FIRST_REQUEST_TIMEOUT = os.getenv('FIRST_REQUEST_TIMEOUT', 0.3)

DEFAULT_REQUEST_TIMEOUT = os.getenv('DEFAULT_REQUEST_TIMEOUT', 1000)

# Coefficient to multiply user-set timeout by, mostly for ensuring that response time on client side is met
TIMEOUT_SAFETY_PERCENT = os.getenv('TIMEOUT_SAFETY_PERCENT', 0.95)

MINIMAL_SAFE_TIMEOUT = os.getenv('MINIMAL_SAFE_TIMEOUT', 300)

# Setting loglevel for a project
LOGLEVEL = logging.DEBUG

# Limits for AsyncClient
MAX_CONNECTIONS = os.getenv("MAX_CONN", 200)
MAX_KEEP_ALIVE_CONNECTIONS = os.getenv("MAX_KEEP_ALIVE", 1)
