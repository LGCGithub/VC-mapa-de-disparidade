import cv2 as cv
import numpy as np
import os
import json

barra = "" # tenho que testar em linux pra ver se funciona como eu espero que funcione

if os.name == 'nt':
    barra = "\\"
if os.name == 'posix':
    barra = "/"

directory_left = "left" + barra
directory_right = "right" + barra
directory_info = "info" + barra
directory_output = "depth_map" + barra

left_imgs = []
right_imgs = []
info_imgs = []

directory = os.listdir(directory_left)

for filename in directory:
    left_imgs.append(cv.imread(directory_left + filename, 0))
    right_imgs.append(cv.imread(directory_right + filename, 0))
    try:
        info_imgs.append(json.load(open(directory_info + filename)))
    except:
        info_imgs.append({})

stereo = cv.StereoBM_create(numDisparities=256, blockSize=9)

# branco = perto
# preto = longe

for index in range(0, len(left_imgs)):
    # Calcula o mapa de disparidade
    disparity = stereo.compute(left_imgs[index], right_imgs[index])

    # Trabalhar com float é melhor
    disparity = disparity.astype(np.float32) / 255.0

    # Normaliza o mapa de disparidade
    disparity = cv.normalize(src=disparity, dst=None, alpha=0.0, beta=1.0, norm_type=cv.NORM_MINMAX)

    # Tentativa de deixar o mapa mais suave, borrando
    #disparity = cv.GaussianBlur(disparity, ksize=(21, 21), sigmaX=0)

    cv.imshow("left", left_imgs[index])
    cv.imshow("right", right_imgs[index])
    cv.imshow("disparity map", disparity)
    
    cv.waitKey(0)
