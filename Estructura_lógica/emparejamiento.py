import random

from clases import *
from random import *

#----------Crear vértices y aristas--------------
n = 9 #número de carros
V = [] #lista con n carros
for i in range (n):
    V.append("V"+str(i))
m = 3 #número de estaciones de carga
PC = [] #lista con 3m espacios de carga (3 por estación)
for i in range (m):
    for j in range(3):
        PC.append("PC"+str(i)+str(j))
E = [] #lista con aristas entre todos los espacios de carga y vehículos
for i in V:
    for j in PC:
        E.append((i,j))
#------------------------------------------------

#------------Empezar algoritmo-------------------

#Creo una lista con todas las distancias
distancias = []
for i in V:
    for j in PC:
        distancias.append((i,j,randint(1,20)))
#WARNING: acá no tengo comprendido que si los puntos de carga están dentro de la misma estación tienen la misma distancia, ya que asumo que la clase da las distancias garanizando que esas condiciones se cumplan

#Filtro teniendo en cuenta que no pueden superar un rad_max y obtengo las distancias posibles
rad_max = 10
distancias_utiles = []
for i in range(len(distancias)):
    if distancias[i][2] <= rad_max:
        distancias_utiles.append(distancias[i])
print(distancias_utiles)

#Cada carro se empareja con su estación con distancia mínima
def emparejar_con_minimo (distancias_utiles):
    val = 100
    est = 'nn'
    empa = []
    for j in V:
        for i in range(len(distancias)):
            if(distancias[i][0] == j):
                val = distancias[i][2]
                est = distancias[i][1]
                break
        for i in range(len(distancias)):
            if distancias[i][0] == j:
                if distancias[i][2] < val:
                    val = distancias[i][2]
                    est = distancias[i][1]
            if(i == len(distancias)-1):
                empa.append((j,est,val))
                val = 100
                est = 'nn'
    return empa

emparejamiento = emparejar_con_minimo(distancias_utiles)
print(emparejamiento)

#Función para que cuando estén repetidas, borre de la lista y vuelva a buscar el emparejamiento mínimo
def encontrar_emparejamiento(empa, distancias):
    est_emp = []
    est_repe = ()
    for i in range(len(empa)):
        if empa[i][1] not in est_emp:
            est_emp.append(empa[i][1])
            if i == len(empa)-1:
                return empa
        elif empa[i][1] in est_emp:
            est_emp = []
            est_repe = (empa[i][0], empa[i][1])
            break
    print(distancias)
    for i in distancias:
        if (i[0] == est_repe[0] and i[1] == est_repe[1]):
            distancias.remove(i)
            print(distancias)
            break

    a = emparejar_con_minimo(distancias)
    return encontrar_emparejamiento(a, distancias)

print(encontrar_emparejamiento(emparejamiento,distancias_utiles))
