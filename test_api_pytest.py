import requests
import pytest

BASE_URL= "https://jsonplaceholder.typicode.com"

def test_get_post():
    response=requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code==200
    data=response.json()
    assert data["id"]==1
    assert data["userId"]==1
    assert "title" in data
    print("get test passed")

def test_create_post():
    new_post={"title":"create post","userId":1,"body":"test body"}
    response=requests.post(f"{BASE_URL}/posts",json=new_post)
    assert response.status_code ==201
    data=response.json()
    assert data["title"]=="create post"
    assert "id" in data
    print("creating a post is successful")

def test_update_post():
    updated={"title":"updated post","userId":1,"body":"updated body"}
    response=requests.put(f"{BASE_URL}/posts/1",json=updated)
    assert response.status_code ==200
    data=response.json()
    assert data["title"]=="updated post"
    print("updating a post is successful")
    
def test_delete_post():
    response=requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code==200
    print("deleting a post is successfull")

          
    