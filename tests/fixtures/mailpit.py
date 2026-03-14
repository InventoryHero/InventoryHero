import time

import pytest

from tests.utils.email import clear_messages


@pytest.fixture(autouse=True, scope="function")
def clean_mailpit():
    clear_messages()
    yield


