import pandas as pd
from librerias import tokenizadorLematizador

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

    return 0

if __name__ == "__main__":
    main()
