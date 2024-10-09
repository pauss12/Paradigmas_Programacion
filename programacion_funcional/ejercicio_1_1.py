#Hay que hacer una peticion para buscar la pelicula, y de ahi hace una peticion a buscar el poster de esa misma pelicula y vamos a guardarla en nuestro ordenador

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

def print_error():
    print("Ha ocurrido un error. CUIDADO!!")

def build_url(movie_title):
    return f"https://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

def get_poster(data):
    y = json.loads(data)
    url = y["Poster"]
    response = get(url)
    if response.status_code == 200:
        with open("programacion_funcional/poster.jpg", "wb") as file    :
            file.write(response.content)
    else:
        print_error()

def main():
    movie_title = input("Introduce el título de la película: ")
    url = build_url(movie_title)
    data = make_get_request(url, get_poster, print_error)
    
main()