import pandas as pd
from librerias import tokenizadorLematizador
from sklearn.model_selection import train_test_split
import numpy as np

def main():

    #cargamos el dataset
    dataFrame = pd.read_excel("./Rest_Mex_2022_Sentiment_Analysis_Track_Train.xlsx") #<- Requiere que se instale openpyxl -> pip install openpyxl

    print(dataFrame)

    withoutTitles = dataFrame.drop('Title', axis=1)
    without_Opinions_And_Opinions = withoutTitles.drop('Opinion', axis=1)  #<- dataset sin titulos ni opiniones

    titles = dataFrame['Title'].values
    opinions = dataFrame['Opinion'].values


    print("dataframe sin titulos ni opiniones:\n\n")
    print(without_Opinions_And_Opinions)

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

    SEL = pd.read_excel("./SEL/SEL.xlsx")

    categorias = [SEL['Palabra'].values, SEL['Categoría'].values, SEL['PFA'].values]

    #for categoria in categorias:

    print(categorias[2][1])

    misCategorias = []

    for opinion in train['Opinion'].values:
        alegria = [0, "alegria"]
        sorpresa = [0, "aorpresa"]
        furia = [0, "furia"]
        miedo = [0, "miedo"]
        desagrado = [0, "desagrado"]
        trizteza = [0, "tristeza"]

        palabras = str(opinion).replace(',', '').replace('.', '').split(' ')

        for palabra in palabras:

            #print("esto es una palabra: ", palabra)

            #comparamos cada elemento con SEL
            for i in range(len(categorias)):
                #print("me imprimo")
                if palabra == categorias[0][i]:
                    print("aqui hay un match")
                    match categorias[1][i]:
                        case "Alegría":
                            #print("se ha hecho match con alegría")
                            alegria[0]+=float(categorias[2][i])
                        case "Sorpresa":
                            sorpresa[0]+=float(categorias[2][i])
                        case "Enojo":
                            furia[0]+=float(categorias[2][i])
                        case "Miedo":
                            miedo[0]+=float(categorias[2][i])
                        case "Repulsión":
                            desagrado[0]+=float(categorias[2][i])
                        case "Tristeza":
                            trizteza[0]+=float(categorias[2][i]) 

        #Evaluamos cual de los FPA es mayor para asignar la categoria emocional que tiene la noticia

        
        # print("alegria", alegria[0])
        # print("sorpresa", sorpresa[0])
        # print("furia", furia[0])
        # print("miedo", miedo[0])
        # print("desagrado", desagrado[0])
        # print("tristeza", trizteza[0])

        # print(max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]]))

        if(max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]]) == 0):
            misCategorias.append([0, "sin categoria"])
        elif (alegria[0] == max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]])):
            misCategorias.append(alegria)
        elif (sorpresa[0] == max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]])):
            misCategorias.append(alegria)
        elif (furia[0] == max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]])):
            misCategorias.append(alegria)
        elif (miedo[0] == max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]])):
            misCategorias.append(alegria)
        elif (desagrado[0] == max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]])):
            misCategorias.append(alegria)
        elif (trizteza[0] == max([alegria[0], sorpresa[0], furia[0], trizteza[0], desagrado[0], miedo[0]])):
            misCategorias.append(alegria)
        else:
            misCategorias.append([0, "sin categoria"])
    
    #print("estas son las categorias que encontramos:\n\n")

    for categoria in misCategorias:
         print(categoria)


    return 0

if __name__ == "__main__":
    main()
