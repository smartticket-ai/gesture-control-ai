import cv2

class Camera:
    def __init__(self):
        # Intentamos con el índice 0 (cámara por defecto)
        self.cap = cv2.VideoCapture(0)
        
        # Si no abre (o DroidCam está en otro índice), probamos con el 1 o 2
        if not self.cap.isOpened():
            print("Buscando cámara en índice 1 (DroidCam)...")
            self.cap = cv2.VideoCapture(1)
            
        if not self.cap.isOpened():
            print("Buscando cámara en índice 2...")
            self.cap = cv2.VideoCapture(2)

        if not self.cap.isOpened():
            print("⚠️ ERROR: No se detectó ninguna cámara. Asegúrate de que DroidCam esté conectado.")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Efecto espejo para que mover la mano derecha mueva el mouse a la derecha
        return cv2.flip(frame, 1)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
