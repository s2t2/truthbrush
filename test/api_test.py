from truthbrush.api import (
    Api,
    TRUTHSOCIAL_USERNAME,
    TRUTHSOCIAL_PASSWORD,
    TRUTHSOCIAL_TOKEN,
)


def test_client_initialization(client):
    assert isinstance(client, Api)
    assert client._username == TRUTHSOCIAL_USERNAME
    assert client._password == TRUTHSOCIAL_PASSWORD
    assert client.auth_id == TRUTHSOCIAL_TOKEN


def test_client_check_login(client):
    assert client.auth_id == None

    client._check_login()

    # obtains and sets the auth token:
    assert isinstance(client.auth_id, str)


def test_client_get_auth_id(client):
    # a lower level method for obtaining an auth token:
    auth_id = client.get_auth_id(client._username, client._password)
    assert isinstance(auth_id, str)
