from requests import get, post, delete

print(get("http://127.0.0.1:5000/api/v2/users").json())
print(delete("http://127.0.0.1:5000/api/v2/users/1").json())