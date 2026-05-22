user ={"name":"jayasree","country":"india","age":47}
print(user["name"])
print(user["country"])
print(user["age"])

user["age"]=25
print(user["age"])

user["city"]="sandiego"
print(user)
del (user["country"])
print(user)
print("country" in user)
print("language" in user)
print(user.keys())
print(user.values())