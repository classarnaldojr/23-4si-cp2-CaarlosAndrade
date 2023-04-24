import cv2
import mediapipe as mp
import constants

# instanciando variaveis
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0, 
    min_detection_confidence=0.3, 
    min_tracking_confidence=0.3,
    max_num_hands=2
)

move_player_1 = ""
move_player_2 = ""

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1

def setMove(hand):
    if hand == constants.LEFT:
        if (landmark[6].x < landmark[8].x) and (landmark[10].x < landmark[12].x) and (landmark[14].x < landmark[16].x):
            return constants.PAPEL
        elif (landmark[6].x < landmark[8].x) and (landmark[10].x < landmark[12].x):
            return constants.TESOURA
        elif (landmark[6].x > landmark[8].x):
            return constants.PEDRA
    elif hand == constants.RIGHT:
        if (landmark[6].x > landmark[8].x) and (landmark[10].x > landmark[12].x) and (landmark[14].x > landmark[16].x):
            return constants.PAPEL
        elif (landmark[6].x > landmark[8].x) and (landmark[10].x > landmark[12].x):
            return constants.TESOURA
        elif (landmark[6].x < landmark[8].x):
            return constants.PEDRA

def setMatchWinner(move_player_1, move_player_2):
    if move_player_1 == move_player_2:
        return "Empate!"
    elif move_player_1 == "pedra" and move_player_2 == "tesoura":
        return "Jogador 1"
    elif move_player_1 == "papel" and move_player_2 == "pedra":
        return "Jogador 1"
    elif move_player_1 == "tesoura" and move_player_2 == "papel":
        return "Jogador 1"
    else:
        return "Jogador 2"
  


# capturando video do desafio
video_capture = cv2.VideoCapture("pedra-papel-tesoura.mp4")

# le cada frame da imagem e exibe em uma tela
while video_capture.isOpened():
    ret, video = video_capture.read()
    video = cv2.resize(video, (1000,600))
    h, w, _ = video.shape
    if not ret:
        break

    video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
    video.flags.writeable = False
    results = hands.process(video)
    video.flags.writeable = True
    video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)

    hand_landmarks = results.multi_hand_landmarks
    if hand_landmarks and len(hand_landmarks) == 2:

        for landmarks in hand_landmarks:
            # acessa o landmark 0 da mão atual
            landmark = landmarks.landmark

            # para onde está apontada a mão ?
            if (landmark[0].x < landmark[12].x):
                # Mão esquerda
                move_player_1 = setMove(constants.LEFT)
                cv2.putText(video, "Jogador 1", (50,70), font, font_scale, (0,0,0), 2, cv2.LINE_AA)
                cv2.putText(video, move_player_1, (50,100), font, font_scale, (0,0,0), 2, cv2.LINE_AA)
                
            else:
                # Mão direita
                move_player_2 = setMove(constants.RIGHT)                
                cv2.putText(video, "Jogador 2", (w-200,70), font, font_scale, (0,0,0), 2, cv2.LINE_AA)
                cv2.putText(video, move_player_2, (w-200,100), font, font_scale, (0,0,0), 2, cv2.LINE_AA)    

            winner = setMatchWinner(move_player_1, move_player_2)
            cv2.getTextSize(winner, font, fontScale=font_scale, thickness=1)[0]
            cv2.putText(video, f'Resultado: {winner}', (320,(h-100)), font, font_scale, (0,0,0), 2, cv2.LINE_AA)
            
            
    cv2.imshow("Game - Rock, Paper, Scissors", video)

   # Esperar pela tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()