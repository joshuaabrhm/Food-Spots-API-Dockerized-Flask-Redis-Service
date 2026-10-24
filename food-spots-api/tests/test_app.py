import fakeredis
import pytest

import app as app_module


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        app_module, "r", fakeredis.FakeStrictRedis(decode_responses=True)
    )
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_home_counts_visits(client):
    assert client.get("/").get_json()["visits"] == 1
    assert client.get("/").get_json()["visits"] == 2


def test_add_and_list_spots(client):
    res = client.post("/spots", json={"name": "CTR", "area": "Malleshwaram"})
    assert res.status_code == 201
    spots = client.get("/spots").get_json()
    assert spots == [{"name": "CTR", "area": "Malleshwaram"}]


def test_add_spot_validation(client):
    res = client.post("/spots", json={"name": "CTR"})
    assert res.status_code == 400


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}
