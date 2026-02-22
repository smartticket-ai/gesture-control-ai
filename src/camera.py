import cv2

class Camera:
    def __init__(self):
        # DroidCam suele aparecer en el índice 0, 1 o 2.
        # Probamos el 0 primero
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            # Si falla el 0, intentamos con el 1 (muy común para DroidCam)
            self.cap = cv2.VideoCapture(1)
            
        if not self.cap.isOpened():
            print("⚠️ No se detectó cámara en 0 o 1. Verificando DroidCam...")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Volteo horizontal para que sea natural al mover la mano
        return cv2.flip(frame, 1)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
