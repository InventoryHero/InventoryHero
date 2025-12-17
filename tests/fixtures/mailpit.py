import time

import pytest
import requests

MAILPIT_API = "http://localhost:8025/api/v1"

@pytest.fixture(autouse=True, scope="function")
def clean_mailpit():
    requests.delete(f"{MAILPIT_API}/messages")
    yield


def wait_for_messages(timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{MAILPIT_API}/messages")
        r.raise_for_status()
        data = r.json()
        if data["total"] > 0:
            return data
        time.sleep(0.2)
    raise AssertionError("Expected email, but none was received")


def get_message(message_id):
    r = requests.get(f"{MAILPIT_API}/message/{message_id}")
    r.raise_for_status()
    return r.json()
