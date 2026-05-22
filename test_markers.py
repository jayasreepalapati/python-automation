import pytest

@pytest.mark.smoke
def test_login():
    assert "admin" == "admin"
    
@pytest.mark.smoke
def test_homepage():
    assert "home" in "homepage"

@pytest.mark.regression
def test_search():
    assert "python" in "python automation"

@pytest.mark.regression
def test_logout():
    assert "logout"=="logout"

@pytest.mark.slow
def test_report():
    assert 2+2 == 4
    
