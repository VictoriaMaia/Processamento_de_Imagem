from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2

image = cv2.imread("d.jpg")

#Aplicando o filtro de deslocamento médio
shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
cv2.imshow("Imagem original", image)

# convert the mean shift image to grayscale, then apply
# Otsu's thresholding
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imshow("Threshold", thresh)

#Calculando distância euclidiana para cada pixel
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=20,
	labels=thresh)

markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("[INFO] {} segmentos encontrados".format(len(np.unique(labels)) - 1))

for label in np.unique(labels):
	if label == 0:
		continue

	mask = np.zeros(gray.shape, dtype="uint8")
	mask[labels == label] = 255

	# Detectando os contornos
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key=cv2.contourArea)

	# Circundando o objeto
	#((x, y), r) = cv2.minEnclosingCircle(c)
	image = cv2.drawContours(image, cnts, -1, (0, 255, 0), 3)
	#cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
	
	#cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
		#cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow("Imagem final", image)
cv2.waitKey(0)
