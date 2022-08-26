from .database import client, session
from app import schema

def test_root(client):
	res = client.get("/")
	assert res.json().get("message") == "HelloWorld"
	assert res.status_code == 200


def test_create_user(client):
	res = client.post("/users/", json={"email": "sartaj@gmail.com", "password": "123456"})
	print(res.json())
	new_user = schema.UserOut(**res.json())
	assert new_user.email == "sartaj@gmail.com"
	assert res.status_code == 201

def test_login_user(client):
	res = client.post("/login", data={"username": "sartaj@gmail.com", "password": "123456"})
	print(res.json())
	assert res.status_code == 200