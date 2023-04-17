import cv2
import os, sys, os.path
import numpy as np
import mediapipe as mp

def imagem_webcan(img):
    # convertendo a imagem para ficar cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detector de bordas na imagem
    # "cv2.CV_8U" indica o tipo de dados da imagem resultante. 
    # E o parâmetro "ksize=5" é o tamanho do kernel utilizado na convolução para a aplicação do operador.
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=5)

    # faz a binarizacao de uma imagem
    # edges é a que será imagem binarizada
    # O valor "100" é o limite de intensidade de pixel
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    return mask
video_capture = cv2.VideoCapture(0)

# video_capture = cv2.VideoCapture("pedra-papel-tesoura.mp4") ### suport video mp4. .avi  .mkv

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands = 1)
mpDraw = mp.solutions.drawing_utils

# verifica se existe video
if video_capture.isOpened():
    rval, frame = video_capture.read()
else:
    rval = False

# le cada frame da imagem e exibe em uma tela
while rval:

    img = imagem_webcan(frame)

    result = Hand.process(img)

    handsPoints = result.multi_hand_landmarks
    if handsPoints:
        for points in handsPoints:
            print(points)

    # (frame) = varivel original do frame

    # exibe o frame da imagem enquanto rval for true
    cv2.imshow("preview", cv2.resize(img, (1000,600)))
    cv2.imshow("original", cv2.resize(frame, (1000,600)))

    rval, frame = video_capture.read()
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyWindow("original")
video_capture.release()