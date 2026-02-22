import cv2

class Camera:
    def __init__(self):
        # ¡Adiós Animaze! Forzamos el puerto 1 directamente.
        # ⚠️ ATENCIÓN: Si sigue saliendo Animaze, cambia este 1 por un 2, o un 3.
        self.cap = cv2.VideoCapture(1) 
        
        if not self.cap.isOpened():
            print("⚠️ No hay cámara en este puerto.")

    def get_frame(self):
        if self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Efecto espejo
        return cv2.flip(frame, 1)

    def release(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
