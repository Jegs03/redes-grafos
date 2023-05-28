import random as rn
import math
from scipy.spatial import distance

class carro:
    def __init__(self,id, posicion, carga, capacidad,tipo):
        self.id=id
        self.posicion=posicion
        self.carga=carga
        self.capacidad=capacidad
        self.tipo=tipo
        self.rango=carga*tipo
        self.cargando=False
    def __str__(self):
        return f"id:{self.id}\npocicion:{self.posicion}\ncarga:{self.carga*100}%\nrango:{self.rango}"
    def hacer_fila(self,punto_de_carga):
        punto_de_carga.fila.append(self)
        return len(punto_de_carga.fila)
    def moverse(self):
        old_pos=self.posicion
        self.posicion=cord_rand(old_pos,self.rango)
        self.rango=self.rango - distance.euclidean(self.posicion,old_pos)
        self.carga=self.rango/self.tipo


    def buscar_cargador(self,ls_cargadores):
        minimo=ls_cargadores[0]
        for x in ls_cargadores:
            if  distance.euclidean(self.posicion,x.posicion)<=self.rango:
                if distance.euclidean(self.posicion,x.posicion)<distance.euclidean(self.posicion,minimo.posicion):
                    if len(x.fila)/self.capacidad < 0.8:
                         minimo=x
                    else:
                         continue
                else:
                     continue
            else:
                 continue
        return minimo 
                 
                 
                 

class punto_de_carga:
        def __init__(self,id, posicion, carga, capacidad,tipo):
            self.id=id
            self.posicion=posicion
            self.carga=carga
            self.capacidad=capacidad
            self.tipo=tipo
            self.fila=[]
            self.cargando=[]
        def __str__(self):
            return f"id:{self.id}\npocicion:{self.posicion}\ncarga:{self.carga*100}%\nfila:{self.fila}"
        

def cord_rand(p,r):
    alpha = 2 * math.pi * rn.random()
    # random radius
    r = r * math.sqrt(rn.random())
    # calculating coordinates
    x = r * math.cos(alpha) + p[0]
    y = r * math.sin(alpha) + p[1]
    return (x,y)

