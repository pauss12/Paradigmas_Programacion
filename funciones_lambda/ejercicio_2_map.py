#Escribir un programa que imprima por pantalla todos los elemetnos de una lista de strings
str = "hola"

def print_character(x):
    return x

print(str)

#Imprime un caracter por linea
print(list(map(print_character, str)))

#Otra forma de hacerlo:
lista = ["hola", "adios", "buenos dias", "buenas noches"]
list(map(print, lista))