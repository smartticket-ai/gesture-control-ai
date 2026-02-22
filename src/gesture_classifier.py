class GestureClassifier:
    def __init__(self):
        pass

    def classify(self, landmarks):
        if not landmarks:
            return None
        
        # Obtenemos los puntos clave (Landmarks) de la primera mano detectada
        hand = landmarks[0]
        
        # Lógica simple: Comparar la altura de las puntas de los dedos con sus nudillos
        # Puntos MediaPipe: Índice (8), Medio (12), Anular (16), Meñique (20)
        # Sus nudillos base: Índice (5), Medio (9), Anular (13), Meñique (17)
        
        fingers_up = []
        
        # Dedos: Índice, Medio, Anular, Meñique (coordenada Y disminuye al subir)
        for tip, base in zip([8, 12, 16, 20], [5, 9, 13, 17]):
            if hand.landmark[tip].y < hand.landmark[base].y:
                fingers_up.append(True)
            else:
                fingers_up.append(False)
        
        # Definición de gestos básicos
        if all(fingers_up):
            return "MANO_ABIERTA"  # Todos los dedos arriba
        if fingers_up[0] and not any(fingers_up[1:]):
            return "SOLO_INDICE"   # Solo el índice arriba (Modo Mouse)
        if not any(fingers_up):
            return "PUÑO"          # Ningún dedo arriba
            
        return None
