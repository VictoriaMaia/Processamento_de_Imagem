import cv2
import numpy as np

def get8n(x, y, shape):
    out = []
    x_max = shape[1]-1
    y_max = shape[0]-1

    #top left
    x_out = min(max(x-1,0), x_max)
    y_out = min(max(y-1,0), y_max)
    out.append((x_out, y_out))

    #top center
    x_out = x
    y_out = min(max(y-1,0), y_max)
    out.append((x_out, y_out))

    #top right
    x_out = min(max(x+1,0), x_max)
    y_out = min(max(y-1,0), y_max)
    out.append((x_out, y_out))

    #left
    x_out = min(max(x-1,0), x_max)
    y_out = y
    out.append((x_out, y_out))

    #right
    x_out = min(max(x+1,0), x_max)
    y_out = y
    out.append((x_out, y_out))

    #bottom left
    x_out = min(max(x-1,0), x_max)
    y_out = min(max(y+1,0), y_max)
    out.append((x_out, y_out))

    #bottom center
    x_out = x
    y_out = min(max(y+1,0), y_max)
    out.append((x_out, y_out))

    #bottom right
    x_out = min(max(x+1,0), x_max)
    y_out = min(max(y+1,0), y_max)
    out.append((x_out, y_out))

    return out

def region_growing(img, seed):
    list = []
    img_f = np.zeros_like(img)
    list.append((seed[0], seed[1]))
    processed = []
    while(len(list) > 0):
        pix = list[0]
        img_f[pix[0], pix[1]] = 255
        for coord in get8n(pix[0], pix[1], img.shape):
            if img[coord[0], coord[1]] != 0:
                img_f[coord[0], coord[1]] = 255
                if not coord in processed:
                    list.append(coord)
                processed.append(coord)
        list.pop(0)
    return img_f

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('Seed: ' + str(x) + ', ' + str(y), img[y,x])
        clicks.append((y,x))


clicks = []
image = cv2.imread('moedas.jpg', 0)

ret, img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

cv2.namedWindow('Imagem original')
cv2.setMouseCallback('Imagem original', on_mouse, 0, )
cv2.imshow('Imagem original', img)
cv2.waitKey()

seed = clicks[-1]
out = region_growing(img, seed)

cv2.imshow('Imagem final', out)
cv2.waitKey()
cv2.destroyAllWindows()

while(1):
    k = cv2.waitKey(0) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()