import sys
import os
import cv2

# ESTO SOLUCIONA TUS ERRORES DE IMPORTACIÓN
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from camera import Camera
from hand_tracker import HandTracker
from gesture_classifier import GestureClassifier
from controller import Controller

def main():
    cam = Camera()
    tracker = HandTracker()
    classifier = GestureClassifier()
    control = Controller()

    print("Iniciando sistema... Presiona 'q' para salir.")

    while True:
        frame = cam.get_frame()
        if frame is None: break

        landmarks = tracker.detect(frame)
        if landmarks:
            gesture = classifier.classify(landmarks)
            if gesture:
                cv2.putText(frame, gesture, (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                control.execute(gesture, landmarks)

        cv2.imshow("Gesture Control AI", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
