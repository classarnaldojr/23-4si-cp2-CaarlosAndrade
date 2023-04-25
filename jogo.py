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

last_move_player_1 = None
last_move_player_2 = None
winner = None  
scores = [0, 0]

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 1

# atribui jogadas mão direita (player_1) mão esquerda (player_2)
def setMove(hand, landmark):
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
        
# Definindo ganhador da partida 
def setMatchWinner(move_player_1, move_player_2):
        
        if move_player_1 == move_player_2:
            return 0
        elif move_player_1 == "papel":
            return 1 if move_player_2 == "pedra" else 2
        elif move_player_1 == "pedra":
            return 1 if move_player_2 == "tesoura" else 2
        elif move_player_1 == "tesoura":
            return 1 if move_player_2 == "papel" else 2

# capturando video do desafio
video_capture = cv2.VideoCapture("pedra-papel-tesoura.mp4")

while video_capture.isOpened():
    ret, video = video_capture.read()
    if not ret:
        break

    video = cv2.resize(video, (1000,600))
    h, w, _ = video.shape

    # processando o video usando mediapipe
    video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
    video.flags.writeable = False
    results = hands.process(video)
    video.flags.writeable = True
    video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)

    # recuperando os pontos para identificar mão no video
    hand_landmarks = results.multi_hand_landmarks
    if hand_landmarks and len(hand_landmarks) == 2:

        for landmarks in hand_landmarks:
            # capturando os pontos de uma mão
            landmark = landmarks.landmark

            if (landmark[0].x < landmark[12].x):
                # Mão esquerda
                player_1_hand_landmark = landmark
                move_player_1 = setMove(constants.LEFT, player_1_hand_landmark)
                cv2.putText(video, "Jogador 1", (50,70), font, font_scale, (0,0,0), thickness, cv2.LINE_AA)
                cv2.putText(video, move_player_1, (50,100), font, font_scale, (0,0,0), thickness, cv2.LINE_AA)
                
            else:
                # Mão direita
                player_2_hand_landmark = landmark
                move_player_2 = setMove(constants.RIGHT, player_2_hand_landmark)                
                cv2.putText(video, "Jogador 2", (w-200,70), font, font_scale, (0,0,0), thickness, cv2.LINE_AA)
                cv2.putText(video, move_player_2, (w-200,100), font, font_scale, (0,0,0), thickness, cv2.LINE_AA)    
        if (move_player_2 and move_player_1):
            if (move_player_1 != last_move_player_1 or move_player_2 != last_move_player_2):
                # armazena utlimo movimento
                last_move_player_1 = move_player_1
                last_move_player_2 = move_player_2
                # define ganhador
                winner = setMatchWinner(last_move_player_1, last_move_player_2)
                # atribui os pontos ao placar
                if winner == 1:
                    scores[0] += 1
                elif winner == 2:
                    scores[1] += 1

                score_text = f"{scores[0]} x {scores[1]}"   
                round_result = "Empate!" if winner == 0 else f"Jogador {winner} venceu!"
                    
            score_size, _ = cv2.getTextSize(score_text, font, font_scale, thickness)
            cv2.putText(video, "Placar", [(video.shape[1] - score_size[0]) // 2, 50], font, font_scale, (0,0,0), thickness, cv2.LINE_AA)
            cv2.putText(video, score_text, [(video.shape[1] - score_size[0]) // 2, 100], font, font_scale, (0,0,0), thickness, cv2.LINE_AA)

            result_size, _ = cv2.getTextSize(round_result, font, font_scale, thickness)
            cv2.putText(video, round_result, [(video.shape[1] - result_size[0]) // 2, video.shape[0] - result_size[1]], font, font_scale, (0,0,0), thickness, cv2.LINE_AA)

    cv2.imshow("Game - Rock, Paper, Scissors", video)

   # Esperar pela tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()