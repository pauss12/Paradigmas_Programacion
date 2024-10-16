# Función cuadrados_sumados que, a partir de un numero natural n devuelva la suma de los cuadrados de todos los números entre 1 y n 
from functools import reduce

def cuadrados_sumados(n):
    lista = map(lambda x: x**2, range(1, n+1))
    list = reduce(lambda x, y: x + y, lista)
    return list

# Ejemplo
n = 5
print(cuadrados_sumados(n)) # 55