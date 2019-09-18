# Questão 2
#  Escolha e aplique uma tranformação gamma que resulte em uma imagem 2 mais amarelada. Indique
# os parâmetros escolhidos e os passos realizados

img2 = cv2.imread('2.jpg')
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# Foi feito um split para separar os canais
imgB, imgG, imgR = cv2.split(img2)

# Cada canal foi feito um ganho diferente escolhido de forma manual empírica

# Canal R foi dado um ganho com gamma = 5
imgR = np.array(255*(imgR/255)**5,dtype='uint8')
# Canal G foi dado um ganho com gamma = 0.7
imgG = np.array(255*(imgG/255)**0.7,dtype='uint8')
# Canal B foi dado um ganho com gamma = 0.05
imgB = np.array(255*(imgB/255)**0.05,dtype='uint8')

# Após o ganho foi feito um merge para poder juntar os canais e formar a imagem final
imgAmarelada = cv2.merge((imgR, imgG, imgB))



# !!!!! AVISO !!!!! 
# A imagem mostrada na função plt.imshow esta azulada, 
# mas quando a imagem é salva na função cv2.imwrite ela fica amarelada

# plt.figure(figsize=[20,20])
# plt.subplot(121),plt.imshow(img2),plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(imgAmarelada),plt.title('Amarelada')
# plt.xticks([]), plt.yticks([])
# plt.show()

cv2.imwrite("Q2_amarelada.jpg", imgAmarelada)