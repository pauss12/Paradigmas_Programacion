#Escribir un programa que convierta los carateres de una lista a mayúsculas y a minúsculas, y elimine las letras duplicadas de una secuencia



def upper_lower(x):
    return x.upper(), x.lower()

def remove_duplicates(x):
    return "".join(set(x))

print(list(map(upper_lower, lista)))
print(list(map(remove_duplicates, lista)))

