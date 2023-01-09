import pandas as pd
from librerias import tokenizadorLematizador
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import json
import matplotlib.pyplot as plt

from librerias import dataSets
from librerias import vectorizacion

def main():

    #cargamos el dataset
    dataFrame = pd.read_excel("./Rest_Mex_2022_Sentiment_Analysis_Track_Train.xlsx") #<- Requiere que se instale openpyxl -> pip install openpyxl

    print(dataFrame)

    withoutTitles = dataFrame.drop('Title', axis=1)
    without_Opinions_And_Titles = withoutTitles.drop('Opinion', axis=1)  #<- dataset sin titulos ni opiniones

    titles = dataFrame['Title'].values
    opinions = dataFrame['Opinion'].values


    print("dataframe sin titulos ni opiniones:\n\n")
    print(without_Opinions_And_Titles)

    #aplicamos tokenizacion y lematización al texto de las columnas  Title y Opinion
    # print(opinions)
    # print(opinions.dtype)
    # print(type(opinions[8053]))
    # print(opinions[8053])

    # #error detectado, tenemos que remover el elemento 8054 de las opiniones ya que está vacío
    # listaOpiniones = opinions.tolist()
    # listaOpiniones.pop(8054)

    # print(type(listaOpiniones[29565]))  #<-detectamos otro error, removemos este elemento tambien, ya que esta vacio
    # print(listaOpiniones[29565])

    # listaOpiniones.pop(29565)

    # print(type(listaOpiniones[30209]))  #<-detectamos otro error, removemos este elemento tambien, ya que esta vacio
    # print(listaOpiniones[30209])

    #listaOpiniones.pop(29565)

    #tokenizadorLematizador.tokenizarLematizar(listaOpiniones, "opinionesTokenizadoLematizado.txt")  #<-una vez que guardamos los archivos tokenizados podemos dejar comentadaa esta lina
    
    print(titles[207])  #<- tiene un fromato de tipo date, vamos a mandar todo a txt
    listaTitles = titles.tolist()

    for i in range(len(listaTitles)):
        listaTitles[i] = str(listaTitles[i])

    #ahora ya que nos funamos dos elementos de las opiniones, ya que estaban en blanco, vamos a recuperarlos, al estar vacios, simplemente los añadimos vacios
    listaOpiniones = open("./opinionesTokenizadoLematizado.txt", "r").readlines()
    
    listaOpiniones.insert(8054, '')
    listaOpiniones.insert(29565, '')

    #tokenizadorLematizador.tokenizarLematizar(listaTitles, "titulosTokenizadoLematizado.txt") #<- igual, una vez obtenido el archivo, podemos comentar esta linea

    #ya que hemos aplicado las lemtizaciones y tokenizaciones, vamos a crear un nuevo dataframe, primero recuperando las listas de los titulos y opiniones, y después colocando cada lista en el dataframe
    
    # listaOpiniones = open("./opinionesTokenizadoLematizado.txt", "r").readlines()
    listaTitulos = open("./titulosTokenizadoLematizado.txt", "r").readlines()


    ObjetoDataFrame = {"Title": listaTitulos, "Opinion": listaOpiniones, 'Polarity': dataFrame['Polarity'], 'Attraction': dataFrame['Attraction']} 
    nuevoDataFrame = pd.DataFrame(data=ObjetoDataFrame)

    print(nuevoDataFrame)

    #ahora con el nuevo dataframe, vamos a dividirlo en 80 por ciento entrenamiento y 20 por ciento prueba

    # train, test = train_test_split(nuevoDataFrame, test_size=0.2, shuffle = True, random_state=0)	

    # print("conjunto de entrenamiento: \n\n", train)
    # print("conjuntod e prueba: \n\n", test)

    # #con el conjunto de entrenamiento armamos un conjunto de validacion
    
    X = nuevoDataFrame.drop(['Polarity', 'Attraction'], axis=1).values
    #target = nuevoDataFrame['Polarity'].values
    target = nuevoDataFrame['Attraction'].values

    x = []

    for element in X:
        x.append(str(element))

    representacionVectorial = vectorizacion.VectorizarFrec(x)

    #dataset = dataSets.crearConjuntosDeValidacion(1, representacionVectorial, target)

    #probando con un conjunto de entrenamiento y uno de prueba------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(representacionVectorial, target,test_size=0.2, shuffle=True)

    #---------------------------------------------------------------------------------------------------------

    #print("se ha vectorizado")


    # #reporte de la clasificacion
    # target_names = ['1','2','3','4','5']

    # print(classification_report(dataframeConClasificacion['Polarity'], predicciones_polaridad))
    # print (confusion_matrix(dataframeConClasificacion['Polarity'], predicciones_polaridad))

    # #matriz de confusion

    # cm = confusion_matrix(dataframeConClasificacion['Polarity'], predicciones_polaridad)
    # print (cm)
    # disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
    # disp.plot()
    # plt.show()

    i = 0
    clf = MultinomialNB()
    # clf.fit(X_train.toarray(), y_train)
    contador1 = 0
    contador2 = int(X_train.shape[0]/5)
    for i in range(4):
        #clf.partial_fit(X_train.toarray()[contador1 : contador2], y_train[contador1 : contador2], classes = [1,2,3,4,5])
        clf.partial_fit(X_train.toarray()[contador1 : contador2], y_train[contador1 : contador2], classes = ['Hotel', 'Restaurant', 'Attractive'])
        contador1+= int(X_train.shape[0]/5)
        contador2+= int(X_train.shape[0]/5)

    #clf.partial_fit(X_train.toarray()[contador2:], y_train[contador2:], classes = [1,2,3,4,5])
    clf.partial_fit(X_train.toarray()[contador2:], y_train[contador2:], classes = ['Hotel', 'Restaurant', 'Attractive'])
    

    #ahora lo implementamos en el conjunto de prueba

    y_predict = clf.predict(X_test.toarray())

    print(y_predict)
    print(y_test)
    print(accuracy_score(y_test, y_predict))
    print(f1_score(y_test, y_predict, average = None))

    # #reporte de la clasificacion
    #target_names = ['1','2','3','4','5']
    target_names = ['Hotel', 'Restaurant', 'Attractive']

    print(classification_report(y_test, y_predict))
    print (confusion_matrix(y_test, y_predict))

    #matriz de confusion

    cm = confusion_matrix(y_test, y_predict)
    print (cm)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
    disp.plot()
    plt.show()
        
        
    return 0

if __name__ == "__main__":
    main()
