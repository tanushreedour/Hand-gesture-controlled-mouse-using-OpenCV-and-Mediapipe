import cv2 
import mediapipe as mp
import pyautogui as auto 

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_hands_new = mp_hands.Hands(max_num_hands=2, model_complexity=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)

screen_width, screen_height = auto.size()

index_y = 0 

capture = cv2.VideoCapture(0)

class MouseClick:
    while True:
        isTrue, frame = capture.read()

        frame = cv2.flip(frame, 1)

        frame_height, frame_width, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = mp_hands_new.process(rgb_frame)
        hands = output.multi_hand_landmarks
        rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        if hands:
            for hand in hands:
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec = mp_drawing.DrawingSpec(color =(0, 0, 255), thickness = 4,  circle_radius = 2), connection_drawing_spec =  mp_drawing.DrawingSpec(color = (255, 255, 255), thickness = 2, circle_radius= 2))
                # mp_drawing.draw_landmarks(frame, hand)

                landmarks = hand.landmark


                for id, landmarks in enumerate(landmarks):
                    x = int(landmarks.x * frame_width)
                    y = int(landmarks.y * frame_height)

                    print(x, y)

                    if id == 8:
                        index_x = (screen_width / frame_width) * x
                        index_y = (screen_height / frame_height) * y
                        auto.moveTo(index_x, index_y)

                    if id == 12:
                        middle_x = (screen_width / frame_width) * x
                        middle_y = (screen_height / frame_height) * y

                        if abs(index_y - middle_y) < 20:
                            auto.click()
                            auto.sleep(1)
                                
        cv2.imshow('Mouse', frame)
    
        if cv2.waitKey(2) & 0xFF == 13:
            break

    capture.release()
    cv2.destroyAllWindows()

mouse_click = MouseClick()
