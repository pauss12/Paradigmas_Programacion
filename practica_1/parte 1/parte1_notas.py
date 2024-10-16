#Tenemos una lista de estudiantes, donde cada estudiante tiene su nombre y una lista de calificaciones. Queremos filtrar a los estudiantes que tienen
#un promedio de calificaciones mayor o igual a 6 (nota mínima para aprobar). Como ejemplo podemos utilizar la siguiente lista: 
estudiantes = [
    {"nombre": "Juan", "calificaciones": [7, 8, 6, 5]},
    {"nombre": "Ana", "calificaciones": [9, 6, 8]},
    {"nombre": "Pedro", "calificaciones": [4, 5, 3]},
    {"nombre": "Maria", "calificaciones": [10, 9, 9]},
    {"nombre": "Luis", "calificaciones": [3, 2, 5]}
] 

def promedio(calificaciones):
    #Crear una lista con las calificaciones medias de cada estudiante, con 2 decimales. Añade el nombre del estudiante a la lista junto con su promedio.
    #Devuelve la lista con los estudiantes que han aprobado.
    lista_promedios = list(map(lambda x: {"nombre": x["nombre"], "promedio": round(sum(x["calificaciones"]) / len(x["calificaciones"]), 2)}, calificaciones))
    return lista_promedios

def get_aprobados(lista_promedios):
    #Filtrar los estudiantes que han aprobado. Devuelve una lista con los estudiantes que han aprobado.
    return list(filter(lambda x: x["promedio"] >= 6, lista_promedios))

def main():
    lista_promedios = promedio(estudiantes)
    aprobados = get_aprobados(lista_promedios)
    print(aprobados)

main()

