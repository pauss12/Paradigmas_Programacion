# Función cuadrados_sumados que, a partir de un numero natural n devuelva la suma de los cuadrados de todos los números entre 1 y n 
from functools import reduce

def cuadrados_sumados(n):
    lista = map(lambda x: x**2, range(1, n+1))
    list = reduce(lambda x, y: x + y, lista)
    return list

# Ejemplos para probar la función
print(cuadrados_sumados(1))  # 1^2 = 1
print(cuadrados_sumados(2))  # 1^2 + 2^2 = 1 + 4 = 5
print(cuadrados_sumados(3))  # 1^2 + 2^2 + 3^2 = 1 + 4 + 9 = 14
print(cuadrados_sumados(4))  # 1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30
print(cuadrados_sumados(5))  # 1^2 + 2^2 + 3^2 + 4^2 + 5^2 = 1 + 4 + 9 + 16 + 25 = 55
print(cuadrados_sumados(6))  # 1^2 + 2^2 + 3^2 + 4^2 + 5^2 + 6^2 = 1 + 4 + 9 + 16 + 25 + 36 = 91
print(cuadrados_sumados(7))  # 1^2 + 2^2 + 3^2 + 4^2 + 5^2 + 6^2 + 7^2 = 1 + 4 + 9 + 16 + 25 + 36 + 49 = 140

