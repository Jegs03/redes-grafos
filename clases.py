import random as rn
import math
from scipy.spatial import distance

class carro:
    def __init__(self,cod, posicion, carga, capacidad,tipo,estacion):
        self.id=cod
        self.posicion=posicion
        self.carga=carga
        self.capacidad=capacidad
        self.tipo=tipo
        self.rango=carga*tipo
        self.cargando=False
        self.estacion=estacion
        self.estado='andando'
    def __str__(self):
        return f"id:{self.id}\npocicion:{self.posicion}\ncarga:{self.carga*100}%\nrango:{self.rango}\nestacion:{self.estacion.id}"
    def hacer_fila(self,punto_de_carga):
        punto_de_carga.fila.append(self)
        return len(punto_de_carga.fila)
    def moverse(self):
        old_pos=self.posicion
        self.posicion=cord_rand(old_pos,self.rango*0.25)
        self.rango=self.rango - distance.euclidean(self.posicion,old_pos)
        self.carga=self.rango/self.tipo


    def buscar_cargador(self,ls_cargadores):
        minimo=self.estacion
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
        self.estacion=minimo
        
    def ir_cargador(self):
        old_pos=self.posicion
        self.posicion=self.estacion.posicion
        self.rango=self.rango - distance.euclidean(self.posicion,old_pos)
        self.carga=self.rango/self.tipo
    def distancia_cargador(self):
        return distance.euclidean(self.posicion,self.cargando.posicion)
        
                 
                 
                 

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
        def cargar(self,carro):
            self.fila.append(carro)
            carro.estado='enfila'
        def cargar2(self):
            
            for x in self.cargando:
                x.carga=1
                x.rango=x.carga*x.tipo
                x.estado='andando'
                x.moverse()
                x.buscar_cargador
                self.carga=self.carga-0.01
            self.cargando=[]
            for n in range(self.capacidad):
                if self.fila:
                    c=self.fila.pop()
                    self.cargando.append(c)
                else:
                    continue
        

def cord_rand(p,r):
    alpha = 2 * math.pi * rn.random()
    # random radius
    r = r * math.sqrt(rn.random())
    # calculating coordinates
    x = r * math.cos(alpha) + p[0]
    y = r * math.sin(alpha) + p[1]
    return (x,y)

def crear_carros(n,est,i):
    carros=[]
    for x in range(n):
        cor=cord_rand(est.posicion,2)
        car=carro(chr(x+97+i),cor,(rn.triangular(0.25, 1,0.75)),10000,50,est)
        carros.append(car)
    return carros 
