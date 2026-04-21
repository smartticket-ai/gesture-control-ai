import mediapipe as mp
import cv2
# Importaciones directas para evitar el error de AttributeError en Windows
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing

class HandTracker:
    def __init__(self):
        # Usamos las referencias directas que importamos arriba
        self.mp_hands = mp_hands
        self.mp_draw = mp_drawing
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,  # 2 para detectar el Modo Jefe
            min_detection_confidence=0.85, # Aumentado para evitar parpadeos
            min_tracking_confidence=0.80   # Aumentado para seguir la mano con firmeza
        )

    def detect(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        return results.multi_hand_landmarks