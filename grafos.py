import networkx as nx
import matplotlib.pyplot as plt
from clases import *
from random import *
from networkx.drawing.layout import bipartite_layout
#----------Crear vértices y aristas--------------
n = 7 #número de carros
V = [] #lista con n carros
for i in range (n):
    V.append("V"+str(i))
m = 4 #número de estaciones de carga
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
d_u = []
for i in range(len(distancias)):
    if distancias[i][2] <= rad_max:
        d_u.append(distancias[i])
#print(distancias_utiles)

#Cada carro se empareja con su estación con distancia mínima
def emparejar_con_minimo (distancias_utiles):
    val = 100
    est = 'nn'
    empa = []
    for j in V:
        for i in range(len(distancias_utiles)):
            if(distancias_utiles[i][0] == j):
                val = distancias_utiles[i][2]
                est = distancias_utiles[i][1]
                break
        for i in range(len(distancias_utiles)):
            if distancias_utiles[i][0] == j:
                if distancias_utiles[i][2] < val:
                    val = distancias_utiles[i][2]
                    est = distancias_utiles[i][1]
            if(i == len(distancias_utiles)-1):
                empa.append((j,est,val))
                val = 100
                est = 'nn'
    return empa

emparejamiento = emparejar_con_minimo(d_u)
#print(emparejamiento)

#Función para que cuando estén repetidas, borre de la lista y vuelva a buscar el emparejamiento mínimo
def encontrar_emparejamiento(empa, distancias):
    est_emp = []
    est_repe = ()
    for i in range(len(empa)):
        if empa[i][1] not in est_emp:
            #print('aaaaaaa')
            est_emp.append(empa[i][1])
            if i == len(empa)-1:
                return empa
        elif empa[i][1] in est_emp:
            est_emp = []
            est_repe = (empa[i][0], empa[i][1])
            break
    #print(distancias)
    d=distancias
    for i in distancias:
        if (i[0] == est_repe[0] and i[1] == est_repe[1]):
            d.remove(i)
            #print(distancias)
            break
            
    
    a = emparejar_con_minimo(d)
    return encontrar_emparejamiento(a, d)
En=encontrar_emparejamiento(emparejamiento,d_u)
print(En)
ls=[]
g=nx.Graph()
for x in E:
    g.add_node(x[0],tp='v',bipartite=0)
    g.add_node(x[1],tp='PC',bipartite=1)
    g.add_edge(x[0],x[1],cl='0000',weight=1)
color_map=nx.get_node_attributes(g,'tp')
for k in color_map:
    if color_map[k]=='v':
        color_map[k]='blue'
    if color_map[k]=='PC':
        color_map[k]='green'
cl=[color_map.get(node) for node in g.nodes()]
carros=[x for x in g.nodes() if x[0]=='V']
for j in En:
    g.add_edge(j[0],j[1],weight=j[2],cl='r')
colo_map=nx.get_edge_attributes(g,'cl').values()
w_map=nx.get_edge_attributes(g,'weight').values()
print(w_map)
nx.draw(g,node_color=cl,edge_color=colo_map,width=list(w_map),pos=bipartite_layout(g,carros),with_labels=True,node_size=650)
plt.show()