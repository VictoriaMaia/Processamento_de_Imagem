# Questão 3
# Considere a imagem 3 dividida em 4 quadrantes. Realize a equalização dos
# histogramas locais correspondentes aos quadrantes 2 e 3.

import cv2
import numpy as np
import matplotlib.pyplot as plt

img3 = cv2.imread('3.jpg', 0)
plt.imshow(img3, 'gray');

# img3.shape
# Imagem tem 683 por 1024
# Pegando a metade para dividir nos quadrantes fica arredondando 342 por 512

img3Quadrante2 = img3[:342 , 512:]
im_eq_quad2 = cv2.equalizeHist(img3Quadrante2)

plt.figure(figsize=[15,15])
plt.subplot(121),plt.imshow(img3Quadrante2, 'gray'),plt.title('Imagem quadrante 2')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(im_eq_quad2, 'gray'),plt.title('Equalizado')
plt.xticks([]), plt.yticks([])
plt.show()

img3Quadrante3 = img3[342: , :512]
im_eq_quad3 = cv2.equalizeHist(img3Quadrante3)

plt.figure(figsize=[15,15])
plt.subplot(121),plt.imshow(img3Quadrante3, 'gray'),plt.title('Imagem quadrante 3')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(im_eq_quad3, 'gray'),plt.title('Equalizado')
plt.xticks([]), plt.yticks([])
plt.show()


cv2.imwrite("Q3_Quadrante2.jpg", img3Quadrante2)
cv2.imwrite("Q3_Quadrante2_Equalizado.jpg", im_eq_quad2)
cv2.imwrite("Q3_Quadrante3.jpg", img3Quadrante3)
cv2.imwrite("Q3_Quadrante3_Equalizado.jpg", im_eq_quad3)