from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


with open("noticias_salida.txt", mode='r', encoding='utf-8') as f:
    corpus = f.readlines()

    #corpus = ['El niño corre velozmente por el camino a gran velocidad .',
    #          'El coche rojo del niño es grande .',
    #          'El coche tiene un color rojo brillante y tiene llantas nuevas .',
    #          '¿ Las nuevas canicas del niño son color rojo ?'
    #]

    # Representación vectorial binarizada
    # ~ vectorizador_binario = CountVectorizer(binary=True)
    vectorizador_binario = CountVectorizer(binary=True, token_pattern= r'(?u)\w\w+|\w\w+\n|\.\,\;\:\¿\?\¡\!')
    X = vectorizador_binario.fit_transform(corpus)
    print (vectorizador_binario.get_feature_names_out())
    print (X)#sparse matrix
    print (type(X))#sparse matrix
    # ~ print (type(X.toarray()))#dense ndarray
    print ('Representación vectorial binarizada')
    print (X.toarray())#dense ndarray

    A = csr_matrix(X.toarray())
    df_bin = pd.DataFrame.sparse.from_spmatrix(A, columns=vectorizador_binario.get_feature_names_out())
    df_bin.to_csv("./representación_binaria.csv")

    #Representación vectorial por frecuencia
    vectorizador_frecuencia = CountVectorizer(token_pattern= r'(?u)\w\w+|\w\w+\n|\.\,\;\:\¿\?\¡\!')
    X = vectorizador_frecuencia.fit_transform(corpus)
    print('Representación vectorial por frecuencia')
    print (X.toarray())

    B = csr_matrix(X.toarray())
    df_freq = pd.DataFrame.sparse.from_spmatrix(A, columns=vectorizador_binario.get_feature_names_out())
    df_freq.to_csv("./representación_vectorial_frecuencia.csv")

    #Representación vectorial tf-idf
    vectorizador_tfidf = TfidfVectorizer(token_pattern= r'(?u)\w\w+|\w\w+\n|\.\,\;\:\¿\?\¡\!')
    X = vectorizador_tfidf.fit_transform(corpus)
    print ('Representación vectorial tf-idf')
    print (X.toarray())

    C = csr_matrix(X.toarray())
    df_tf_idf = pd.DataFrame.sparse.from_spmatrix(A, columns=vectorizador_binario.get_feature_names_out())
    df_tf_idf.to_csv("./representación_tf_idf.csv")

    #uso_pandas!!!
