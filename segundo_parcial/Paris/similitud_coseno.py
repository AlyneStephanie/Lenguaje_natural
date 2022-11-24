from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from tabulate import tabulate
import math 
import matplotlib.pyplot as plt
import seaborn as sns 

#corpus simple para realizar pruebas
corpus_prueba = ['El nino corre velozmente por el camino a gran velocidad .',
          'El coche rojo del niño es grande .',
          'El coche tiene un color rojo brillante y tiene llantas nuevas .',
          '¿ Las nuevas canicas del nino son color rojo ?'
]

corpus = []#variable donde remos el corpus

with open("noticias_salida.txt", encoding="utf-8") as fname:#estamos abriendo el archivo de donde tomaremos el corpus 
	lineas = fname.readlines()#leemos las lineas  del archivo 
	for linea in lineas:
		corpus.append(linea.strip('\n'))#agregamos cada linea al erreglo  corpus 

# Representación vectorial binarizada
# ~ vectorizador_binario = CountVectorizer(binary=True)

vectorizador_binario = CountVectorizer(binary=True, token_pattern= r'(?u)\w\w+|\w\w+\n|[.,&;:\?\¿¡!]')
X = vectorizador_binario.fit_transform(corpus) #vectorizamos el corpus

#print (vectorizador_binario.get_feature_names_out())
#print (X)#sparse matrix
#print (type(X))#sparse matrix
# ~ print (type(X.toarray()))#dense ndarray
#print ('Representación vectorial binarizada')
#print (X.toarray())#dense ndarray



df = pd.DataFrame(X.toarray(),columns=vectorizador_binario.get_feature_names_out() )
#print(vectorizador_binario.get_feature_names_out())
vectorizado_aux=X.toarray()#convertimos el vectorizado a array
#df.to_csv('vectorizado.csv')
#print(X.toarray())

#función coseno 
def cosine(x, y):
	val = sum(x[index] * y[index] for index in range(len(x)))
	sr_x = math.sqrt(sum(x_val**2 for x_val in x))
	sr_y = math.sqrt(sum(y_val**2 for y_val in y))
	res = val/(sr_x*sr_y)
	return (res)

#print("Similitud doc 1 y 2: " +str(cosine(vectorizado_aux[1][1:],vectorizado_aux[2][1:])))

similitud_coseno_matriz_total=[]#matriz donde guardaremos todas las similitudes con indice
mapa_de_calor=[]#matriz donde guardaremos todas las similitudes sin indicie


#obtener todas las opciones con un vector similitud<---

#print(len(vectorizado_aux))
#print(tabulate(vectorizado_aux))
for i in range(len(vectorizado_aux)):
	similitudes_del_vector=[]#lista en donde guardaremos las similitudes de el archivo i con cada archivo j 
	similitudes_simples=[]
	for j in range(len(vectorizado_aux)):
		similitudes_del_vector.append([cosine(vectorizado_aux[i][1:],vectorizado_aux[j][1:]),0])#para no tomar el encabezado que se tiene enonces solo tomamos el arreglo apartir del elemento 1 y agregamos otro elemento donde pondremos el indice del archivo
		similitudes_simples.append(cosine(vectorizado_aux[i][1:],vectorizado_aux[j][1:]))#guardamos la cercania sin indice
	similitud_coseno_matriz_total.append(similitudes_del_vector)#agregamos la lista creada en el for anterior en la matriz grandota
	mapa_de_calor.append(similitudes_simples)

for i in similitud_coseno_matriz_total:
	for j in range(int(len(i))):
		i[j][1]=j#colocamos el valor del indice de cada elemento en la matriz grandota



#print(similitud_coseno_matriz_total)
#for i in similitud_coseno_matriz_total:
#	print("\n"+str(i)+"\n")

similitudes_ordenadas=[]#aqui guardaremos las similitudes ordenadas de mayor a menos
for i in similitud_coseno_matriz_total:
	similitudes_ordenadas.append(sorted(i, key=lambda similitud: similitud[0], reverse=True))#ordenar a los individuos de acuerdo a su evaluacion

#dataframeSimilitudes=pd.DataFrame(similitud_coseno_matriz_total )#creamos el dataframe de las similitudes 

#dataframeSimilitudes.to_csv('similitudes.csv')
#print("simili")
#for i in similitud_coseno_matriz_total:
#print(dataframeSimilitudes)
#print(dataframeSimilitudesOrdenada)
#print(tabulate(similitudes_ordenadas))

#escribimos en archivo txt 
file = open("similitudes.txt", "w+",encoding="utf-8")#abrimos archivo donde vamos a guardar las similitudes
for i in range(len(similitudes_ordenadas)):
	for j in range(100):#solo imprimimos los 100 primeros archivos 
		print("noticia "+str(i)+" - noticia "+ str(similitudes_ordenadas[i][j][1])+"  :"+str(similitudes_ordenadas[i][j][0] ))#imprimimos en consola
		file.write("noticia "+str(i)+" - noticia "+ str(similitudes_ordenadas[i][j][1])+"  :"+str(similitudes_ordenadas[i][j][0] )+"\n")#guardamos en archivo txt 
	print("\n")
	file.write("\n")
file.close()
#mapa de calor
encabezados=[]#donde vamos a guardar los encabezados
diccionario={}#diccionario para crear el data frame para el mapa de calor 
for i in range(10):
		diccionario["documento_"+str(i)]=mapa_de_calor[i][0:10]#llenamos nuestro diccionario con los primeros 10 archivos
		encabezados.append("documento_"+str(i))


#print(diccionario)

dfcalor = pd.DataFrame(diccionario,encabezados)#definimos el dataframe para el mapa de calor
print (dfcalor)

sns.heatmap(data=dfcalor, cmap="Greens", annot=True)#funcion para crear el mapa 
plt.show()