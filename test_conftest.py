def test_username(user):
    assert user["username"] == "admin"

def test_url_count(test_urls):
    assert len(test_urls) == 3

def test_status_codes(status_codes):
    assert 200 in status_codes
    assert len(status_codes) == 5