import pytest

@pytest.fixture
def user():
    return {
    "username":"admin",
    "password":"admin@123",
    "role":"admin"
    }

@pytest.fixture
def test_urls():
    return [
        "https://demo.com/login",
        "https://demo.com/dashboard",
        "https://demo.com/logout"
    
    ]
def test_username(user):
    assert user["username"]=="admin"
def test_password_len(user):
    assert len(user["password"])>=8
def test_user_rol1(user):
    assert user["role"]=="admin"
def test_url_count(test_urls):
    assert len(test_urls)==3
def test_lohin_url(test_urls):
    assert "login" in test_urls[0]
    
    