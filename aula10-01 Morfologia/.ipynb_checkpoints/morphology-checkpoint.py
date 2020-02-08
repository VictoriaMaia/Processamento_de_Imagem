import sys
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


#abre imagem
filename = sys.argv[1]
img = cv.imread(filename,0)

#elemento estruturante
elem_type = cv.MORPH_RECT
#elem_type = cv.MORPH_CROSS
#elem_type = cv.MORPH_ELLIPSE
element = cv.getStructuringElement(elem_type, (3, 3))

#erosao #min
erosion_dst = cv.erode(img, element)

#dilatacao #max
dilatation_dst = cv.dilate(img, element)

#borda
borda1 = cv.subtract(img,erosion_dst)
borda2 = cv.subtract(dilatation_dst,img)

cv.imwrite("borda1.jpg",borda1)
cv.imwrite("borda2.jpg",borda2)
#mostra imagens
plt.subplot(221),plt.imshow(erosion_dst,cmap = 'gray')
plt.subplot(222),plt.imshow(dilatation_dst,cmap = 'gray')
plt.subplot(223),plt.imshow(borda1,cmap = 'gray')
plt.subplot(224),plt.imshow(borda2,cmap = 'gray')

plt.show()


