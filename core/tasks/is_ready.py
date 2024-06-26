import logging
import socket
import requests
from core.config import litellm_url, vector_db_url
from .celery_app import app
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

def check_service_health(url):
    try:
        response = requests.get(url, timeout=5)  # 5 seconds timeout
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        logging.info(f"Health check passed for {url}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Health check failed for {url}: {e}")
        return False

def is_ready():
    services = [f"{litellm_url}/health/readiness", f"{vector_db_url}/ping"]  # Add more services here
    all_services_ok = True

    for service in services:
        if not check_service_health(service):
            all_services_ok = False
    # Add a delay here
    logging.info("Waiting for Celery worker to start...")
    time.sleep(10)  # Wait for 10 seconds

    try:
        pong = app.control.ping([f'celery@{socket.gethostname()}'])
        logging.info(f"Ping response: {pong} for celery@{socket.gethostname()}")
        if len(pong) == 0 or list(pong[0].values())[0].get('ok', None) is None:
            logging.error(f"Ping failed: {pong}")
            all_services_ok = False
        else:
            logging.info("Celery worker ping successful")
    except Exception as e:
        logging.error(f"Error pinging Celery worker: {e}")
        all_services_ok = False

    if all_services_ok:
        logging.info("All services are ready")
    else:
        logging.error("One or more services are not ready")

if __name__ == "__main__":
    is_ready()