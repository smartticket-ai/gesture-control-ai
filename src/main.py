from .camera import Camera
from .hand_tracker import HandTracker
from .gesture_classifier import GestureClassifier
from .controller import Controller
import cv2

def main():
    cam = Camera()
    tracker = HandTracker()
    classifier = GestureClassifier()
    control = Controller()

    while True:
        frame = cam.get_frame()
        if frame is None: break

        landmarks = tracker.detect(frame)
        
        if landmarks:
            gesture = classifier.classify(landmarks)
            if gesture:
                # Dibujamos el nombre del gesto en la pantalla
                cv2.putText(frame, f"Gesto: {gesture}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Ejecutamos la acción en el PC
                control.execute(gesture, landmarks)

        cv2.imshow("Sistema de Control Gestual", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
