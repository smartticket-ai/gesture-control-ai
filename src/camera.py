import cv2

class Camera:
    def __init__(self):
        # Intentamos buscar cámaras en los puertos 0, 1 y 2 (DroidCam suele usar el 1)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(2)
            
        if not self.cap.isOpened():
            print("⚠️ ERROR: No se detectó ninguna cámara física ni DroidCam.")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Efecto espejo para que mover la mano sea intuitivo
        return cv2.flip(frame, 1)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
