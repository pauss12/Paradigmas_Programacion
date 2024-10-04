#EJERCICIO

#Con los conocimientos adquiridos en la clase de hoy, crea un programa que te diga la edad de tu mascota en años humanos.
#Tipos de mascota:
#Perro: 1 año perruno = 7 años humanos
#Gato: 1 año gato = 5 años de humano
#Pez: 1 año pez = 12 años humanos

def mostrar_edad(edad):
    return edad
    
def perro(mostrar_edad):
    edad = int(input("¿Cuantos años tiene tu perro?"))
    edad = edad * 7
    print("Tu perro tiene ", mostrar_edad(edad), " años humanos")

def gato(mostrar_edad):
    edad = int(input("¿Cuantos años tiene tu gato?"))
    edad = edad * 5
    print("Tu gato tiene ", mostrar_edad(edad), " años humanos")

def pez(mostrar_edad):
    edad = int(input("¿Cuantos años tiene tu Pez?"))
    edad = edad * 12
    print("Tu Pez tiene ", mostrar_edad(edad), " años humanos")


def main():
    
    mascota = input("¿Que tipo de mascota tienes: Pez, Perro o Gato?")
    if (mascota == "perro"):
        perro(mostrar_edad)
    elif (mascota == "gato"):
        gato(mostrar_edad)
    elif (mascota == "pez"):
        pez(mostrar_edad)

main()