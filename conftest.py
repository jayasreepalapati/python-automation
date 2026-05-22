import pytest
@pytest.fixture
def user():
    return{
    "username":"admin",
    "password":"admin@123",
    "role":"admin"
    }
    
@pytest.fixture
def test_urls():
    return["https://demo.com/login",
        "https://demo.com/dashboard",
        "https://demo.com/logout"]
    

@pytest.fixture
def status_codes():
     return[200,505,400,200,200]   