# Questão 7
# Utilizando como base as figuras 7a e 7b, forme o desenho de um “boneco palito” aplicando uma
# sequência de transformações geométricas e operações lógicas nas imagens, seguindo as regras abaixo.
# – A figura resultante deve ter um tamanho de 300x300.
# – Use cópias da figura 7b para os braços, pernas e tronco do boneco.
# – Não redimensione as imagens para criar o tronco e a cabeça.
# – Cada braço deve ter 75% do tamanho do tronco.
# – As pernas devem estar em um ângulo de 90º entre si e devem ter o dobro do tamanho dos braços.
# – Posicione o boneco no centro da imagem.


circulo = cv2.imread('7a.jpg',0)
barra = cv2.imread('7b.jpg',0)

# plt.figure(figsize=[15,15])
plt.subplot(121), plt.imshow(circulo, 'gray')
plt.subplot(122), plt.imshow(barra, 'gray')
plt.show()

width = barra.shape[1]
height = barra.shape[0]

# Imagem final
imgFinal = np.zeros((300,300), dtype=np.uint8)
imgFinal.fill(255)
# plt.imshow(cv2.cvtColor(imgFinal, cv2.COLOR_BGR2RGB));

print('imagens: ', circulo.shape, 'imagemFinal: ', imgFinal.shape)

# Rotacionando

rotacao90 = cv2.getRotationMatrix2D((50,50),90,1)
tronco = cv2.warpAffine(barra,rotacao30,(width,height), borderValue=255)
# plt.imshow(tronco, 'gray');

rotacao45 = cv2.getRotationMatrix2D((50,50),45,.75)
Lbraco = cv2.warpAffine(barra,rotacao45,(width,height), borderValue=255)
# plt.imshow(Lbraco, 'gray');

rotacaoM45 = cv2.getRotationMatrix2D((50,50),-45,.75)
Rbraco = cv2.warpAffine(barra,rotacaoM45,(width,height), borderValue=255)
plt.imshow(Rbraco, 'gray');


# Montando o boneco
# cabeça
imgFinal[0:100,100:200] = cv2.bitwise_and(imgFinal[0:100, 100:200], circulo)
# plt.imshow(cv2.cvtColor(imgFinal, cv2.COLOR_BGR2RGB));
# plt.imshow(imgFinal, 'gray');

# tronco
imgFinal[57:157, 100:200] = cv2.bitwise_and(imgFinal[57:157, 100:200], tronco)
# plt.imshow(imgFinal, 'gray');

# Lbraco
imgFinal[50:150, 80:180] = cv2.bitwise_and(imgFinal[50:150, 80:180], Lbraco)
# plt.imshow(imgFinal, 'gray');

# Rbraco
imgFinal[50:150, 120:220] = cv2.bitwise_and(imgFinal[50:150, 120:220], Rbraco)
# plt.imshow(imgFinal, 'gray');

# Lperna
imgFinal[120:220, 80:180] = cv2.bitwise_and(imgFinal[120:220, 80:180], Lbraco)
imgFinal[160:260, 40:140] = cv2.bitwise_and(imgFinal[160:260, 40:140], Lbraco)
# plt.imshow(imgFinal, 'gray');

# Rperna
imgFinal[120:220, 120:220] = cv2.bitwise_and(imgFinal[120:220, 120:220], Rbraco)
imgFinal[160:260, 160:260] = cv2.bitwise_and(imgFinal[160:260, 160:260], Rbraco)
plt.imshow(imgFinal, 'gray');


cv2.imwrite("Q7_Boneco.jpg", imgFinal)