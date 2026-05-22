def test_valid_login():
    username = "admin"
    password= "admin123"
    expected = "welcome"
    actual = "welcome"
    assert actual == expected
    
def test_invalid_login():
    usernmae = "admin"
    password = "wrongpassword"
    expected = "error"
    actual ="error"
    assert actual== expected

def test_add():
    result=2+3
    assert result == 5

def test_string_upper():
    text = "hello"
    assert text.upper()=="HELLO"
    
def test_list_len():
    test_cases=["login test","pwdtest","searchtest"]
    assert len(test_cases)==3

def test_login_status():
    status="pass"
    assert status == "pass"

def test_url_contains():
    url="https://demo.com/login"
    assert "login" in url

    