import cv2
import math
import numpy as np
import sys

def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()

def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix

def white_balance(img, percent):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100

    half_percent = percent / 200.0

    canais = cv2.split(img)

    canais_out = []
    for channel in canais:
        assert len(channel.shape) == 2
        
        # Percentuais baixo e altos com base no percentual de entrada
        h, w = channel.shape
        vec_size = w * h
        flat = channel.reshape(vec_size)

        assert len(flat.shape) == 1

        flat = np.sort(flat)

        n_cols = flat.shape[0]

        low_val  = flat[math.floor(n_cols * half_percent)]
        high_val = flat[math.ceil( n_cols * (1.0 - half_percent))]

        #print("Lowval: ", low_val)
        #print("Highval: ", high_val)
        
        thresholded = apply_threshold(channel, low_val, high_val)
        normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        canais_out.append(normalized)

    return cv2.merge(canais_out)

    img = cv2.imread('b.jpg')
    out = white_balance(img, 1)
    cv2.imshow("Original", img)
    cv2.imshow("Corrigida", out)
    cv2.waitKey(0)
