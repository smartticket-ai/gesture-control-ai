import math

class GestureClassifier:
    def __init__(self):
        # Reducimos a 3 para que sea más rápido al reaccionar
        self.gesture_history = []
        self.history_size = 3 

    def _get_fingers_up(self, hand):
        fingers = []
        for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
            fingers.append(hand.landmark[tip].y < hand.landmark[pip].y)
        return fingers

    def classify(self, landmarks):
        if not landmarks:
            self.gesture_history = []
            return None
        
        current_gesture = None
        
        # --- MODO 2 MANOS (Volumen y Clic Derecho) ---
        if len(landmarks) >= 2:
            hand2 = landmarks[1] 
            f2 = self._get_fingers_up(hand2)
            
            # Es puño si los 4 dedos principales están cerrados
            es_puno_m2 = not any(f2)
            
            if es_puno_m2:
                # Calculamos distancia del pulgar al nudillo del índice
                # Bajamos el umbral a 0.04 para que sea más sensible
                dist_pulgar = math.hypot(hand2.landmark[4].x - hand2.landmark[5].x, 
                                         hand2.landmark[4].y - hand2.landmark[5].y)
                
                # Coordenadas clave para comparar
                punta_pulgar_y = hand2.landmark[4].y
                nudillo_indice_y = hand2.landmark[5].y
                base_pulgar_y = hand2.landmark[2].y

                # VOL UP: Pulgar claramente arriba del nudillo
                if dist_pulgar > 0.04 and punta_pulgar_y < nudillo_indice_y - 0.02:
                    current_gesture = "VOL_UP"
                
                # VOL DOWN: Pulgar claramente abajo de su propia base
                elif dist_pulgar > 0.04 and punta_pulgar_y > base_pulgar_y + 0.02:
                    current_gesture = "VOL_DOWN"
                
                # Si es puño cerrado y el pulgar no está ni arriba ni abajo
                else:
                    current_gesture = "RIGHT_CLICK"

        # --- MODO 1 MANO (Mouse Exclusivo) ---
        if not current_gesture: 
            hand1 = landmarks[0]
            f1 = self._get_fingers_up(hand1)
            dist_pinza = math.hypot(hand1.landmark[4].x - hand1.landmark[12].x, hand1.landmark[4].y - hand1.landmark[12].y)
            
            if not any(f1): current_gesture = "CLICK"
            elif dist_pinza < 0.08: current_gesture = "DRAG"
            elif f1[0] and f1[1] and not f1[2] and not f1[3]: current_gesture = "MODO_SCROLL"
            elif f1[0] and not any(f1[1:]): current_gesture = "MODO_MOUSE"

        # --- SISTEMA DE ESTABILIZACIÓN ---
        self.gesture_history.append(current_gesture)
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
            
        if len(self.gesture_history) == self.history_size and all(g == current_gesture for g in self.gesture_history):
            return current_gesture
            
        return None