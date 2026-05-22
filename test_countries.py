import requests
import pytest

base_url= "https://restcountries.com/v3.1"

def test_india_capital():
    response=requests.get(f"{base_url}/name/india")
    assert response.status_code==200
    data=response.json()
    assert data[0]["capital"][0]=="New Delhi"
    print("india capital test passed")

def test_usa_currency():
    response=requests.get(f"{base_url}/name/usa")
    assert response.status_code==200
    data=response.json()
    assert list(data[0]["currencies"].keys())[0]=="USD"
    print("USA currency test is passed")

def test_invalid_country():
    response=requests.get(f"{base_url}/name/invalidcountry")
    assert response.status_code==404
    print("invalid country test is passed")