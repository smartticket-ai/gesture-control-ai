import cv2

class Camera:
    def __init__(self, source=0):
        # Intentamos abrir el puerto indicado (por defecto 0)
        self.cap = cv2.VideoCapture(source)
        
        # Si el puerto 0 no funciona, intentamos el 1 como respaldo automático
        if not self.cap.isOpened():
            print(f"⚠️ Puerto {source} fallido, intentando con puerto 1...")
            self.cap = cv2.VideoCapture(1)
            
        # Verificación final
        if not self.cap.isOpened():
            print("❌ Error: No se pudo abrir ninguna cámara.")
            self.cap = None
        else:
            print("✅ Cámara conectada correctamente.")

    def get_frame(self):
        # Si self.cap es None, no intentamos leer
        if self.cap is None or not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Efecto espejo para una experiencia más natural
        return cv2.flip(frame, 1)

    def release(self):
        # Verificamos antes de liberar para evitar errores de referencia
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()