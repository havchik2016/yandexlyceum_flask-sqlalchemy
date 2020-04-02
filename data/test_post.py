from requests import post, get
from datetime import datetime

print(get("http://127.0.0.1:5000/api/jobs").json())  # работы до запросов
print(post("http://127.0.0.1:5000/api/jobs").json())  # некорректный запрос (нет аргументов)
print(post("http://127.0.0.1:5000/api/jobs", json={
    "collaborators": "1",
    "end_date": "2020-04-02 15:30:04",
    "id": 1,
    "is_finished": False,
    "job": "lol",
    "start_date": "2020-04-02 15:30:03",
    "team_leader": 1,
    "work_size": 30
}).json())  # некорректный запрос (такой id уже есть)
print(post("http://127.0.0.1:5000/api/jobs", json={
    "id": 3
}).json())  # некорректный запрос (недостаточно аргументов
print(post("http://127.0.0.1:5000/api/jobs", json={
    "collaborators": "2",
    "end_date": "2020-04-02 16:05:54.545801",
    "id": 2,
    "is_finished": False,
    "work_size": 30,
    "start_date": "2020-04-02 16:05:45.982085",
    "team_leader": 1,
    "job": "EndLyceum"
}).json())  # корректный запрос
print(get("http://127.0.0.1:5000/api/jobs").json())  # работ стало на 1 больше
