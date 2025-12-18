import time

import requests
from bs4 import BeautifulSoup

MAILPIT_API = "http://localhost:8025/api/v1"


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

def parse_email_messages(email: str, needle: str):
    messages = wait_for_messages()
    assert messages["total"] == 1
    msg = messages["messages"][0]
    assert msg["To"][0]["Address"] == email
    body = get_message(msg["ID"])
    assert needle in body["HTML"]

    soup = BeautifulSoup(body["HTML"], "html.parser")
    reset_links = [
        link for link in [a["href"] for a in soup.find_all("a", href=True)]
        if needle in link
    ]
    assert len(reset_links) == 2
    assert reset_links[0] == reset_links[1]
    return reset_links[0].split("/")[-1]

def clear_messages():
    requests.delete(f"{MAILPIT_API}/messages")