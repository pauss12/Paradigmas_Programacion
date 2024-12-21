from rx import create, operators
from requests import get
from rx.core import Observer
from rx.subject import Subject
from tkinter import Tk, Label, Button, Entry, Listbox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk, UnidentifiedImageError
import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO

class App:

    #  INIT METHOD THAT CREATES THE WINDOW  ---------------------------------------------------------------------------------------
    def __init__(self):

        self.image_subject = Subject() 
        
        self.image_subject.subscribe( 
            on_next=self.on_image_downloaded, 
            on_error=self.on_error, 
            on_completed=self.on_completed 
        ) 
        
        self.n_photos = 0 
        self.images = []

        self.create_window()

    #  METHOD THAT CREATES THE WINDOW  ----------------------------------------------------
    def create_window(self):
        
        self.window = Tk()

        self.window.geometry('500x600')

        self.window.resizable(False, False)

        self.label = Label(text='URL a procesar', font=('Arial', 11))
        self.label.grid(column=0, row=0, pady=10, padx=(20, 0), sticky='w')

        self.entry = Entry(width=30)
        self.entry.grid(column=1, row=0, pady=10, padx=(40, 0), sticky='w')

        self.Button = Button(text='Buscar', width=30, height=1, background='light grey', fg='black', command=self.search_url)
        self.Button.grid(column=1, row=1, pady=10, padx=(10, 20), sticky='w')

        self.options = Listbox(width=30, height=20, background='light grey', fg='black')
        self.options.grid(column=0, row=2, columnspan=1, pady=10, padx=20, sticky='w')
        self.options.bind('<<ListboxSelect>>', self.on_image_selected)

        self.image = Label(background='light grey', width=30, height=20)
        self.image.grid(column=1, row=2, pady=10, padx=(10, 20), sticky='w')

        self.barra_progresadora = Progressbar(orient="horizontal", length=150, mode="determinate")
        self.barra_progresadora.grid(column=1, row=3, columnspan=2, pady=10, padx=(30, 0), sticky='w')

        #texto que diga el numero de imagenes con su valor que depende de la busqueda de la url
        self.text = Label(text=f'Numero de imagenes: {self.n_photos}', font=('Arial', 11))
        self.text.grid(column=1, row=4, pady=10, padx=(20, 0), sticky='w')

        self.window.mainloop()

    # METHOD SUBSCRIBED -------------------------------------------------------------------
    def on_error(self, error):
        print(f'Error: {error}')

    def on_completed(self):
        print("All the Images have been downloaded")

    def on_image_downloaded(self, image):
        img_url, img_data, img_alt = image
        self.images.append((img_url, img_data, img_alt))
        self.options.insert('end', img_alt)

    # METHOD THAT DISPLAYS THE SELECTED IMAGE  ----------------------------------------------
    def on_image_selected(self, event):

        w = event.widget 
        index = int(w.curselection()[0])

        img_data = self.images[index]
        img_url = img_data[0]
        
        try: 
            image = Image.open(BytesIO(img_data)) 
            image = image.resize((label_width, label_height), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image) 
            self.image.config(image=photo) 
            self.image.image = photo 

        except UnidentifiedImageError: 
            print(f'Error: La imagen en la URL {img_url} no se pudo identificar.')



    #  METHOD THAT SEARCHES THE URL  -------------------------------------------------------
    def search_url(self):

        url = self.entry.get().strip()

        if not url:
            self.on_error('Error: Debe ingresar una URL.')
        
        asyncio.run(self.get_images(url))

    #  METHOD THAT GETS THE IMAGES  ---------------------------------------------------------
    async def get_images(self, url):
        
        try:
            
            async with aiohttp.ClientSession() as session: 
                async with session.get(url) as response: 
                    html = await response.text() 
                    soup = BeautifulSoup(html, 'html.parser') 
                    img_tags = soup.find_all('img') 
                    image_urls = [urljoin(url, img['src']) for img in img_tags if 'src' in img.attrs]
                    image_alts = [img.get('alt', 'N/A') for img in img_tags]
                    
                    if not image_urls: 
                        self.on_error('Error: No se encontraron imágenes.') 
                        return 
                    
                    self.n_photos = len(image_urls) 
                    self.barra_progresadora["maximum"] = self.n_photos 
                    
                    tasks = [self.download_image(session, img_url) for img_url in image_urls] 
                    self.images = await asyncio.gather(*tasks) 
                    
                    progress = 0
                    i = 0
                    for img_data, img_url, img_alt in zip(self.images, image_urls, image_alts):
                        i = image_urls.index(img_url) + 1 
                        self.text['text'] = f'Numero de imagenes: {i}'
                        time.sleep(0.1)
                        if img_data: 
                            self.image_subject.on_next((img_url, img_data, img_alt)) 
                            progress += 1 
                            self.update_progress(progress) 

                    self.image_subject.on_completed()
        
        except Exception as e:
            self.on_error(f'Error: {e}')

    #  METHOD THAT DOWNLOADS THE IMAGES  ---------------------------------------------------
    async def download_image(self, session, url):
        try:
            async with session.get(url) as response:
                image_data = await response.read()
                return image_data
        except Exception as e:
            self.on_error(f'{e}')
            return None

    #  METHOD THAT MAKES UPDATES THE PROGRESS BAR  -----------------------------------------
    def update_progress(self, progress):
        self.barra_progresadora['value'] = progress
        self.barra_progresadora.update()

App()
