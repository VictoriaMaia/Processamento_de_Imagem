import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_mat_energy(im):
    
    ddepth = cv2.CV_32F
    x = cv2.Sobel(im, ddepth, 1, 0)
    y = cv2.Sobel(im, ddepth, 0, 1)
    x_abs = cv2.convertScaleAbs(x)
    y_abs = cv2.convertScaleAbs(y)
    mat_energy = cv2.addWeighted(x_abs, 0.5, y_abs, 0.5, 0)
    
    return mat_energy

def rotacionar(image, angulo):
    altura = image.shape[0]
    largura = image.shape[1]
    
    x_center = int(largura/2)
    y_center = int(altura/2)
    
    M = cv2.getRotationMatrix2D((x_center, y_center), angulo, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    nW = int((altura * sin) + (largura * cos))
    nH = int((altura * cos) + (largura * sin))
 
    M[0, 2] += (nW / 2) - x_center
    M[1, 2] += (nH / 2) - y_center
 
    return cv2.warpAffine(image, M, (nW, nH))

def seam_dimimuir(imagem, num_iteracoes, vira=0):

    img = imagem.copy()
    
    if vira == 1:
        img = rotacionar(img, 90)
        
    for s in range(num_iteracoes):
        altura = img.shape[0]
        largura = img.shape[1]
        mat_energy = get_mat_energy(img).astype('uint16')

        seam = np.zeros(img.shape).astype('uint16')

        seam = mat_energy

        for i in range(1, altura, 1):
            for j in range(0, largura, 1):
                if(j == 0):
                    seam[i,j] += np.min((seam[i-1, j], seam[i-1, j+1]))
                elif(j == largura-1):
                    seam[i,j] += np.min((seam[i-1, j-1], seam[i-1, j]))
                else:
                    seam[i,j] += np.min((seam[i-1, j-1], seam[i-1, j], seam[i-1, j+1]))

        indice_menor = np.argmin(seam[altura-1, :])

        for i in range(altura-1, -1, -1):
            img[i, indice_menor:largura-2] = img[i, indice_menor+1:largura-1]
            if indice_menor == 0:
                indice_menor = np.argmin((seam[i-1, indice_menor], seam[i-1, indice_menor+1]))
            elif indice_menor == largura-1:
                indice_menor = (indice_menor-1) + np.argmin((seam[i-1, indice_menor-1], seam[i-1, indice_menor]))
            else:
                indice_menor = (indice_menor-1) + np.argmin((seam[i-1, indice_menor-1], seam[i-1, indice_menor], seam[i-1, indice_menor+1]))

        img = img[:, :-1]
        
    if vira == 1:
        img = rotacionar(img, -90)
    
    return img

def nada(x):
    return

def executar(x):
    new_largura = cv2.getTrackbarPos('largura','image')
    new_altura = cv2.getTrackbarPos('altura','image')
    print(new_altura, new_largura)
    new = imagem.copy()

    if new_altura < imagem.shape[0]:
        # print("tenho que diminuir na altura", imagem.shape[0]-new_altura)
        interacoes = imagem.shape[0]-new_altura
        new = seam_dimimuir(new, interacoes, 1)
    
    # if new_altura > imagem.shape[0]:
        # print("aumentando altura")
    
    if new_largura < imagem.shape[1]:
        # print("tenho que diminuir na largura", imagem.shape[1]-new_largura)
        interacoes = imagem.shape[1]-new_largura
        new = seam_dimimuir(new, interacoes)        
        

    # if interacoes_largura > imagem.shape[1]:
    #     print("aumentando largura")
    cv2.imshow('image', new)
    return



filename = sys.argv[1]
print("Selecione a altura e largura que deseja e mova a barra executar. Espere um pouco e verá o resultado")
print("Esse programa só diminui a imagem!!")

imagem = cv2.imread(filename, 0)

altura = imagem.shape[0]
largura = imagem.shape[1]

dobro_altura = imagem.shape[0]*2
dobro_largura = imagem.shape[1]*2


cv2.namedWindow('image',cv2.WINDOW_NORMAL)

cv2.createTrackbar('altura','image', altura, dobro_altura, nada)
cv2.createTrackbar('largura','image', largura, dobro_largura, nada)
cv2.createTrackbar('executar','image', 0, 1, executar)

cv2.imshow('image',imagem)


while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows()