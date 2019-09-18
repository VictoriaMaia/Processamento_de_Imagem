# Questão 1
# Combine as imagens 1a e 1b e resolva a questão que aparece na imagem resultante.

import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread('1a.bmp')
img2 = cv2.imread('1b.bmp')

imgResult = cv2.bitwise_and(img1, img2)
plt.figure(figsize=[20,20])
plt.imshow(imgResult);

kernelA = np.float32([[-1,2,-1],[-1,2,-1],[-1,2,-1]])
kernelB = np.float32([[-1,-1,-1],[2,2,2],[-1,-1,-1]])
kernelC = np.float32([[-1,-1,2],[-1,2,-1],[2,-1,-1]])

img5 = cv2.imread('5.jpg')

customA = cv2.filter2D(img5, -1, kernelA)
customB = cv2.filter2D(img5, -1, kernelB)
customC = cv2.filter2D(img5, -1, kernelC)

plt.figure(figsize=[20,20])
plt.subplot(311),plt.imshow(customA),plt.title('Realça as colunas')
plt.xticks([]), plt.yticks([])
plt.subplot(312),plt.imshow(customB),plt.title('Realça as linhas')
plt.xticks([]), plt.yticks([])
plt.subplot(313),plt.imshow(customC),plt.title('Realça as bordas, tanto linhas como colunas')
plt.xticks([]), plt.yticks([])
plt.show()


cv2.imwrite("Q1_Combinacao_a_b.jpg", imgResult)
cv2.imwrite("Q1_Mascara_a.jpg", customA)
cv2.imwrite("Q1_Mascara_b.jpg", customB)
cv2.imwrite("Q1_Mascara_c.jpg", customC)


# A mascara A realça as colunas da imagem
# A mascara B realça as linhas da imagem
# A mascara C realça tanto as linhas como as colunas
