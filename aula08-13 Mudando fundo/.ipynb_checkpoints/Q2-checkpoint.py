import cv2
import numpy as np
import matplotlib.pyplot as plt


img3 = cv2.imread('imagens_prova/3.jpg', 0)

width = img3.shape[1]
height = img3.shape[0]

rotacao90 = cv2.getRotationMatrix2D((238,236),90,1)
img3_rotacionada90 = cv2.warpAffine(img3,rotacao90,(width,height), borderValue=255)

img3_escala2x = cv2.resize(img3,(width*2,height*2))

M_translation = np.float32([[1,0,100],[0,1,50]])
M_scaling = np.float32([[.8,0,1], [0,.9,1]])

img3_transladada = cv2.warpAffine(img3,M_scaling,(width,height))
img3_transladada = cv2.warpAffine(img3_transladada, M_translation, (width,height))

fft_img3 = np.fft.fft2(img3)
fft_img3_shift = np.fft.fftshift(fft_img3)

fft_img3_rot90 = np.fft.fft2(img3_rotacionada90)
fft_img3_rot90_shift = np.fft.fftshift(fft_img3_rot90)

fft_img3_esc = np.fft.fft2(img3_escala2x)
fft_img3_esc_shift = np.fft.fftshift(fft_img3_esc)

fft_img3_tran = np.fft.fft2(img3_transladada)
fft_img3_tran_shift = np.fft.fftshift(fft_img3_tran)

plt.figure(figsize=[10,10])
plt.subplot(221), plt.imshow(np.log(np.abs(fft_img3_shift)+1), 'gray'), plt.title('Original')
plt.subplot(222), plt.imshow(np.log(np.abs(fft_img3_rot90_shift)+1), 'gray'),plt.title('Rotacionada')
plt.subplot(223), plt.imshow(np.log(np.abs(fft_img3_esc_shift)+1), 'gray'), plt.title('Escalonada')
plt.subplot(224), plt.imshow(np.log(np.abs(fft_img3_tran_shift)+1), 'gray'),plt.title('Transladada')
plt.show()

print("As baixas frequências da imagem rotacionada mudaram de posição e na imagem escalonada tem um aumento de frequencias altas")