import matplotlib.pyplot as plt
import re
import math

#METODOS

def getDistancias (dicio) :
    dist = 0
    distancias = dict()
    for chave1 in dicio:
        coordx1, coordy1 = dicio[chave1]
        x1 = float(coordx1)
        y1 = float(coordy1)
        for chave2 in dicio:
            if chave1 != chave2 : 
            #inserir codigo impedindo realizar a iteracao de distancias repetidas
                coordx2, coordy2 = dicio[chave2]
                x2 = float(coordx2)
                y2 = float(coordy2)
                dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                distancias[chave1, chave2] = dist
            else:
                pass
    return distancias

def setPontos (fname) :
    pontos = dict()
    fhand = open(fname) #ler arquivo
    for line in fhand: 
        line = line.rstrip()
        chave = re.findall('^[(A-Za-z)]', line) #get key
        x = re.findall('([0-9]+),', line) #get a from a, b
        y = re.findall(',([0-9]+)', line) #get b from a, b
        pontos[chave[0]] = x[0], y[0] #atribui novo par {key: a, b} ao dicio pontos
    return pontos

#MAIN

#leitura e extracao das coordenadas
NomeLocais = input('insira nome do arquivo dos pontos: ')
locais = setPontos(NomeLocais) #coleta as coordenadas dos locais
print (locais) 
distancias = getDistancias(locais) #determina distancias entre os pontos
print(distancias)
NomeTerreno = input('insira nome do arquivo do terreno: ')
terreno = setPontos(NomeTerreno)
print (terreno)

#plotar pontos e terreno
pontos = locais.keys()
x = list()
y = list()
for value in locais : #coleta o valor das coordenadas em listas
    coordx, coordy = locais[value]
    x.append(float(coordx)) #dimensao x
    y.append(float(coordy)) #dimensao y
fig = plt.figure(dpi=200) #construcao do objeto grafico
ax = fig.add_axes([0.13, 0.13, 0.83, 0.83])
ax.scatter(x, y, color='red', marker='.')
for i, point in enumerate(pontos): #nomeamento dos pontos
    ax.annotate(' ' + point, (x[i], y[i]))

pontinhos = terreno.keys()
x2 = list()
y2 = list()
for value in terreno : #coleta o valor das coordenadas em listas
    coordx2, coordy2 = terreno[value]
    x2.append(float(coordx2)) #dimensao x
    y2.append(float(coordy2)) #dimensao y
x2.append(x2[0])
y2.append(y2[0])
ax.plot(x2, y2, color='black', marker='.')


for i, point in enumerate(pontinhos): #nomeamento dos pontos
    ax.annotate(' ' + point, (x2[i], y2[i]))

print(x2)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()