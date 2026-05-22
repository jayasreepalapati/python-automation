import requests

#get a post from jsonplaceholder
response=requests.get("https://jsonplaceholder.typicode.com/posts/1")

#put a post on json
new_post={
    "title": "new post",
    "body": "this is my new post",
    "user-id":1
}
response =requests.post("https://jsonplaceholder.typicode.com/posts",json=new_post)
print("post",response.status_code)
print("created",response.json())

#uodate a post

update_post = {
    "title": "updated post",
    "body": "this is my updated post",
    "user-id":1
}
response =requests.put("https://jsonplaceholder.typicode.com/posts/1",json=update_post)
print("updated",response.status_code)
print("updated post",response.json())


#delete apost
response=requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print("delete",response.status_code)