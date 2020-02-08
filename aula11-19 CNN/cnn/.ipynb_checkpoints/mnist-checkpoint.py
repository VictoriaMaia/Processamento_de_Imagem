import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.utils import np_utils,plot_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from sklearn.metrics import confusion_matrix


N_CLASSES = 10

def cnn_setup(n_classes, n_kernels = 32, kernel_size = (3,3)):
  #Instancia a rede
  cnn = Sequential()

  #Camada de convolução
  cnn.add(Conv2D(n_kernels, kernel_size,input_shape=(28, 28, 1), activation = 'relu'))

  #Normaliza os feature maps
  cnn.add(BatchNormalization())

  #camada de pooling
  cnn.add(MaxPooling2D(pool_size = (2,2)))

  #Novas camadas (opcional) de convolução e pooling
  cnn.add(Conv2D(n_kernels, kernel_size, activation = 'relu'))
  cnn.add(BatchNormalization())
  cnn.add(MaxPooling2D(pool_size = (2,2)))

  #Camada de flattening
  cnn.add(Flatten())

  #Rede densa
  n_neuronios = 128
  taxa_dropout = 0.2

  #Primeira camada oculta
  cnn.add(Dense(units = n_neuronios, activation = 'relu'))
  cnn.add(Dropout(taxa_dropout))

  #Segunda camada oculta
  cnn.add(Dense(units = n_neuronios, activation = 'relu'))
  cnn.add(Dropout(taxa_dropout))

  #Camada de saida
  cnn.add(Dense(units = n_classes, activation = 'softmax'))
  return cnn

def show_sample_data(inputs,classes):
  N = 10
  for i in range(N):
    plt.subplot(N,N,i+1),plt.imshow(inputs[i],cmap = 'gray')
    plt.title(classes[i]), plt.xticks([]), plt.yticks([])

  plt.show()


#Carrega base MNIST
(X_training, y_training), (X_test, y_test) = mnist.load_data()
#(X_training, y_training), (X_test, y_test) = fashion_mnist.load_data()

#Mostra alguns exemplos do dataset
#show_sample_data(X_test,y_test)

#Reshape
db_training = X_training.reshape(X_training.shape[0], 28, 28, 1)
db_test = X_test.reshape(X_test.shape[0], 28, 28, 1)


#Muda escala para 0 a 1.0
db_training = db_training.astype('float32')
db_test = db_test.astype('float32')
db_training /= 255
db_test /= 255

#Muda a codificação das classes, criando classes dummy de 0 a 9, com 
# 0 = 100000000
# 1 = 000000010
# etc.

classe_training = np_utils.to_categorical(y_training, N_CLASSES)
classe_test = np_utils.to_categorical(y_test, N_CLASSES)


#Cria a rede
classifier = cnn_setup(N_CLASSES)

#Compila a rede
classifier.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

#Treinamento
classifier.fit(db_training, classe_training, batch_size = 128, epochs = 3, validation_data = (db_test, classe_test))


#Teste da rede
print("Teste da rede:")
resultado = classifier.evaluate(db_test, classe_test)
print(resultado)


#Matriz de confusão
print("Matriz de confusão:")
predictions = classifier.predict(db_test)
classes = [np.argmax(t) for t in classe_test]
previsoes = [np.argmax(t) for t in predictions]
conf_matrix = confusion_matrix(previsoes, classes)
print(conf_matrix)


#Salva rede
#estrutura
with open('cnn.json', 'w') as json_file:
    json_file.write(classifier.to_json()) 

#pesos
classifier.save_weights('weights.h5')

#imagem da rede
plot_model(classifier, to_file='model.png')


