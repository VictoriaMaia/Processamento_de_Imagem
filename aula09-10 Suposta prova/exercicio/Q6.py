# Questão 6 
#  Faça a coloração da imagem 6 de forma que o resultado final seja uma imagem colorida da bandeira
# do Brasil

img6 = cv2.imread('6.jpeg')

plt.hist(img6.ravel(), 256, [0,256]);

imgFinal = img6.copy()

# azul
imgFinal[img6[:,:,0] < 80,0] = 0
imgFinal[img6[:,:,1] < 80,1] = 0
imgFinal[img6[:,:,2] < 80,2] = 100

# verde 
imgFinal[(img6[:,:,0] < 110) & (img6[:,:,0] > 80),0] = 0
imgFinal[(img6[:,:,0] < 110) & (img6[:,:,0] > 80),1] = 100
imgFinal[(img6[:,:,0] < 110) & (img6[:,:,0] > 80),2] = 0

# amarelo
imgFinal[(img6[:,:,0] < 240) & (img6[:,:,0] > 230),0] = 255
imgFinal[(img6[:,:,0] < 240) & (img6[:,:,0] > 230),1] = 255
imgFinal[(img6[:,:,0] < 240) & (img6[:,:,0] > 230),2] = 0

# branco
imgFinal[img6[:,:,0] > 240,0] = 255
imgFinal[img6[:,:,1] > 240,1] = 255
imgFinal[img6[:,:,2] > 240,2] = 255


plt.figure(figsize=[15,15])
plt.subplot(121), plt.imshow(imgFinal, 'gray')
plt.subplot(122), plt.imshow(img6, 'gray')
plt.show()

imgFinal = cv2.cvtColor(imgFinal, cv2.COLOR_BGR2RGB)
cv2.imwrite("Q6_bandeira_colorida.jpg", imgFinal)