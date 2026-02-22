import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Efecto espejo para que el movimiento sea intuitivo
        return cv2.flip(frame, 1)

    def release(self):
        self.cap.release()
