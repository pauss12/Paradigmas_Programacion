#Escribir un programa que triplique todos los elementos de una lista de enteros

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def triple(x):
    return x * 3

print(lista)
print(list(map(triple, lista)))

#Hacerlo en una linea:
print(list(map(lambda x: x * 3, lista)))