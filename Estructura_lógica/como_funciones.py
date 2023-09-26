from clases import *
import networkx as nx
import matplotlib.pyplot as plt
from moviepy.editor import *


def algo_BG(n_i,k1,k2,k3,cor,vid=False):
    costo=0
    ls_estacion=[]
    for x in cor:
        est=punto_de_carga(x,cor[x],1,6,1)
        ls_estacion.append(est)
        
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
        if shape_map[k] == 'karro':
            shape_map[k] = 'o'
        if shape_map[k] == 'kamineta':
            shape_map[k] = 'd'
        if shape_map[k] == 'kamion':
            shape_map[k] = 's'

    for k, v in shape_map.items():
        g.nodes[k]['node_shape'] = v

    size_map = nx.get_node_attributes(g, 'cl')

    for k in size_map:
        if size_map[k] == 'estacion':
            size_map[k] = 20
        if size_map[k]== 'karro':
            size_map[k] = 5
        if size_map[k]== 'kamineta':
            size_map[k] = 10
        if size_map[k]== 'kamion':
            size_map[k] = 15
    # Asignar los tamaños de los nodos directamente al grafo
    zl=[size_map.get(node) for node in g.nodes()]
    g.add_edges_from(aristas)
    if vid:
        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_0')
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
            if size_map[k]== 'karro':
                size_map[k] = 5
            if size_map[k]== 'kamineta':
                size_map[k] = 10
            if size_map[k]== 'kamion':
                size_map[k] = 15
        # Asignar los tamaños de los nodos directamente al grafo
        zl=[size_map.get(node) for node in g.nodes()]
        g.add_edges_from(aristas)

        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_{r+1}')
        plt.clf()

    if vid:
        print('video')
        frames=[]
        for x in range(n_i+1):
            I=ImageClip(f'algoritmo_{x}.png').set_duration(2)
            frames.append(I)
        Video_Clip=concatenate_videoclips(frames,method='compose')
        Video_Clip.write_videofile('video.mp4',fps=24,remove_temp=True,codec="libx264", audio_codec="aac")
    return (costo)

def algo_dis(n_i,k1,k2,k3,cor,vid=False):
    costo=0
    ls_estacion=[]
    for x in cor:
        est=punto_de_carga(x,cor[x],1,6,1)
        ls_estacion.append(est)
        
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
        if shape_map[k] == 'karro':
            shape_map[k] = 'o'
        if shape_map[k] == 'kamineta':
            shape_map[k] = 'd'
        if shape_map[k] == 'kamion':
            shape_map[k] = 's'

    for k, v in shape_map.items():
        g.nodes[k]['node_shape'] = v

    size_map = nx.get_node_attributes(g, 'cl')

    for k in size_map:
        if size_map[k] == 'estacion':
            size_map[k] = 20
        if size_map[k]== 'karro':
            size_map[k] = 5
        if size_map[k]== 'kamineta':
            size_map[k] = 10
        if size_map[k]== 'kamion':
            size_map[k] = 15
    # Asignar los tamaños de los nodos directamente al grafo
    zl=[size_map.get(node) for node in g.nodes()]
    g.add_edges_from(aristas)
    if vid:
        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_0')
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
            if size_map[k]== 'karro':
                size_map[k] = 5
            if size_map[k]== 'kamineta':
                size_map[k] = 10
            if size_map[k]== 'kamion':
                size_map[k] = 15
        # Asignar los tamaños de los nodos directamente al grafo
        zl=[size_map.get(node) for node in g.nodes()]
        g.add_edges_from(aristas)

        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_{r+1}')
        plt.clf()

    if vid:
        print('video')
        frames=[]
        for x in range(n_i+1):
            I=ImageClip(f'algoritmo_{x}.png').set_duration(2)
            frames.append(I)
        Video_Clip=concatenate_videoclips(frames,method='compose')
        Video_Clip.write_videofile('video.mp4',fps=24,remove_temp=True,codec="libx264", audio_codec="aac")
    return (costo)

def algo_rn(n_i,k1,k2,k3,cor,vid=False):
    costo=0
    ls_estacion=[]
    for x in cor:
        est=punto_de_carga(x,cor[x],1,6,1)
        ls_estacion.append(est)
        
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
        if shape_map[k] == 'karro':
            shape_map[k] = 'o'
        if shape_map[k] == 'kamineta':
            shape_map[k] = 'd'
        if shape_map[k] == 'kamion':
            shape_map[k] = 's'

    for k, v in shape_map.items():
        g.nodes[k]['node_shape'] = v

    size_map = nx.get_node_attributes(g, 'cl')

    for k in size_map:
        if size_map[k] == 'estacion':
            size_map[k] = 20
        if size_map[k]== 'karro':
            size_map[k] = 5
        if size_map[k]== 'kamineta':
            size_map[k] = 10
        if size_map[k]== 'kamion':
            size_map[k] = 15
    # Asignar los tamaños de los nodos directamente al grafo
    zl=[size_map.get(node) for node in g.nodes()]
    g.add_edges_from(aristas)
    if vid:
        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_0')
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
            if size_map[k]== 'karro':
                size_map[k] = 5
            if size_map[k]== 'kamineta':
                size_map[k] = 10
            if size_map[k]== 'kamion':
                size_map[k] = 15
        # Asignar los tamaños de los nodos directamente al grafo
        zl=[size_map.get(node) for node in g.nodes()]
        g.add_edges_from(aristas)

        plt.xlim(0, 80)
        plt.ylim(0, 100)
        plt.autoscale(False)
        nx.draw(g,pos=cor,node_color=cl,node_size=zl)
        plt.savefig(fname=f'algoritmo_{r+1}')
        plt.clf()

    if vid:
        print('video')
        frames=[]
        for x in range(n_i+1):
            I=ImageClip(f'algoritmo_{x}.png').set_duration(2)
            frames.append(I)
        Video_Clip=concatenate_videoclips(frames,method='compose')
        Video_Clip.write_videofile('video.mp4',fps=24,remove_temp=True,codec="libx264", audio_codec="aac")
    return (costo)     