import socket

import requests

from core.config import litellm_url, vector_db_url

def is_ready():
    # response = requests.get(f"{litellm_url}/health", headers={
    #     "Authorization": f"Bearer {os.getenv('LITELLM_MASTER_KEY', '')}"
    # })
    # if not response.ok:
    #     raise Exception(response.text)

    # print(response)

    response = requests.get(f"{litellm_url}/health/readiness")
    if not response.ok:
        raise Exception(response.text)

    print(response)

    response = requests.get(f"{vector_db_url}/healthz")
    if not response.ok:
        raise Exception(response.text)

    print(response)


if __name__ == "__main__":
    is_ready()
