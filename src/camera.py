import cv2

class Camera:
    def __init__(self):
        # Selecciona la cámara predeterminada (0)
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Volteamos la imagen (efecto espejo) para que sea más natural
        return cv2.flip(frame, 1)

    def release(self):
        self.cap.release()
