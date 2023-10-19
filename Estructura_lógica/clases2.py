import random as rn
import math
from scipy.spatial import distance
import networkx as nx
import matplotlib.pyplot as plt
from moviepy.editor import *
class carro:
    def __init__(self,cod, posicion, carga, capacidad,tipo,estacion,clase):
        self.id=cod
        self.posicion=posicion
        self.carga=carga
        self.capacidad=capacidad
        self.tipo=tipo
        self.rango=carga*tipo
        self.cargando=False
        self.estacion=estacion
        self.estado='andando'
        self.clase=clase
    def __str__(self):
        return f"id:{self.id}\npocicion:{self.posicion}\ncarga:{self.carga*100}%\nrango:{self.rango}\nestacion:{self.estacion.id}"
    def hacer_fila(self,punto_de_carga):
        punto_de_carga.fila.append(self)
        return len(punto_de_carga.fila)
    def moverse(self):
        old_pos=self.posicion
        self.posicion=cord_rand(old_pos,self.rango*0.25)
        self.rango=self.rango - distance.euclidean(self.posicion,old_pos)
        self.carga=self.rango/self.capacidad


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
    def buscar_cargador_rn(self,ls_cargadores):
        self.estacion=rn.choice(ls_cargadores)
    def buscar_cargador_dis(self,ls_cargadores):
        minimo=self.estacion
        for x in ls_cargadores:
            if  distance.euclidean(self.posicion,x.posicion)<=self.rango:
                if distance.euclidean(self.posicion,x.posicion)<distance.euclidean(self.posicion,minimo.posicion):
                    minimo=x
                else:
                     continue
            else:
                 continue        
    def ir_cargador(self):
        old_pos=self.posicion
        self.posicion=self.estacion.posicion
        self.rango=self.rango - distance.euclidean(self.posicion,old_pos)
        self.carga=self.rango/self.tipo
        return distance.euclidean(self.posicion,old_pos)
    def list_cargador(self,ls_cargadores):
        ls=[]
        for x in ls_cargadores:
            if  distance.euclidean(self.posicion,x.posicion)<=self.rango*0.25:
                ls.append(x)
        return ls

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
            return 50
        def cargar2(self):
            cos=0
            for x in self.cargando:
                x.carga=1
                x.rango=x.carga*x.tipo
                x.estado='andando'
                x.moverse()
                x.buscar_cargador
                #self.carga=self.carga-0.01
                cos=cos+(10/self.tipo)+10
            self.cargando=[]
            for n in range(self.capacidad):
                if self.fila:
                    c=self.fila.pop()
                    self.cargando.append(c)
                else:
                    continue
            return cos + len(self.fila)*10
        
def cord_rand(p,r):
    alpha = 2 * math.pi * rn.random()
    # random radius
    r = r * math.sqrt(rn.random())
    # calculating coordinates
    x = r * math.cos(alpha) + p[0]
    y = r * math.sin(alpha) + p[1]
    return (x,y)

def crear_carros(n1,n2,n3,est,i):
    carros=[]
    for x in range(n1):
        cor=cord_rand(est.posicion,2)
        car=carro(f'{x}_k1',cor,(rn.triangular(0.25, 1,0.75)),480000,50,est,'BYD')
        carros.append(car)
        
    for y in range(n2):
        
        cor=cord_rand(est.posicion,2)
        car=carro(f'{y}_k2',cor,(rn.triangular(0.25, 1,0.75)),15000,60,est,'Zoe')
        carros.append(car)
    for z in range(n3):
        cor=cord_rand(est.posicion,2)
        car=carro(f'{z}_k3',cor,(rn.triangular(0.25, 1,0.75)),30000,40,est,'i3')
        carros.append(car)
    return carros 

def crear_estaciones(dist,cord,Manual=[],const=1):
    ls_estacion=[]
    for x in cord:
        if dist=='rand':
            vl=rn.randint(1,3)
        if dist=='const':
            vl=const
        if dist=='manual':
            vl=Manual[x]
        est=punto_de_carga(x,cord[x],1,6,vl)
        ls_estacion.append(est)
    return ls_estacion

def algo_BG(n_i,k1,k2,k3,cor,dist,Manual=[],cost=1,vid=False):
    costo=0
    ls_estacion=crear_estaciones(dist,cor,Manual,cost)
        
    ls_carros=[]

    i=0
    for e in ls_estacion:
        ls_carros=ls_carros+crear_carros(k1,k2,k3,e,i)
        i=i+10
    g=nx.Graph()
    vertices=[x for x in range(21) if x>0]
    for n in vertices:
        g.add_node(n,tp='estacion',cl='estacion')
    #print(verices)


    aristas=[]
    for x in ls_carros:
        g.add_node(x.id,tp=x.estado,cl=x.clase)
        cor.update({x.id:x.posicion})
        y=(x.id,x.estacion.id)
        aristas.append(y)
    #print(aristas)
    #print(cor)


    color_map=nx.get_node_attributes(g,'tp')

    for k in color_map:
        if color_map[k]=='estacion':
            color_map[k]='black'
        if color_map[k]=='andando':
            color_map[k]='green'
        if color_map[k]=='ir a cargar':
            color_map[k]='yellow'
        if color_map[k]=='cargando' or color_map[k]=='enfila':
            color_map[k]='red'
    cl=[color_map.get(node) for node in g.nodes()]

    shape_map = nx.get_node_attributes(g, 'cl')

    for k in shape_map:
        if shape_map[k] == 'estacion':
            shape_map[k] = 's'
        if shape_map[k] == 'BYD':
            shape_map[k] = 'o'
        if shape_map[k] == 'Zoe':
            shape_map[k] = 'd'
        if shape_map[k] == 'i3':
            shape_map[k] = 's'

    for k, v in shape_map.items():
        g.nodes[k]['node_shape'] = v

    size_map = nx.get_node_attributes(g, 'cl')

    for k in size_map:
        if size_map[k] == 'estacion':
            size_map[k] = 20
        if size_map[k]== 'BYD':
            size_map[k] = 5
        if size_map[k]== 'Zoe':
            size_map[k] = 10
        if size_map[k]== 'i3':
            size_map[k] = 15
    # Asignar los tamaños de los nodos directamente al grafo
    zl=[size_map.get(node) for node in g.nodes()]
    g.add_edges_from(aristas)
    if vid:
        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_BG_0')
        plt.clf()
    for r in range(n_i):
        for x in ls_carros:
            if x.estado=='ir a cargar':
                costo=costo+x.ir_cargador()
                costo=costo+x.estacion.cargar(x)
                continue
            x.moverse()
            x.buscar_cargador(ls_estacion)
            if x.carga <= 0.25 or rn.randint(0,9)==4:
                x.estado='ir a cargar'
        for e in ls_estacion:
            costo=costo+e.cargar2()
            
        print('--------------------')
        g=nx.Graph()
        vertices=[x for x in range(21) if x>0]
        for n in vertices:
            g.add_node(n,tp='estacion',cl='estacion')
        #print(verices)
       
        aristas=[]
        for x in ls_carros:
            g.add_node(x.id,tp=x.estado,cl=x.clase)
            cor.update({x.id:x.posicion})
            y=(x.id,x.estacion.id)
            aristas.append(y)
        #print(aristas)
        #print(cor)


        color_map=nx.get_node_attributes(g,'tp')

        for k in color_map:
            if color_map[k]=='estacion':
                color_map[k]='black'
            if color_map[k]=='andando':
                color_map[k]='green'
            if color_map[k]=='ir a cargar':
                color_map[k]='yellow'
            if color_map[k]=='cargando' or color_map[k]=='enfila':
                color_map[k]='red'
                
        cl=[color_map.get(node) for node in g.nodes()]


        size_map = nx.get_node_attributes(g, 'cl')

        for k in size_map:
            if size_map[k] == 'estacion':
                size_map[k] = 20
            if size_map[k]== 'BYD':
                size_map[k] = 5
            if size_map[k]== 'Zoe':
                size_map[k] = 10
            if size_map[k]== 'i3':
                size_map[k] = 15
        # Asignar los tamaños de los nodos directamente al grafo
        zl=[size_map.get(node) for node in g.nodes()]
        g.add_edges_from(aristas)

        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_BG_{r+1}')
        plt.clf()

    if vid:
        print('video')
        frames=[]
        for x in range(n_i+1):
            I=ImageClip(f'algoritmo_BG_{x}.png').set_duration(2)
            frames.append(I)
        Video_Clip=concatenate_videoclips(frames,method='compose')
        Video_Clip.write_videofile('BG.mp4',fps=24,remove_temp=True,codec="libx264", audio_codec="aac")
    return (costo)

def algo_dis(n_i,k1,k2,k3,cor,dist,Manual=[],cost=1,vid=False):
    costo=0
    ls_estacion=crear_estaciones(dist,cor,Manual,cost)
        
    ls_carros=[]

    i=0
    for e in ls_estacion:
        ls_carros=ls_carros+crear_carros(k1,k2,k3,e,i)
        i=i+10
    g=nx.Graph()
    vertices=[x for x in range(21) if x>0]
    for n in vertices:
        g.add_node(n,tp='estacion',cl='estacion')
    #print(verices)


    aristas=[]
    for x in ls_carros:
        g.add_node(x.id,tp=x.estado,cl=x.clase)
        cor.update({x.id:x.posicion})
        y=(x.id,x.estacion.id)
        aristas.append(y)
    #print(aristas)
    #print(cor)


    color_map=nx.get_node_attributes(g,'tp')

    for k in color_map:
        if color_map[k]=='estacion':
            color_map[k]='black'
        if color_map[k]=='andando':
            color_map[k]='green'
        if color_map[k]=='ir a cargar':
            color_map[k]='yellow'
        if color_map[k]=='cargando' or color_map[k]=='enfila':
            color_map[k]='red'
    cl=[color_map.get(node) for node in g.nodes()]

    shape_map = nx.get_node_attributes(g, 'cl')

    for k in shape_map:
        if shape_map[k] == 'estacion':
            shape_map[k] = 's'
        if shape_map[k] == 'BYD':
            shape_map[k] = 'o'
        if shape_map[k] == 'Zoe':
            shape_map[k] = 'd'
        if shape_map[k] == 'i3':
            shape_map[k] = 's'

    for k, v in shape_map.items():
        g.nodes[k]['node_shape'] = v

    size_map = nx.get_node_attributes(g, 'cl')

    for k in size_map:
        if size_map[k] == 'estacion':
            size_map[k] = 20
        if size_map[k]== 'BYD':
            size_map[k] = 5
        if size_map[k]== 'Zoe':
            size_map[k] = 10
        if size_map[k]== 'i3':
            size_map[k] = 15
    # Asignar los tamaños de los nodos directamente al grafo
    zl=[size_map.get(node) for node in g.nodes()]
    g.add_edges_from(aristas)
    if vid:
        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_dis_0')
        plt.clf()
    for r in range(n_i):
        for x in ls_carros:
            if x.estado=='ir a cargar':
                costo=costo+x.ir_cargador()
                costo=costo+x.estacion.cargar(x)
                continue
            x.moverse()
            x.buscar_cargador_dis(ls_estacion)
            if x.carga <= 0.25 or rn.randint(0,9)==4:
                x.estado='ir a cargar'
        for e in ls_estacion:
            e.cargar2()
        print('--------------------')
        g=nx.Graph()
        vertices=[x for x in range(21) if x>0]
        for n in vertices:
            g.add_node(n,tp='estacion',cl='estacion')
        #print(verices)
       
        aristas=[]
        for x in ls_carros:
            g.add_node(x.id,tp=x.estado,cl=x.clase)
            cor.update({x.id:x.posicion})
            y=(x.id,x.estacion.id)
            aristas.append(y)
        #print(aristas)
        #print(cor)


        color_map=nx.get_node_attributes(g,'tp')

        for k in color_map:
            if color_map[k]=='estacion':
                color_map[k]='black'
            if color_map[k]=='andando':
                color_map[k]='green'
            if color_map[k]=='ir a cargar':
                color_map[k]='yellow'
            if color_map[k]=='cargando' or color_map[k]=='enfila':
                color_map[k]='red'
                
        cl=[color_map.get(node) for node in g.nodes()]


        size_map = nx.get_node_attributes(g, 'cl')

        for k in size_map:
            if size_map[k] == 'estacion':
                size_map[k] = 20
            if size_map[k]== 'BYD':
                size_map[k] = 5
            if size_map[k]== 'Zoe':
                size_map[k] = 10
            if size_map[k]== 'i3':
                size_map[k] = 15
        # Asignar los tamaños de los nodos directamente al grafo
        zl=[size_map.get(node) for node in g.nodes()]
        g.add_edges_from(aristas)

        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_dis_{r+1}')
        plt.clf()

    if vid:
        print('video')
        frames=[]
        for x in range(n_i+1):
            I=ImageClip(f'algoritmo_dis_{x}.png').set_duration(2)
            frames.append(I)
        Video_Clip=concatenate_videoclips(frames,method='compose')
        Video_Clip.write_videofile('dis.mp4',fps=24,remove_temp=True,codec="libx264", audio_codec="aac")
    return (costo)

def algo_rn(n_i,k1,k2,k3,cor,dist,Manual=[],cost=1,vid=False):
    costo=0
    ls_estacion=crear_estaciones(dist,cor,Manual,cost)
        
    ls_carros=[]

    i=0
    for e in ls_estacion:
        ls_carros=ls_carros+crear_carros(k1,k2,k3,e,i)
        i=i+10
    g=nx.Graph()
    vertices=[x for x in range(21) if x>0]
    for n in vertices:
        g.add_node(n,tp='estacion',cl='estacion')
    #print(verices)


    aristas=[]
    for x in ls_carros:
        g.add_node(x.id,tp=x.estado,cl=x.clase)
        cor.update({x.id:x.posicion})
        y=(x.id,x.estacion.id)
        aristas.append(y)
    #print(aristas)
    #print(cor)


    color_map=nx.get_node_attributes(g,'tp')

    for k in color_map:
        if color_map[k]=='estacion':
            color_map[k]='black'
        if color_map[k]=='andando':
            color_map[k]='green'
        if color_map[k]=='ir a cargar':
            color_map[k]='yellow'
        if color_map[k]=='cargando' or color_map[k]=='enfila':
            color_map[k]='red'
    cl=[color_map.get(node) for node in g.nodes()]

    shape_map = nx.get_node_attributes(g, 'cl')

    for k in shape_map:
        if shape_map[k] == 'estacion':
            shape_map[k] = 's'
        if shape_map[k] == 'BYD':
            shape_map[k] = 'o'
        if shape_map[k] == 'Zoe':
            shape_map[k] = 'd'
        if shape_map[k] == 'i3':
            shape_map[k] = 's'

    for k, v in shape_map.items():
        g.nodes[k]['node_shape'] = v

    size_map = nx.get_node_attributes(g, 'cl')

    for k in size_map:
        if size_map[k] == 'estacion':
            size_map[k] = 20
        if size_map[k]== 'BYD':
            size_map[k] = 5
        if size_map[k]== 'Zoe':
            size_map[k] = 10
        if size_map[k]== 'i3':
            size_map[k] = 15
    # Asignar los tamaños de los nodos directamente al grafo
    zl=[size_map.get(node) for node in g.nodes()]
    g.add_edges_from(aristas)
    if vid:
        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_rn_0')
        plt.clf()
    for r in range(n_i):
        for x in ls_carros:
            if x.estado=='ir a cargar':
                costo=costo+x.ir_cargador()
                costo=costo+x.estacion.cargar(x)
                continue
            x.moverse()
            x.buscar_cargador_rn(ls_estacion)
            if x.carga <= 0.25 or rn.randint(0,9)==4:
                x.estado='ir a cargar'
        for e in ls_estacion:
            e.cargar2()
        print('--------------------')
        g=nx.Graph()
        vertices=[x for x in range(21) if x>0]
        for n in vertices:
            g.add_node(n,tp='estacion',cl='estacion')
        #print(verices)
       
        aristas=[]
        for x in ls_carros:
            g.add_node(x.id,tp=x.estado,cl=x.clase)
            cor.update({x.id:x.posicion})
            y=(x.id,x.estacion.id)
            aristas.append(y)
        #print(aristas)
        #print(cor)


        color_map=nx.get_node_attributes(g,'tp')

        for k in color_map:
            if color_map[k]=='estacion':
                color_map[k]='black'
            if color_map[k]=='andando':
                color_map[k]='green'
            if color_map[k]=='ir a cargar':
                color_map[k]='yellow'
            if color_map[k]=='cargando' or color_map[k]=='enfila':
                color_map[k]='red'
                
        cl=[color_map.get(node) for node in g.nodes()]


        size_map = nx.get_node_attributes(g, 'cl')

        for k in size_map:
            if size_map[k] == 'estacion':
                size_map[k] = 20
            if size_map[k]== 'BYD':
                size_map[k] = 5
            if size_map[k]== 'Zoe':
                size_map[k] = 10
            if size_map[k]== 'i3':
                size_map[k] = 15
        # Asignar los tamaños de los nodos directamente al grafo
        zl=[size_map.get(node) for node in g.nodes()]
        g.add_edges_from(aristas)

        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_rn_{r+1}')
        plt.clf()

    if vid:
        print('video')
        frames=[]
        for x in range(n_i+1):
            I=ImageClip(f'algoritmo_rn_{x}.png').set_duration(2)
            frames.append(I)
        Video_Clip=concatenate_videoclips(frames,method='compose')
        Video_Clip.write_videofile('rn.mp4',fps=24,remove_temp=True,codec="libx264", audio_codec="aac")
    return (costo)     

def test(m,n_i,k1,k2,k3,cor,dist,Manual=[],cost=1,vid=False,graph=False):
    a_bg=0
    a_dis=0
    a_rn=0
    for t in range(m):
        a_bg+=algo_dis(n_i,k1,k2,k3,cor,dist,Manual,cost,vid)
        a_dis+=algo_dis(n_i,k1,k2,k3,cor,dist,Manual,cost,vid)
        a_rn+=algo_rn(n_i,k1,k2,k3,cor,dist,Manual,cost,vid)
        print(t)
    a_bg=a_bg/m
    a_dis=a_dis/m
    a_rn=a_rn/m   
    if graph:
        plt.bar(['BG','Distance','random'],[a_bg,a_dis,a_rn])
        plt.savefig(fname=f'bars')
    return f'BG:{a_bg},Distance:{a_dis},random{a_rn}'