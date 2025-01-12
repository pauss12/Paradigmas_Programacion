import asyncio
import aiohttp
from urllib.parse import urljoin
from tkinter import Tk, StringVar, Listbox, Button, Label, ttk
from PIL import Image, ImageTk
import io
from rx.subject import Subject
from bs4 import BeautifulSoup


def user_fotos():
    root = Tk()
    root.title("Imagenes de URLs")

    url_var = StringVar()

    Label(root, text="URL:").grid(row=0, column=0, padx=5, pady=5)

    entrada_url = ttk.Entry(root, textvariable=url_var, width=50)
    entrada_url.grid(row=0, column=1, padx=5, pady=5)

    buscar = Button(root, text="Buscar")
    buscar.grid(row=0, column=2, padx=5, pady=5)

    lista_imgs = Listbox(root, height=15, width=50)
    lista_imgs.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    barraProgreso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    barraProgreso.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    estado = Label(root, text="")
    estado.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    imagen = Label(root)
    imagen.grid(row=1, column=2, rowspan=3, padx=5, pady=5)

    totalImgs = Label(root, text="Se encontraron 0 imágenes")
    totalImgs.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    return root, url_var, buscar, lista_imgs, barraProgreso, estado, imagen, totalImgs


async def descargar_fotos(url, subject):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            img_tags = soup.find_all('img')
            img_urls = [(urljoin(url, img.get('src')), img.get('alt', '')) for img in img_tags if img.get('src')]
            total_images = len(img_urls)

            if not img_urls:
                subject.on_error(Exception("No se encontraron imágenes."))
                return

            subject.on_next(("total", total_images))

            for i, (img_url, alt_text) in enumerate(img_urls):
                absolute_img_url = urljoin(url, img_url)
                try:
                    async with session.get(absolute_img_url) as img_response:
                        img_data = await img_response.read()
                        name = alt_text if alt_text else absolute_img_url.split("/")[-1]
                        subject.on_next(("image", name, img_data, i + 1, total_images))
                except Exception as e:
                    subject.on_error(e)

            subject.on_completed()
        except Exception as e:
            subject.on_error(e)


def run_asyncio_task(coro):
    asyncio.ensure_future(coro)


def update_user(subject, lista_imgs, barraProgreso, estado, imagen, totalImgs):
    def handle_event(event):
        if event[0] == "total":
            total_images = event[1]
            totalImgs.config(text=f"Se encontraron {total_images} imágenes")
            barraProgreso["maximum"] = total_images
            barraProgreso["value"] = 0
            lista_imgs.delete(0, "end")
            lista_imgs.image_data = []

        elif event[0] == "image":
            name, img_data, current, total = event[1:]
            lista_imgs.insert("end", name)
            lista_imgs.image_data = getattr(lista_imgs, "image_data", [])
            lista_imgs.image_data.append(img_data)
            barraProgreso["value"] = current
            estado.config(text=f"Descargando {current}/{total}...")

    def on_select(_):
        selected_index = lista_imgs.curselection()
        if selected_index:
            img_data = lista_imgs.image_data[selected_index[0]]
            image = Image.open(io.BytesIO(img_data))
            photo = ImageTk.PhotoImage(image)
            imagen.config(image=photo)
            imagen.image = photo

    lista_imgs.bind("<<ListboxSelect>>", on_select)

    subject.subscribe(
        on_next=handle_event,
        on_error=lambda e: estado.config(text=f"Error: {str(e)}"),
        on_completed=lambda: estado.config(text="Descarga completada.")
    )


def main():
    root, url_var, buscar, lista_imgs, barraProgreso, estado, imagen, totalImgs = user_fotos()

    def start_fetch():
        subject = Subject()
        update_user(subject, lista_imgs, barraProgreso, estado, imagen, totalImgs)
        run_asyncio_task(descargar_fotos(url_var.get(), subject))

    buscar.config(command=start_fetch)

    def run_asyncio_in_background():
        loop = asyncio.get_event_loop()
        loop.call_soon(loop.stop)
        loop.run_forever()
        root.after(100, run_asyncio_in_background)

    root.after(100, run_asyncio_in_background)
    root.mainloop()

if __name__ == "__main__":
    main()
