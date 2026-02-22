class GestureClassifier:
    def classify(self, landmarks):
        if not landmarks:
            return None
        
        hand = landmarks[0]
        fingers = []

        # Puntos de las puntas de los dedos: Índice(8), Medio(12), Anular(16), Meñique(20)
        # Comparar con sus nudillos: 6, 10, 14, 18
        for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
            if hand.landmark[tip].y < hand.landmark[pip].y:
                fingers.append(True) # Dedo levantado
            else:
                fingers.append(False)

        # Lógica de gestos
        if all(fingers): return "MANO_ABIERTA"
        if fingers[0] and not any(fingers[1:]): return "MODO_MOUSE" # Solo índice
        if not any(fingers): return "PUÑO"
        
        return None
