import pandas as pd
from librerias import tokenizadorLematizador
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
import json

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


    ObjetoDataFrame = {"Title": listaTitulos, "Opinion": listaOpiniones, "Polarity": dataFrame['Polarity'], "Attraction": dataFrame['Attraction']} 
    nuevoDataFrame = pd.DataFrame(data=ObjetoDataFrame)

    print(nuevoDataFrame)

    #ahora con el nuevo dataframe, vamos a dividirlo en 80 por ciento entrenamiento y 20 por ciento prueba

    train, test = train_test_split(nuevoDataFrame, test_size=0.2, shuffle = True, random_state=0)	

    print("conjunto de entrenamiento: \n\n", train)
    print("conjuntod e prueba: \n\n", test)


    #vamos a comenzar con la logica para determinar emociones
    #con base en el texto que anexó el profesor, el siguiente paso es comparar todas y cada una de las palabras del dataframe ya procesado e ir sumando sus FPA a cada emocion
    #para esto propongo crear una variable para cada emocion, y estas se inicializarán en 0 en cada iteracion, y para cada comparación se le van a ir sumando los FPA correspondientes a dicha emocion


    #probemos una logica para hacer lo mismo que estamos haciendo pero ahora con diccionarios:

    SEL = pd.read_excel("./SEL/SEL.xlsx")

    
    #Palabra	 Nula[%]	 Baja[%] 	 Media[%]	 Alta[%]	 PFA	Categor�a
    diccionario = {}
    for i in range(len(SEL['Palabra'])):

        diccionario[SEL['Palabra'][i]] = {'PFA' : SEL['PFA'][i], 'Categoría' : SEL['Categoría'][i]}
    
        
    print(diccionario['oscuro'])

    misCategorias = []
    misFPA = []

    for opinion in train['Opinion'].values:
        alegria = [0, "alegria"]
        sorpresa = [0, "aorpresa"]
        furia = [0, "furia"]
        miedo = [0, "miedo"]
        desagrado = [0, "desagrado"]
        trizteza = [0, "tristeza"]

        palabras = str(opinion).replace(',', '').replace('.', '').split(' ')

    
    # print(SEL['Palabra'])

        for palabra in palabras:

            try:
                #print(diccionario[palabra])
                match diccionario[palabra]['Categoría']:
                    case "Alegría":
                        #print("se ha hecho match con alegría")
                        alegria[0]+=float(diccionario[palabra]['PFA'])
                    case "Sorpresa":
                        sorpresa[0]+=float(diccionario[palabra]['PFA'])
                    case "Enojo":
                        furia[0]+=float(diccionario[palabra]['PFA'])
                    case "Miedo":
                        miedo[0]+=float(diccionario[palabra]['PFA'])
                    case "Repulsión":
                        desagrado[0]+=float(diccionario[palabra]['PFA'])
                    case "Tristeza":
                        trizteza[0]+=float(diccionario[palabra]['PFA']) 
            except:
                #next(palabra)
                e = 1

        #Evaluamos cual de los FPA es mayor para asignar la categoria emocional que tiene la noticia

        
        # print("alegria", alegria[0])
        # print("sorpresa", sorpresa[0])

        #negativas:----------------------------------------------------
        
        # print("furia", furia[0])
        # print("miedo", miedo[0])
        # print("desagrado", desagrado[0])
        # print("tristeza", trizteza[0])

        # print(max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]]))

        #tomamos el total de PFA de las emociones positivas y el PFA de las negativas y asignamos la polaridad correspondiente
        polaridad = max([(alegria[0] + sorpresa[0]), (miedo[0] + desagrado[0] + furia[0] + trizteza[0])])


        #en esta parte del algoritmo no estamo definiendo ningún umbral, unicamente estamos asignando la polaridad de las opiniones con base en que emociones predominan
        #recordemos que no contamos con esa información explícitamente, así que en este momento unicamente la estamos estimando por lo que predomina en el texto
        if(polaridad == 0):
            misCategorias.append("neutral")
            misFPA.append(0)
        elif (polaridad ==  (alegria[0] + sorpresa[0])):
            misCategorias.append('positivo')
            misFPA.append((alegria[0] + sorpresa[0])-(miedo[0] + desagrado[0] + furia[0] + trizteza[0]))
        elif (polaridad ==  (miedo[0] + desagrado[0] + furia[0] + trizteza[0])):
            misCategorias.append('negativo')
            misFPA.append((alegria[0] + sorpresa[0])-(miedo[0] + desagrado[0] + furia[0] + trizteza[0]))
    
    print("estas son las categorias que encontramos:\n\n")

    # for categoria in misCategorias:
    #     print(categoria)


    #es momento de integrar los datos obtenidos a un nuevo dataframe

    ObjetoDataFrame = {"Opinion": train['Opinion'], 'category': misCategorias} 


    dataframeConClasificacion = pd.DataFrame(data=ObjetoDataFrame)
    #dataframeConClasificacion.assign(categoria=lambda x:misCategorias[:])

    print (dataframeConClasificacion)
    print(type(dataframeConClasificacion))
    
    #creemos un conjunto de validacion de 5 pliegues para que mediante el metodo leave one out, entrenemos nuestro umbral clasificador
    
    target = dataframeConClasificacion['category'].values
    X = dataframeConClasificacion.drop('category', axis=1).values # <- esta isntrucción nos da arreglo de arreglos, esto no no s permitirá realizar correctamente la representacion vectorial


    dataset = dataSets.crearConjuntosDeValidacion(5, X, target)

    #el dataset que acabamos de crear se creó sobre el conjunto de prueba, ahora pra comenzar a entrenar un umbral, podemos convertirlo en un conjunto de validacion de n pliegues para comenzar a experimentar
    i = 1

    umbral = [-0.3,0.3]  #<- [limite inferior, limite superior]
    for pliegue in dataset.validation_set:
        
        #aqui es donde vamos a realizar el entrenamiento del umbral colocando como target el FPA
        #el entrenamiento primero se basará en predecir el valor de FPA, y después de haber inicializado un umbral, se pasara dos veces
        #en la misma iteracion para ver si el umbral se vuelve más angosto o mas amplio

        print("pliegue ", i)
        print(pliegue.X_train)
        i+=1

        x = []
        
        for element in pliegue.X_train:
            x.append(str(element))

        #print(x)
        #vamos a utilizar el modelo de clasificacion gaussiana para predecir el fpa, pero para ello, primero debemos de sacar una representacion vectorial binaria

        #sacando la representacion vectorial----------------------------------------------------------------------------------------------

        representacionVectorial = vectorizacion.VectorizarFrec(x)

        print(len(representacionVectorial.toarray()))
        print(len(pliegue.y_train))
        print(type(pliegue.y_train[0]))

        print(pliegue.y_train[0])
        #-----------------------------------------------------------------------------------------------------------------------------------

        clf = GaussianNB()

        clf.fit(representacionVectorial.toarray(), pliegue.y_train)

        y_predict = clf.predict(representacionVectorial.toarray())

        print(y_predict)
        print(accuracy_score(pliegue.y_train, y_predict))

    return 0

if __name__ == "__main__":
    main()
