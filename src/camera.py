import cv2

class Camera:
    def __init__(self):
        self.cap = None
        
        # Vamos a probar los puertos del 0 al 4 automáticamente
        for i in range(5):
            print(f"🔍 Probando cámara en el puerto {i}...")
            cap = cv2.VideoCapture(i)
            
            if cap.isOpened():
                # Leemos un frame para confirmar que la cámara realmente da imagen
                ret, frame = cap.read()
                if ret:
                    print(f"✅ ¡Cámara detectada y funcionando en el puerto {i}!")
                    self.cap = cap
                    break # Detenemos la búsqueda, ya encontramos la buena
                else:
                    cap.release()
                    
        if self.cap is None or not self.cap.isOpened():
            print("⚠️ ERROR: No se pudo conectar a ninguna cámara válida. Revisa DroidCam.")

    def get_frame(self):
        if self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Efecto espejo para que el movimiento de tu mano sea natural
        return cv2.flip(frame, 1)

    def release(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
