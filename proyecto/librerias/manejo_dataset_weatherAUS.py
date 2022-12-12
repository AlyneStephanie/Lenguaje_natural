from encodings import utf_8
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
import numpy as np
import sys
import pickle
import random

class validation_set:
	def __init__(self, X_train, y_train, X_test, y_test):
		self.X_train = X_train
		self.y_train = y_train
		self.X_test = X_test
		self.y_test = y_test

class test_set:
	def __init__(self, X_test, y_test):
		self.X_test = X_test
		self.y_test = y_test

class data_set:
	def __init__(self, validation_set, test_set):
		self.validation_set = validation_set
		self.test_set = test_set

def generate_train_test(file_name, pliegues):
	#primero generamos un archivo que se contiene el dataset mezclado
	dataset = open("weatherAUS.csv", "r", encoding='utf8')
	datos = dataset.readlines()
	dataset.close()
	cadena = ""

	random.shuffle(datos)

	cadena =  str(encabezado)

	for element in datos:
		cadena += str(element)

	dataset = open("weatherAUS2.csv", "w", encoding='utf8')
	dataset.write(str(cadena))	
	dataset.close()

	# ~ pd.options.display.max_colwidth = 200		#Define el acho de las columnas (ancho máximo por default 50 caracteres)		
	#Lee el corpus original del archivo de entrada y lo pasa a un DataFrame
	df = pd.read_csv(file_name, sep=',', engine='python')
	X = df.drop('RainTomorrow',axis=1).values    						#corpus sin etiquetas 
	y = df['RainTomorrow'].values 									#etiquetas

	#definims una variable para controlar los pliegues
	#pliegues = input("validacion cruzada con cuantos pliegues")
	#tamanoTest = 1/pliegues

	return crearConjuntosDeValidacion(pliegues, X, y)

def crearConjuntosDeValidacion(pliegues, X, y):

	#Separa corpus en conjunto de entrenamiento y prueba

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle = False)	
	
	'''print('\n Dataset\n', df)
	print('\n Corpus')
	print('\n', *X)
	print ('----------------------')
	print('\n Etiquetas')
	print('\n', *y)
	print ('----------------------')
	print('\n Conjunto de prueba')
	print('\n X_test\n', *X_test)
	print('\n y_test\n', *y_test)
	print ('----------------------')
	print('\n Conjunto de entrenamiento = Conjunto de Validación')
	print('\n X_train\n', *X_train)
	print('\n y_train\n', *y_train)'''
	
	
	#Crea pliegues para la validación cruzada
	print ('----------------------')
	print('\n VALIDACION CRUZADA k=2\n')
	validation_sets = []
	kf = KFold(n_splits=pliegues)
	c=0
	for train_index, test_index in kf.split(X_train):
		c=c+1
		X_train_v, X_test_v = X_train[train_index], X_train[test_index]
		y_train_v, y_test_v = y_train[train_index], y_train[test_index]
		#Agrega el pliegue creado a la lista
		validation_sets.append(validation_set(X_train_v, y_train_v, X_test_v, y_test_v))
		'''print('\n PLIEGUE', c, '\n')
		print('X_train_v', *X_train_v,  '\ny_train_v', *y_train_v,'\n')
		print('X_test_v',  *X_test_v,  '\ny_test_v', *y_test_v)'''
	
	#Almacena el conjunto de prueba
	my_test_set = test_set(X_test, y_test)	
	
	#Guarda el dataset con los pliegues del conjunto de validación y el conjunto de pruebas
	my_data_set = data_set(validation_sets, my_test_set) 
	return (my_data_set)

	#guardamos los conjuntos de validacion y prueba en la clase my_data_set
	validation_sets = []

	validation_sets.append(validation_set(X_train, y_train, X_test, y_test))
	my_test_set = test_set(X_test, y_test)

	my_data_set = data_set(validation_sets, my_test_set) 
	return (my_data_set)


if __name__=='__main__':

	dataset = open("weatherAUS.csv", "r", encoding='utf8')
	datos = dataset.readlines()
	dataset.close()
	cadena = ""
	encabezadoX = ""
	encabezadoY = ""
	encabezado = datos.pop(0)

	arrEncabezado = encabezado.split(',')
	encabezadoY = arrEncabezado.pop()

	pliegues = int(input("numero de pliegues: "))

	for i in range(len(arrEncabezado)):

		if i < len(arrEncabezado)-1:
			encabezadoX += arrEncabezado[i] + ","
		else:
			encabezadoX += arrEncabezado[i]

	my_data_set=generate_train_test('weatherAUS2.csv', pliegues)
	
	#Guarda el dataset en formato csv
	np.savetxt("data_test.csv", my_data_set.test_set.X_test, delimiter=",", fmt="%s",
           header="x")
	
	np.savetxt("target_test.csv", my_data_set.test_set.y_test, delimiter=",", fmt="%s",
           header="y", comments="")
    
	i = 1
	for val_set in my_data_set.validation_set:
		np.savetxt("data_validation_train_" +str(pliegues)+ "_" +str(i)+ ".csv", val_set.X_train, delimiter=",", fmt="%s",
           header=encabezadoX, comments="")
		np.savetxt("data_test_" +str(pliegues)+ "_" +str(i)+ ".csv", val_set.X_test, delimiter=",", fmt="%s",
           header=encabezadoX, comments="")
		np.savetxt("target_validation_train_" +str(pliegues)+ "_" +str(i)+ ".csv", val_set.y_train, delimiter=",", fmt="%s",
           header=encabezadoY, comments="")
		np.savetxt("target_test" +str(pliegues)+ "_" +str(i)+ ".csv", val_set.y_test, delimiter=",", fmt="%s",
           header=encabezadoY, comments="")
		i = i + 1
	
	#Guarda el dataset en pickle
	dataset_file = open ('dataset.pkl','wb')
	pickle.dump(my_data_set, dataset_file)
	dataset_file.close()
	
	dataset_file = open ('dataset.pkl','rb')
	my_data_set_pickle = pickle.load(dataset_file)
	print ("-----------------------------------------------")
	#print (*my_data_set_pickle.test_set.X_test)

