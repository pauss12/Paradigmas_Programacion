from tkinter import Tk, Label, Button
from functools import partial

#partial ==> construir funcion parcial

class Calculadora:

    def __init__(self):

        self.keyboard_height = 4
        self.keyboard_width = 4
        
        self.window = Tk()

        self.display = Label(text=0, font=("Arial Bold", 30))
        self.display.grid(column=0, row=0, columnspan=self.keyboard_width)
    
        list_symbols = ["9", "8", "7", "+", "6", "5", "4", "-", "3", "2", "1", "*", "0", "/", "="]

        i = 0
        for symb in list_symbols:
            button = Button(text=symb, font=("Arial Bold", 20), command=partial(self.buttonPressed, symb))
            if (symb == "="):
                button.grid(column= i % self.keyboard_width, 
                            row=int(i / self.keyboard_height + 1), 
                            padx=2, pady=2, columnspan=2)
            else:
                button.grid(column=i % self.keyboard_width, 
                            row=int(i / self.keyboard_height + 1),
                            padx=2, pady=2
                            )
            i += 1

        self.window.mainloop()

    def buttonPressed(self, btn_data):
        current_text = str(self.display.cget("text"))
        if (current_text == "0"):
            current_text = ""
            
        if btn_data == "=":
            self.display.configure(text=eval(current_text))
        else:
            self.display.configure(text=current_text + btn_data)

Calculadora()

