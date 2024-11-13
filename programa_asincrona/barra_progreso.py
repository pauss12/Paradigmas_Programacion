from tkinter import Tk, Label, Button
from tkinter import ttk
import time

# barra_progresadora = ttk.Progressbar(ventana, orient="horizontal", length=250, mode="determinate")
# barra_progresadora["value"] = i

class Barra_Progresar():

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Barra de Progreso")
        self.ventana.geometry("300x200")
        self.barra_progresadora = ttk.Progressbar(self.ventana, orient="horizontal", length=250, mode="determinate")
        self.barra_progresadora.place(x=25, y=50)
        self.boton = Button(self.ventana, text="Iniciar", command=self.iniciar)
        self.boton.place(x=125, y=100)

    def iniciar(self):
        self.boton["state"] = "disabled"
        for i in range(101):
            self.barra_progresadora["value"] = i
            time.sleep(0.1)
            self.ventana.update()
        self.boton["state"] = "normal"

ventana = Tk()
aplicacion = Barra_Progresar(ventana)
ventana.mainloop()
