import sys
import os
import cv2
import time
from collections import deque
from statistics import mode

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera import Camera
from hand_tracker import HandTracker
from gesture_classifier import GestureClassifier
from controller import Controller
from camera_tracker import CameraTracker  # 🌟 IMPORTAMOS EL NUEVO TRACKER

def main():
    cam = Camera()
    tracker = HandTracker()
    classifier = GestureClassifier()
    control = Controller()
    cam_tracker = CameraTracker()  # 🌟 INICIALIZAMOS EL AUTO-FRAMING

    # Variables solo para el volumen
    last_volume_action_time = 0
    volume_cooldown = 0.2  
    
    gesture_buffer = deque(maxlen=7)

    print("Iniciando sistema... Presiona 'q' en la ventana de video para salir.")

    while True:
        frame = cam.get_frame()
        
        if frame is None: 
            cv2.waitKey(100)
            continue

        landmarks = tracker.detect(frame)
        stable_gesture = None
        color = (0, 255, 0) # Color por defecto para el texto
        
        if landmarks:
            raw_gesture = classifier.classify(landmarks)
            
            if raw_gesture:
                gesture_buffer.append(raw_gesture)
                stable_gesture = mode(gesture_buffer)
            else:
                gesture_buffer.clear()
                
            if stable_gesture:
                current_time = time.time()
                
                # Lógica del Volumen
                if stable_gesture in ["VOL_UP", "VOL_DOWN"]:
                    if current_time - last_volume_action_time > volume_cooldown:
                        control.execute(stable_gesture, landmarks)
                        last_volume_action_time = current_time
                        color = (255, 0, 0)
                    else:
                        color = (0, 255, 0)
                        
                # Lógica del clic
                elif stable_gesture == "CLICK":
                    control.execute(stable_gesture, landmarks)
                    color = (0, 0, 255) # Rojo
                        
                # Otros gestos
                else:
                    control.execute(stable_gesture, landmarks)
                    color = (0, 255, 0)

        else:
            gesture_buffer.clear()

        # 🌟 MAGIA DEL AUTO-FRAMING (ZOOM INTELIGENTE) 🌟
        # Generamos el nuevo frame ajustado a las manos
        frame_display = cam_tracker.process_frame(frame, landmarks)

        # 🌟 DIBUJAR TEXTO (Después del zoom) 🌟
        # Lo dibujamos en el frame_display para que el texto nunca se deforme ni se recorte
        if stable_gesture:
            cv2.putText(frame_display, f"Gesto: {stable_gesture}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Gesture Control AI", frame_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()