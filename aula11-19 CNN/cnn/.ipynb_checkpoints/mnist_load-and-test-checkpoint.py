import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
#from keras.models import Sequential
#from keras.layers import Dense, Flatten, Dropout
from keras.utils import np_utils
#from keras.layers import Conv2D, MaxPooling2D
#from keras.layers.normalization import BatchNormalization
from sklearn.metrics import confusion_matrix
from keras.models import model_from_json

N_CLASSES = 10

def cnn_load(filepath='cnn.json', weight_file='weights.h5'):
  f = open(filepath, 'r')
  cnn_struct = f.read()
  f.close()

  cnn = model_from_json(cnn_struct)
  cnn.load_weights(weight_file)
  return cnn


#Carrega base MNIST
(X_training, y_training), (X_test, y_test) = mnist.load_data()

db_training = X_training.reshape(X_training.shape[0], 28, 28, 1)
db_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

#concatena bases de treinamento e teste
X = np.concatenate((db_training, db_test))
Y = np.concatenate((y_training, y_test))

#Muda escala para 0 a 1.0
X = X.astype('float32')
X /= 255

#Muda a codificação das classes, criando classes dummy de 0 a 9, com 
# 0 = 100000000
# 1 = 000000010
# etc

y_cat = np_utils.to_categorical(Y, N_CLASSES)


#Carrega a rede
classifier = cnn_load()
classifier.summary()


#Testa uma entrada
print("Teste...")
new_x = X[0].reshape(1, 28, 28, 1)
previsao = classifier.predict(new_x)
print("Probabilidades")
print(previsao)
print("Previsão:")
print(previsao>0.5)


#matriz de confusão
print("Matriz de confusão:")
predictions = classifier.predict(X)
classes = [np.argmax(t) for t in y_cat]
previsoes = [np.argmax(t) for t in predictions]
conf_matrix = confusion_matrix(previsoes, classes)
print(conf_matrix)
