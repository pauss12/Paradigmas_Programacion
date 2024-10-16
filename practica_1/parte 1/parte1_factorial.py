#Función factorial que, tomando un numero como entrada, nos devuelva el factorial de ese número. Con funciones lambda, map, filter y reduce.
from functools import reduce

def factorial(n):
    num = reduce(lambda x, y: x * y, range(1, n+1))
    return num

# Ejemplo
n = 5
print(factorial(n)) # 120

