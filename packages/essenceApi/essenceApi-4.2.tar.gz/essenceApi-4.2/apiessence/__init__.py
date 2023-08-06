import requests

def say_hello():
    print("привет")

url = 'http://81.200.147.83:5000/api'

def get_remove_wl(server_id, user_id):
    data = f"get_remove_wl {server_id} {user_id}"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()['result']
        print(f"[API]: {result}")
    else:
        print('Ошибка при выполнении запроса:', response.status_code)
