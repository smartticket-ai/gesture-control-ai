import cv2
import numpy as np

class CameraTracker:
    def __init__(self):
        # Qué tan suave quieres que sea el movimiento de la cámara (0.1 = muy suave, 1.0 = rígido)
        self.smooth_factor = 0.15 
        # Margen adicional alrededor de la mano (para que no esté pegada al borde)
        self.padding = 0.6 
        
        self.prev_bbox = None

    def process_frame(self, frame, multi_hand_landmarks):
        h, w, _ = frame.shape
        
        # Si no hay manos, el objetivo es mostrar toda la pantalla normal
        if not multi_hand_landmarks:
            target_bbox = [0, w, 0, h]
        else:
            # Encontrar los puntos más extremos de TODAS las manos en pantalla
            x_min, x_max, y_min, y_max = w, 0, h, 0
            for hand_landmarks in multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_min = min(x_min, x)
                    x_max = max(x_max, x)
                    y_min = min(y_min, y)
                    y_max = max(y_max, y)
            
            # Calcular el ancho y alto del cuadro de las manos
            box_w = x_max - x_min
            box_h = y_max - y_min
            
            # Prevenir que el cuadro sea demasiado pequeño si la mano está cerrada
            box_w = max(box_w, 100)
            box_h = max(box_h, 100)
            
            # Añadir el margen (padding)
            pad_w = int(box_w * self.padding)
            pad_h = int(box_h * self.padding)
            
            target_x_min = max(0, x_min - pad_w)
            target_x_max = min(w, x_max + pad_w)
            target_y_min = max(0, y_min - pad_h)
            target_y_max = min(h, y_max + pad_h)
            
            # --- MANTENER LA PROPORCIÓN DE LA CÁMARA ---
            # Si no hacemos esto, la imagen se verá estirada o aplastada.
            target_w = target_x_max - target_x_min
            target_h = target_y_max - target_y_min
            aspect_ratio = w / h
            
            if target_w / target_h > aspect_ratio:
                # Muy ancho, necesitamos aumentar el alto
                new_h = int(target_w / aspect_ratio)
                diff = new_h - target_h
                target_y_min = max(0, target_y_min - diff // 2)
                target_y_max = min(h, target_y_max + diff // 2)
            else:
                # Muy alto, necesitamos aumentar el ancho
                new_w = int(target_h * aspect_ratio)
                diff = new_w - target_w
                target_x_min = max(0, target_x_min - diff // 2)
                target_x_max = min(w, target_x_max + diff // 2)
            
            # Asegurarse de que el cuadro no se salga de la pantalla original
            target_x_min = max(0, target_x_min)
            target_x_max = min(w, target_x_max)
            target_y_min = max(0, target_y_min)
            target_y_max = min(h, target_y_max)
            
            target_bbox = [target_x_min, target_x_max, target_y_min, target_y_max]

        # --- SUAVIZADO (Efecto cinemático) ---
        if self.prev_bbox is None:
            self.prev_bbox = target_bbox
        else:
            self.prev_bbox = [
                int(self.prev_bbox[i] + (target_bbox[i] - self.prev_bbox[i]) * self.smooth_factor)
                for i in range(4)
            ]
        
        p_xmin, p_xmax, p_ymin, p_ymax = self.prev_bbox
        
        # Evitar errores si el área es 0 (medida de seguridad)
        if p_xmax - p_xmin < 10 or p_ymax - p_ymin < 10:
            return frame

        # --- RECORTAR Y HACER ZOOM ---
        cropped_frame = frame[p_ymin:p_ymax, p_xmin:p_xmax]
        zoomed_frame = cv2.resize(cropped_frame, (w, h))
        
        return zoomed_frame