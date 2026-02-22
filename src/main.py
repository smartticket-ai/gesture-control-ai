import sys
import os
import cv2

# Asegura que Python encuentre tus otros archivos sin errores
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera import Camera
from hand_tracker import HandTracker
from gesture_classifier import GestureClassifier
from controller import Controller

def main():
    cam = Camera()
    tracker = HandTracker()
    classifier = GestureClassifier()
    control = Controller()

    print("Iniciando sistema... Presiona 'q' en la ventana de video para salir.")

    while True:
        frame = cam.get_frame()
        # Si la cámara tarda en iniciar, evitamos que el programa explote
        if frame is None: 
            cv2.waitKey(100)
            continue

        landmarks = tracker.detect(frame)
        if landmarks:
            gesture = classifier.classify(landmarks)
            if gesture:
                # Mostrar el texto verde en pantalla
                cv2.putText(frame, f"Gesto: {gesture}", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                control.execute(gesture, landmarks)

        cv2.imshow("Gesture Control AI", frame)

        # Cerrar con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
