from tkinter import Tk, Label, Button, Entry, Listbox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk, UnidentifiedImageError
import threading
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO

class App:

    def __init__(self):
        self.n_photos = 0
        self.images = []
        self.create_window()

    def create_window(self):
        self.window = Tk()
        self.window.resizable(False, False)

        self.label = Label(text='URL a procesar', font=('Arial', 11))
        self.label.grid(column=0, row=0, pady=10, padx=(20, 0), sticky='w')

        self.entry = Entry(width=30)
        self.entry.grid(column=1, row=0, pady=10, padx=(40, 0), sticky='w')

        self.Button = Button(text='Buscar', width=30, height=1, background='light grey', fg='black', command=self.search_url)
        self.Button.grid(column=1, row=1, pady=10, padx=(10, 20), sticky='w')

        self.options = Listbox(width=30, height=20, background='light grey', fg='black')
        self.options.grid(column=0, row=2, columnspan=1, pady=10, padx=20, sticky='ns')
        self.options.bind('<<ListboxSelect>>', self.on_image_selected)

        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

        self.image = Label(background='light grey', width=30, height=20)
        self.image.grid(column=1, row=2, pady=10, padx=(10, 20), sticky='nsew')

        self.barra_progresadora = Progressbar(orient="horizontal", length=150, mode="determinate")
        self.barra_progresadora.grid(column=1, row=3, columnspan=2, pady=10, padx=(30, 0), sticky='w')

        self.text = Label(text=f'Numero de imagenes: {self.n_photos}', font=('Arial', 11))
        self.text.grid(column=1, row=4, pady=10, padx=(20, 0), sticky='w')
        
        self.total_images = Label(text=f'Se encontraron {self.n_photos} imágenes: ', font=('Arial', 11))
        self.total_images.grid(column=1, row=5, pady=10, padx=(20, 0), sticky='w')

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window.mainloop()

    def on_error(self, error):
        print(f'Error: {error}')

    def on_completed(self):
        print("All the Images have been downloaded")

    def on_image_downloaded(self, image, subject):
        img_url, img_data, img_alt = image
        self.images.append((img_url, img_data, img_alt))
        self.options.insert('end', img_alt)

    def search_url(self):
        url = self.entry.get().strip()

        if not url:
            self.on_error('Error: Debe ingresar una URL.')
            return

        # Reset the UI and images before starting a new search
        self.images = []
        self.options.delete(0, 'end')
        self.n_photos = 0
        self.barra_progresadora['value'] = 0
        self.text['text'] = f'Numero de imagenes: {self.n_photos}'
        self.image.configure(image=None)
        self.image.image = None

        # Start image fetching in a separate thread
        threading.Thread(target=self.get_images, args=(url,)).start()

    def on_image_selected(self, event):
        selection = self.options.curselection()
        
        if not selection:
            return

        index = int(selection[0])
        img_url, img_data, img_alt = self.images[index]
        
        try:
            image = Image.open(BytesIO(img_data))

            resized_image = self.resize_image(image)

            photo = ImageTk.PhotoImage(resized_image)
            self.image.configure(image=photo)
            self.image.image = photo

        except UnidentifiedImageError:
            print(f'Error: La imagen en la URL {img_url} no se pudo identificar.')

    def resize_image(self, image):
        label_width = self.image.winfo_width()
        label_height = self.image.winfo_height()
        
        img_ratio = image.width / image.height
        label_ratio = label_width / label_height
        
        if img_ratio > label_ratio:
            new_width = label_width
            new_height = int(label_width / img_ratio)
        else:
            new_height = label_height
            new_width = int(label_height * img_ratio)
        
        return image.resize((new_width, new_height), Image.LANCZOS)

    def get_images(self, url):
        print('entra a get_images')

        try:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            img_tags = soup.find_all('img')
            image_urls = [urljoin(url, img['src']) for img in img_tags if 'src' in img.attrs]
            image_alts = [img.get('alt', 'N/A') for img in img_tags]

            if not image_urls:
                self.on_error('Error: No se encontraron imágenes.')
                return

            self.n_photos = len(image_urls)
            self.barra_progresadora["maximum"] = self.n_photos

            progress = 0
            for img_url, img_alt in zip(image_urls, image_alts):
                img_data = self.download_image(img_url)
                if img_data:
                    self.on_image_downloaded((img_url, img_data, img_alt), None)
                    progress += 1
                    self.update_progress(progress)
                self.text['text'] = f'Numero de imagenes: {self.n_photos}'
                time.sleep(0.1)

            self.total_images['text'] = f'Se encontraron {self.n_photos} imágenes '

        except Exception as e:
            self.on_error(f'Error: {e}')

    def download_image(self, url):
        try:
            response = requests.get(url)
            return response.content
        except Exception as e:
            self.on_error(f'{e}')
            return None

    def update_progress(self, progress):
        self.barra_progresadora['value'] = progress
        self.barra_progresadora.update()

    def on_close(self):
        self.window.quit()

App()
