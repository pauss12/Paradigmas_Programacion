#Función factorial que, tomando un numero como entrada, nos devuelva el factorial de ese número. Con funciones lambda, map, filter y reduce.
from functools import reduce

def factorial(n):
    if n == 0:
        return 1
    num = reduce(lambda x, y: x * y, range(1, n + 1))
    return num

# Pruebas ------------------------------------------
print(factorial(0))  # 0! = 1
print(factorial(1))  # 1! = 1
print(factorial(2))  # 2! = 2 * 1 = 
print(factorial(3))  # 3! = 3 * 2 * 1 = 6
print(factorial(4))  # 4! = 4 * 3 * 2 * 1 = 24
print(factorial(5))  # 5! = 5 * 4 * 3 * 2 * 1 = 120
print(factorial(6))  # 6! = 720
print(factorial(7))  # 7! = 5040