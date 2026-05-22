import pytest

@pytest.mark.parametrize("username,password,expected",[("admin","admin@123","welcome"),
                                                       ("user1","user1@123","welcome"),
                                                       ("user2","user2@123","welcome"),
                                                       ("wrong","wrongpwd","error"),
                                                       ])

def test_login(username,password,expected):
    if username =="wrong":
        actual = "error"
    else:
        actual = "welcome"
    assert actual == expected 
    
    