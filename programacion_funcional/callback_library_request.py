from requests import get

def get_movie_data(title, apikey, on_success, on_error):

    
    url = f"http://www.omdbapi.com/?t={title}&apikey={apikey}"
    response = get(url)
    
    if response.status_code == 200:
        on_success(response.json())
    else:
        on_error(response.text)

get_movie_data("The Matrix", "b7da8d8e", lambda data: print(data), lambda error: print(error))

get_movie_data("Interstellar", "fbd46cff", lambda data: print(data), lambda error: print(error))