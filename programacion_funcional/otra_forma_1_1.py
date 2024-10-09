from requests import get
import json
from functools import partial # Partial nos permite crear una función parcial, una que ya tiene ciertos parámetros asignados

api_key = "f8c0e272"

def make_get_request(url, onsuccess, onerror):
    response = get(url)
    if response.status_code == 200:
        onsuccess(response.content)
    else:
        onerror()
    return 

def print_data(data):
    print(data)

def get_title(data):
    y = json.loads(data)
    print(y["Title"])

def print_error():
    print("Error")

def get_poster(data):
    y = json.loads(data)
    make_get_request(y["Poster"], partial(save_image, y["Title"]), print_error)

def save_image(title, data):
    with open(f"{title}.jpg", "wb") as file:
        file.write(data)

def build_url(movie_title):
    return f"https://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

def main():
    movie_title = input("Introduce el título de la película: ")
    url = build_url(movie_title)
    data = make_get_request(url, get_poster, print_error)
    
main()