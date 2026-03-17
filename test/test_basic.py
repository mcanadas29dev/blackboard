import pytest
import os
import tempfile
from app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    app = create_app("development")
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "USERS_DB_PATH": db_path,
        "PIZARRA_DB_PATH": db_path,
    })
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_page_loads(client):
    res = client.get("/auth/login")
    assert res.status_code == 200


def test_index_requires_login(client):
    res = client.get("/", follow_redirects=False)
    assert res.status_code == 302
    assert "/auth/login" in res.headers["Location"]
