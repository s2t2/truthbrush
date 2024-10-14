import pytest

from truthbrush.api import Api


@pytest.fixture(scope="module")
def client():
    return Api()


@pytest.fixture(scope="module")
def user_timeline(client):
    result = client.pull_statuses(username="truthsocial", replies=False, verbose=True)
    return list(result)
