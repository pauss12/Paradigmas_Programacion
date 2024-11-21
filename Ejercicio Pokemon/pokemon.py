import tkinter as tk
from PIL import Image, ImageTk
import threading
import requests


class PokemonUI:

    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry('400x400')
        self.window.title('Pokemon API')

        self.label = tk.Label(self.window, text='Nombre del Pokemon:')
        self.label.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.button = tk.Button(self.window, text='Buscar Pokemon', command=self.search_pokemon)
        self.button.pack()

        self.text = tk.Label(self.window)
        self.text.pack()

        # Imagen del Pokemon
        self.image_label = tk.Label(self.window)
        self.image_label.pack()

        self.window.mainloop()

    def search_pokemon(self):

        pokemon_name = self.entry.get().strip()

        if not pokemon_name:
            print("Error: Debe ingresar un nombre de Pokemon.")
            return

        thread1 = threading.Thread(target=self.peticion_api, args=(pokemon_name,))
        thread1.start()

    def peticion_api(self, pokemon_name):
            
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
           
            response = requests.get(url)
    
            if response.status_code == 200:
                pokemon = response.json()
                pokemon_data = {
                    'name': pokemon['name'],
                    'type': pokemon['types'][0]['type']['name'],
                    'height': pokemon['height'],
                    'weight': pokemon['weight'],
                    'image': pokemon['sprites']['front_default']
                }
                self.update_ui_text(pokemon_data)
            else:
                print("Error: Pokemon no encontrado.")

    def update_ui_text(self, pokemon):

        self.text = tk.Label(self.window, text=f"Nombre: {pokemon['name']}\nTipo: {pokemon['type']}\nAltura: {pokemon['height']}\nPeso: {pokemon['weight']}")
        self.text.pack()

        self.show_image(pokemon['image'])


    def show_image(self, url):
        
        img = Image.open(requests.get(url, stream = True).raw)
        img = img.resize((150, 150), Image.Resampling.NEAREST) 
      
        #quiero mostrar la imagen en la ventana, en el label correspondiente
        photo = ImageTk.PhotoImage(img)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
       

def main():
    pokemon_ui = PokemonUI()
    pokemon_ui.window.mainloop()

main()