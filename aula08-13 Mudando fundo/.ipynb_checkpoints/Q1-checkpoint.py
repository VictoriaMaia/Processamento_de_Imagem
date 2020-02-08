import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread('imagens_prova/1.jpg')
img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

low_blue = np.array([10,60,100])
high_blue = np.array([90,120,255])
mask2 = cv2.inRange(img1_hsv, low_blue, high_blue)

low_green = np.array([20, 155, 45])
high_green = np.array([110, 255, 255])
mask = cv2.inRange(img1_hsv, low_green, high_green)

green = cv2.bitwise_and(img1, img1_hsv, mask=mask)
plt.imshow(green);

blue = cv2.bitwise_and(img1, img1_hsv, mask=mask2)
plt.imshow(blue);

final = cv2.add(green, blue)
plt.imshow(final);
