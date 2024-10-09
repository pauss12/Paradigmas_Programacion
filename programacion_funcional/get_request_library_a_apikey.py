from secret import api_key
from requests import get
import json

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

def build_url(movie_title):
    return f"https://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

def main():
    movie_title = input("Introduce el título de la película: ")
    url = build_url(movie_title)
    data = make_get_request(url, get_title, print_error)
    
main()