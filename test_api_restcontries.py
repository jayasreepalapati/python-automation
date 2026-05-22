import requests
response=requests.get("https://restcountries.com/v3.1/name/usa")
data=response.json()

print("country",data[0]["name"]["common"])
print("capital",data[0]["capital"][0])
print("population",data[0]["population"])
print("currency",list(data[0]["currencies"].keys())[0])

