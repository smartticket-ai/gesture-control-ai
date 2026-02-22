from camera import Camera
from hand_tracker import HandTracker
import cv2

def main():
    cam = Camera()
    tracker = HandTracker()

    print("Sistema iniciado. Presiona 'q' para salir.")

    while True:
        frame = cam.get_frame()
        if frame is None:
            break

        # Detectar mano y dibujar puntos
        landmarks = tracker.detect(frame)

        # Mostrar la ventana
        cv2.imshow("Control Gestual AI", frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
