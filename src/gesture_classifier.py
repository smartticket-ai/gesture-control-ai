class GestureClassifier:
    def classify(self, landmarks):
        if not landmarks:
            return None
        
        hand = landmarks[0]
        fingers = []

        # Puntas de los dedos: 8(Índice), 12(Medio), 16(Anular), 20(Meñique)
        # Nudillos (para comparar altura): 6, 10, 14, 18
        for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
            # Si la punta está más arriba que el nudillo, el dedo está levantado
            if hand.landmark[tip].y < hand.landmark[pip].y:
                fingers.append(True)
            else:
                fingers.append(False)

        # Reglas de los gestos
        if all(fingers): return "MANO_ABIERTA"
        if fingers[0] and not any(fingers[1:]): return "MODO_MOUSE" # Solo índice
        if not any(fingers): return "PUÑO" # Todos abajo
        
        return None
