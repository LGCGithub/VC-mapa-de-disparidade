import cv2 as cv
import numpy as np
import os
import json

from math import ceil

barra = "" # tenho que testar em linux pra ver se funciona como eu espero que funcione

if os.name == 'nt':
    barra = "\\"
if os.name == 'posix':
    barra = "/"

directory_left = "left" + barra
directory_right = "right" + barra
directory_info = "info" + barra
directory_output = "depth_map" + barra

directory = os.listdir(directory_left)

sift = cv.SIFT_create()

for filename in directory:
    img_left = cv.imread(directory_left + filename)
    img_right = cv.imread(directory_right + filename)

    h = img_left.shape[0]
    w = img_left.shape[1]

    # Encontrar pontos de correspondência nas imagens
    kp1, des1 = sift.detectAndCompute(img_left, None)
    kp2, des2 = sift.detectAndCompute(img_right, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)

    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    pts1 = []
    pts2 = []

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    
    # Calcula a matriz fundamental
    F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_LMEDS)

    _, H1, H2 = cv.stereoRectifyUncalibrated(pts1, pts2, F, (h, w)) # retorna matrizes para transformação homográfica

    # Correção das matrizes homograficas (Translação)
    # Encontrar novo tamanho das imagens

    new_w = w
    new_h = h

    img_left_rectified = cv.warpPerspective(img_left, H1, (new_w, new_h)) # (w, h)
    img_right_rectified = cv.warpPerspective(img_right, H2, (new_w, new_h))

    cv.imwrite("rectified_left" + barra +  filename, img_left_rectified)
    cv.imwrite("rectified_right" + barra + filename, img_right_rectified)
    