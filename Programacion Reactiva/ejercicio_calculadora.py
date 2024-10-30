from tkinter import Tk, Label, Button, Entry, Checkbutton, BooleanVar
from tkinter.ttk import Combobox

class Calculadora:

    def __init__(self):
        
        self.window = Tk()
        self.window.title("Calculadora")

        self.window.geometry('300x400')

        #Hacer el espacio para mostrar el resultado de la operacion
        self.label = Label(self.window, text="resultado", font=("Arial Bold", 20))
        self.label.grid(column=0, row=0)
        

        self.label = Label(self.window, text="1")

        self.window.mainloop()

Calculadora()

