# Función palíndromos, que recibirá una lista de strings y nos devolverá una lista de True/False indicando cuales eran (o no) palíndromos. Para ello
# crearemos otra función es_palindromo que, a partir de un string, nos devuelva un
# booleano indicando si el string es palíndromo
from functools import reduce

def es_palindromo(string):
    #Creo una lista con las letras del string y la comparo con la lista invertida
    lista = list(map(str.lower, string))
    reversed_lista = list(reversed(lista))
    return list(map(str, lista)) == list(map(str, reversed_lista))

def palindromos(lista_strings):
    #Devuelve una lista de booleanos indicando si cada string es palíndromo, pero para ello, habria que recorrerse todas las cadenas de la lista y aplicar la función es_palindromo
    lista_strings = list(map(str.lower, lista_strings))
    lista_bools = list(map(es_palindromo, lista_strings))
    return lista_bools

# Ejemplo
lista_strings = ['oso', 'reconocer', 'hola', 'ana', 'Oso', 'ososoto', 'Paula', 'osooso']
print(palindromos(lista_strings)) 