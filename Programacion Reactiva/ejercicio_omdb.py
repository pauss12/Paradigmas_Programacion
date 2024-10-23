from rx import create, operators
from requests import get

#Construiremos una pequeña app de películas utilizando la API de OMFb

# http://www.omdbapi.com/

# Accedemos a su web y nos registramos para obtener una API KEY, necesario para poder utilizar esta API

# Desde Pyhton, lanzaremos una petición de búsqueda para buscar las películas que encajen con título

# Procesaremos el JSON de respuesta mediante un Observable y operaciones: 
# Eliminaremos todos los resultados que no tengan type == 'movie'
# Generaremos el mensaje:(ID) - TITULO : URL_POSTER (AÑO)

api_key = "fbd46cff"

import requests

# Función para buscar películas en la API de OMDB
def buscar_peliculas(api_key, titulo):
    url = f"http://www.omdbapi.com/?apikey={api_key}&s={titulo}"
    
    # Realizar la petición GET a la API
    respuesta = requests.get(url)
    
    # Comprobar si la petición fue exitosa
    if respuesta.status_code != 200:
        print(f"Error en la petición: {respuesta.status_code}")
        return []
    
    # Procesar el JSON de la respuesta
    datos = respuesta.json()

    # Si la respuesta tiene un error (como "Movie not found!")
    if 'Error' in datos:
        print(f"Error en la búsqueda: {datos['Error']}")
        return []
    
    # Filtrar resultados para quedarnos solo con los que tengan type == 'movie'
    resultados = [pelicula for pelicula in datos.get('Search', []) if pelicula['Type'] == 'movie']

    return resultados

# Función para generar el mensaje de salida con el formato solicitado
def generar_mensaje(peliculas):
    mensajes = []
    
    for pelicula in peliculas:
        mensaje = f"({pelicula['imdbID']}) - {pelicula['Title']} : {pelicula['Poster']} ({pelicula['Year']})"
        mensajes.append(mensaje)
    
    return mensajes

# Función principal que combina todo el proceso
def main():
    # Sustituye con tu propia API KEY
    api_key = "TU_API_KEY"
    
    # Título a buscar
    titulo = input("Introduce el título de la película a buscar: ")
    
    # Buscar películas
    peliculas = buscar_peliculas(api_key, titulo)
    
    if peliculas:
        # Generar mensajes con el formato solicitado
        mensajes = generar_mensaje(peliculas)
        
        # Mostrar los mensajes generados
        for mensaje in mensajes:
            print(mensaje)
    else:
        print("No se encontraron películas.")

if __name__ == "__main__":
    main()



