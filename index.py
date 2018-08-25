import matplotlib.pyplot as plt
import re
import math
import shapely.geometry as shapgeo

#METODOS

def getDistancias (locais, terreno) :
    dist, soma = 0, 0
    rota = False
    distancias = dict()
    for k1 in locais:
        x1, y1 = locais[k1]
        for k2 in locais:
            if k1 != k2 : #teste pra nao calcular distancia tipo AA
                if (k2 + k1) not in distancias : # dist AB = dist BA logo pula a iteração
                    x2, y2 = locais[k2]
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                    distancias[k1 + k2] = dist
                    soma += dist
                else:
                    soma += dist
                    pass
    for k1 in locais:
        for k2 in locais:
            if k1 != k2 : #teste pra nao calcular distancia tipo AA
                if (k2 + k1) not in distancias : # dist AB = dist BA logo pula a iteração
                    if not(isRota(locais, terreno, rota, k1, k2)): #testar possibilidade de rota
                        distancias[k1 + k2] += 10*soma
    return distancias

def setPontos (fname) :
    pontos = dict()
    fhand = open(fname) #ler arquivo
    for line in fhand: 
        line = line.rstrip()
        chave = re.findall('^[(A-Za-z0-9)]', line) #get key
        x = re.findall('([0-9]+),', line) #get a from a, b
        y = re.findall(',([0-9]+)', line) #get b from a, b
        pontos[chave[0]] = float(x[0]), float(y[0]) #atribui novo par {key: a, b} ao dicio pontos
    return pontos

def getPontos (dicio):
    x = list()
    y = list()
    for value in dicio : #coleta o valor das coordenadas em listas
        coordx, coordy = dicio[value]
        x.append(coordx) #dimensao x
        y.append(coordy) #dimensao y
    return x, y

def isRota (locais, terreno, rota, k1, k2) :
    vertices = list()
    for ponto in terreno: vertices.append(terreno[ponto])
    area = shapgeo.LinearRing(vertices) #define o poligono do terreno
    reta = shapgeo.LineString([locais[k1], locais[k2]]) #define reta entre os pontos
    #print(reta)
    rota = not(reta.intersects(area)) #checa intersecçao, TRUE se nao houver intersecçao
    return rota

def writeCusto (locais, distancia):
    file = open('custos.txt', 'w')
    linhat, cabecalho, linha, pontos  = '', '', '', ''
    linha = 'data; \nparam n :=' + str(len(locais)) + '; #numero de cidades \n\n'
    file.write(linha)
    for ponto in locais:
        pontos = pontos + ' ' + ponto
    linha = 'set I:=' + pontos + '; #cidades de \nset J:=' + pontos + '; #cidades para \n\n#Matriz de Custos:\n'
    file.write(linha)
    cabecalho = 'param C:'
    for local in locais:
        cabecalho = cabecalho + '     ' + local
    file.write(cabecalho + ':=')
    for k1 in locais:
        linhat = ''
        linhat = '\n\t\t' + linhat + k1 + '  '
        for k2 in locais:
            if k1 != k2:
                if (k2 + k1) not in distancia :
                    linhat = linhat + ' ' + str(round(distancia[k1+k2], 2)) + ' '
                else:
                    linhat = linhat + ' ' + str(round(distancia[k2+k1], 2)) + ' '
            else:
                linhat = linhat + ' 0 '
        linhat = linhat
        file.write(linhat)
    file.write(';\n end;')
    file.close()
    return file
#MAIN

#leitura e extracao das coordenadas
#NomeLocais = input('insira nome do arquivo dos pontos: ')
locais = setPontos('pontos.txt') #coleta as coordenadas dos locais
#print (locais) 

#NomeTerreno = input('insira nome do arquivo do terreno: ')
terreno = setPontos('terreno.txt')
#print (terreno)

distancias = getDistancias(locais, terreno) #determina distancias entre os pontos
print(distancias)

#plotar pontos e terreno
x1, y1 = getPontos(locais)
fig = plt.figure(dpi=200) #construcao do objeto grafico
ax = fig.add_axes([0.13, 0.13, 0.83, 0.83])
ax.scatter(x1, y1, color='red', marker='.')
pontosLocais = locais.keys()
for i, point in enumerate(pontosLocais): #nomeamento dos pontos
    ax.annotate('\n ' + point, (x1[i], y1[i]))

x2, y2 = getPontos(terreno)
x2.append(x2[0])
y2.append(y2[0])
ax.plot(x2, y2, color='black', marker='.')
pontosTerreno = terreno.keys()
for i, point in enumerate(pontosTerreno): #nomeamento dos pontos
    ax.annotate('\n ' + point, (x2[i], y2[i]))

ax.set_xlabel('x')
ax.set_ylabel('y')
#plt.show()

writeCusto(locais, distancias)