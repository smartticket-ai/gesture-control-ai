import math

class GestureClassifier:
    def classify(self, landmarks):
        if not landmarks:
            return None
        
        # --- CLICK DERECHO (Mostrar las dos manos) ---
        if len(landmarks) == 2:
            return "RIGHT_CLICK"
            
        hand = landmarks[0]
        fingers = []

        # 1. Analizar dedos (Índice a Meñique)
        for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
            if hand.landmark[tip].y < hand.landmark[pip].y:
                fingers.append(True)
            else:
                fingers.append(False)

        # 2. Distancias para las pinzas
        # Pinza Índice (Para Clic Normal)
        dist_pinza_indice = math.hypot(hand.landmark[4].x - hand.landmark[8].x, hand.landmark[4].y - hand.landmark[8].y)
        pinza_indice_cerrada = dist_pinza_indice < 0.08  
        
        # Pinza Medio (Para Arrastrar)
        dist_pinza_medio = math.hypot(hand.landmark[4].x - hand.landmark[12].x, hand.landmark[4].y - hand.landmark[12].y)
        pinza_medio_cerrada = dist_pinza_medio < 0.08

        # 3. Lógica de Volumen
        indice_y_medio_bajados = not fingers[0] and not fingers[1]
        pulgar_arriba = hand.landmark[4].y < hand.landmark[5].y - 0.02
        pulgar_abajo = hand.landmark[4].y > hand.landmark[0].y + 0.02

        # --- REGLAS DE GESTOS ---
        
        # 1. CLICK NORMAL (Pulgar + Índice)
        if pinza_indice_cerrada:
            return "CLICK"
            
        # 2. MODO ARRASTRE (Pulgar + Medio)
        if pinza_medio_cerrada:
            return "DRAG"

        # 3. GESTOS DE VOLUMEN
        if indice_y_medio_bajados:
            if pulgar_arriba:
                return "VOL_UP"
            elif pulgar_abajo:
                return "VOL_DOWN"

        # 4. SCROLL (Índice y Medio levantados, Anular y Meñique bajados)
        if fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
            return "MODO_SCROLL"

        # 5. MOVIMIENTO DEL MOUSE NORMAL (Solo Índice levantado)
        if fingers[0] and not any(fingers[1:]): 
            return "MODO_MOUSE"
        
        return None