import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self):
        # Usamos la estructura estándar de MediaPipe
        # mp.solutions es la forma correcta de acceder a los módulos dentro del venv
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        # Configuramos el detector de manos
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,        # False para que trate el video como una secuencia
            max_num_hands=1,               # Solo detectamos una mano para no confundir al mouse
            min_detection_confidence=0.7,   # Nivel de confianza para detectar la mano
            min_tracking_confidence=0.5     # Nivel de confianza para seguir el movimiento
        )

    def detect(self, frame):
        # OpenCV usa BGR, pero MediaPipe necesita RGB para procesar la IA
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesamos el frame para buscar las manos
        results = self.hands.process(image_rgb)
        
        # Si la IA encuentra una mano, dibujamos los puntos en el frame original
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Esto dibuja los 21 puntos y las líneas que los unen
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        # Devolvemos los puntos (landmarks) para que el controlador mueva el mouse
        return results.multi_hand_landmarks
