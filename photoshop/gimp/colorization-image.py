# -*- coding: utf-8 -*-
import numpy as np
import cv2

# Função para gerar a peleta de cores com um início e fim de cor definida pelo usuário
def palette( b1, g1, r1, b2, g2, r2):
    
    b = np.linspace(b1, b2, 256)
    g = np.linspace(g1, g2, 256)
    r = np.linspace(r1, r2, 256)
    
    p1 = np.tile( b.reshape(256,1), 256 )
    p2 = np.tile( g.reshape(256,1), 256 )
    p3 = np.tile( r.reshape(256,1), 256 )
       
    p1 = np.uint8(p1)
    p2 = np.uint8(p2)
    p3 = np.uint8(p3)
        
    palette = np.dstack( (np.dstack( (p1,p2) ), p3) )
            
    return palette

# Cor inicial
b1 = 56
g1 = 23
r1 = 87

# Cor final
b2 = 145
g2 = 201
r2 = 150

# Paleta de cores com as cores iniciais e finais definidas   
paleta = palette(b1, g1, r1, b2, g2, r2)

img = cv2.imread('a.jpg', 0)
out = np.zeros( (img.shape[0], img.shape[1], 3) )

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        out[i][j] = paleta [ img[i][j] ][0]

out = np.uint8(out)

# Mostrar uma imagem
cv2.imshow('Paleta de cores', paleta)
cv2.imshow('Imagem Original', img)
cv2.imshow('Imagem resultante', out)
cv2.waitKey(0)
