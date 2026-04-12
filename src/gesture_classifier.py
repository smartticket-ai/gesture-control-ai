import math

class GestureClassifier:
    
    def _get_fingers_up(self, hand):
        fingers = []
        for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
            if hand.landmark[tip].y < hand.landmark[pip].y:
                fingers.append(True)
            else:
                fingers.append(False)
        return fingers

    def classify(self, landmarks):
        if not landmarks:
            return None
        
        # --- MODO 2 MANOS (Volumen y Clic Derecho) ---
        if len(landmarks) >= 2:
            hand2 = landmarks[1] 
            f2 = self._get_fingers_up(hand2)
            
            es_puno_m2 = not any(f2)
            pulgar_arriba_m2 = es_puno_m2 and hand2.landmark[4].y < hand2.landmark[5].y - 0.04
            pulgar_abajo_m2 = es_puno_m2 and hand2.landmark[4].y > hand2.landmark[0].y + 0.04
            
            if pulgar_arriba_m2:
                return "VOL_UP"
            elif pulgar_abajo_m2:
                return "VOL_DOWN"
            elif es_puno_m2:
                return "RIGHT_CLICK"

        # --- MODO 1 MANO (Mouse Exclusivo) ---
        hand1 = landmarks[0]
        f1 = self._get_fingers_up(hand1)

        dist_pinza_medio = math.hypot(hand1.landmark[4].x - hand1.landmark[12].x, hand1.landmark[4].y - hand1.landmark[12].y)
        pinza_medio_cerrada = dist_pinza_medio < 0.08

        es_puno_m1 = not any(f1)

        # 1. CLICK IZQUIERDO NORMAL (Puño)
        if es_puno_m1:
            return "CLICK"

        # 2. MODO ARRASTRE (Pulgar + Medio)
        if pinza_medio_cerrada:
            return "DRAG"

        # 3. SCROLL (Índice y Medio levantados)
        if f1[0] and f1[1] and not f1[2] and not f1[3]:
            return "MODO_SCROLL"

        # 4. MODO MOUSE (Solo Índice levantado)
        if f1[0] and not any(f1[1:]): 
            return "MODO_MOUSE"
        
        return None