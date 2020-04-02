from requests import get

print(get("http://127.0.0.1:5000/api/jobs").json())  # корректный запрос на получение всех работ
print(get("http://127.0.0.1:5000/api/jobs/1").json())  # корректный запрос на получение 1 работы
print(get("http://127.0.0.1:5000/api/jobs/1000").json())  # некорректный запрос на получение 1 работы (нет такого id)
print(get("http://127.0.0.1:5000/api/jobs/lol").json())  # некорректный запрос на получение 1 работы (str, а не int)
