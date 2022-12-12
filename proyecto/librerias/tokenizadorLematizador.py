import spacy
import re


def tokenizarLematizar(dataset, archivoSalida):
    '''
    aplica la tokenización y lematización a un dataset y guarda un arhivo con la tokenización y lematizacion ya hecha
    dataset:    lista de elementos
    archivoSalida: string que le va a dar nombre al archivo de salida
    '''

    nlp = spacy.load("es_core_news_sm")
    nlp.max_length = 1600000
    #noticias_entrada = open('corpus_noticias.txt', 'r',encoding='utf8')
    #with open('file_name', 'r',encoding='utf8') as archivo_entrada:
    #    dataset = archivo_entrada.readlines()

    for i in range (len(dataset)):
        #print("valor de i: ", i)
        dataset[i]=re.sub("\d+&+","",dataset[i])
        dataset[i]=re.sub("[a-zA-ZÀ-ÿ]+&+","",dataset[i])#data set limpio
        dataset[i]=re.sub("&+","",dataset[i])#data set limpio
        dataset[i]=re.sub("[\d.]+","",dataset[i])#data set limpio
        dataset[i]=re.sub("(,\s,\s)+","",dataset[i])#data set limpio

    stopwords = nlp.Defaults.stop_words
    archivo_salida = open(archivoSalida, 'w', encoding='utf8')

    for noticia in dataset:
        doc = nlp(noticia)#tokenizamos
        normalizado=""
        for token in doc:
            #print(token.text, token.pos_, token.dep_, token.lemma_)
            
            normalizado = normalizado +token.lemma_ + " "# Recordatoriousar token.text
        normalizado2=""

        for token in normalizado.split():
            if token.lower() not in stopwords:    #checking whether the word is not 
                normalizado2 = normalizado2 +token+ " "
    #print(nlp.Defaults.stop_words)

        
        archivo_salida.write(normalizado2 + "\n")
    archivo_salida.close()