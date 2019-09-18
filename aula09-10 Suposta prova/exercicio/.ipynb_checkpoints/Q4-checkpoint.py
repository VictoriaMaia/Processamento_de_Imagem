# Questão 4
# Mostre como ficaria a imagem 4 caso as cores R,G e B fossem codificadas com apenas 4 bits cada.

# cv2.imwrite("Q2_.jpg", img)

import cv2
import numpy as np
import matplotlib.pyplot as plt

img4 = cv2.imread('4.jpg')
img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)

valores4bits = np.zeros(256)
for i in range(0, 256):
    valores4bits[i] = int(i/16)
    
r, g, b = cv2.split(img4)

newR = cv2.LUT(r, valores4bits)
newG = cv2.LUT(g, valores4bits)
newB = cv2.LUT(b, valores4bits)

new = cv2.merge((newR, newG, newB))

plt.hist(new.ravel(), 256, [0,256]);

normalized_image = cv2.normalize(new,None,0,256,cv2.NORM_MINMAX)

plt.hist(normalized_image.ravel(), 256, [0,256]);

cv2.imwrite("Q4_Imagem4bits.jpg", new)
cv2.imwrite("Q4_Imagem4bitsNormalizada.jpg", normalized_image)