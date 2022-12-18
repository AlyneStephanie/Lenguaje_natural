from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

corpus = ['El niño corre velozmente por el camino a gran velocidad .',
          'El coche rojo del niño es grande .',
          'El coche tiene un color rojo brillante y tiene llantas nuevas .',
          '¿ Las nuevas canicas del niño son color rojo ?'
]


def VectorizarBin(corpus):

    '''
    realiza la representacion vectorial de tipo binaria\n
    corpus:\t una lista de textos, lo cuales pueden ser, opiniones, noticias, parrafos, etc\n
    \tcada linea o elemento de dicha lista debe de contener exactamente una opinion, noticia, o cualquier otro texto
    '''

    # Representación vectorial binarizada
    # ~ vectorizador_binario = CountVectorizer(binary=True)
    vectorizador_binario = CountVectorizer(binary=True, token_pattern= r'(?u)\w\w+|\w\w+\n|\.')
    X = vectorizador_binario.fit_transform(corpus)
    print (vectorizador_binario.get_feature_names_out())
    print (X)#sparse matrix
    print (type(X))#sparse matrix
    # ~ print (type(X.toarray()))#dense ndarray
    print ('Representación vectorial binarizada')
    print (X.toarray())#dense ndarray

    return X

def VectorizarFrec(corpus):

    '''
    realiza la representacion vectorial de tipo frecuencial\n
    corpus:\t una lista de textos, lo cuales pueden ser, opiniones, noticias, parrafos, etc\n
    \tcada linea o elemento de dicha lista debe de contener exactamente una opinion, noticia, o cualquier otro texto
    '''

    #Representación vectorial por frecuencia
    vectorizador_frecuencia = CountVectorizer(token_pattern= r'(?u)\w\w+|\w\w+\n|\.')
    X = vectorizador_frecuencia.fit_transform(corpus)
    print('Representación vectorial por frecuencia')
    print (X.toarray())

    return X

def VectorizarTFIDF(corpus):

    '''
    realiza la representacion vectorial de tipo TF-IDF\n
    corpus:\t una lista de textos, lo cuales pueden ser, opiniones, noticias, parrafos, etc\n
    \tcada linea o elemento de dicha lista debe de contener exactamente una opinion, noticia, o cualquier otro texto
    '''

    #Representación vectorial tf-idf
    vectorizador_tfidf = TfidfVectorizer(token_pattern= r'(?u)\w\w+|\w\w+\n|\.')
    X = vectorizador_tfidf.fit_transform(corpus)
    print ('Representación vectorial tf-idf')
    print (X.toarray())

    #uso_pandas!!!

    return X