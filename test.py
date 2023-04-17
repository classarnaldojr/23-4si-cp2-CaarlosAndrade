import cv2
import mediapipe as mp

# video = cv2.VideoCapture("pedra-papel-tesoura.mp4") ### suport video mp4. .avi  .mkv
video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1, model_complexity=0)
mpDraw = mp.solutions.drawing_utils

while True:

    check,img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=5) 
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h, w,_ = img.shape
    pontos  = []
    if handsPoints:
        for points in handsPoints:
            # print(points)
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                # convertendo pontos em pixels e encontrando ele na imagem gerada pela web can
                cx,cy = int(cord.x * w), int(cord.y * h)
                # cv2.putText(img, str(id), (cx, cy+15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 2)
                pontos.append((cx,cy))

        dedos = [8,12,16,20]
        contador =0
        if points:
            for x in dedos:
                if pontos[x][1] < pontos[x-2][1]:
                    contador +=1

        print(contador)

    cv2.imshow("Video", cv2.resize(img ,(1000, 600)))

    key = cv2.waitKey(20)
    if key == 27:
        break


cv2.destroyWindow("original")
video.release()