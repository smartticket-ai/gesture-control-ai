import sys
import os
import cv2
import time
import customtkinter as ctk
from PIL import Image, ImageTk
from collections import deque
from statistics import mode

# Importamos tu backend
from camera import Camera
from hand_tracker import HandTracker
from gesture_classifier import GestureClassifier
from controller import Controller
from camera_tracker import CameraTracker

# Configuración visual del Frontend
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VirtualMouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gesture Control AI - Pro Edition")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- VARIABLES DEL BACKEND ---
        self.cam = None
        self.tracker = HandTracker()
        self.classifier = GestureClassifier()
        self.control = Controller()
        self.cam_tracker = CameraTracker()
        
        self.is_running = False
        self.last_volume_action_time = 0
        self.volume_cooldown = 0.2  
        self.gesture_buffer = deque(maxlen=7)

        # --- DISEÑO DE LA INTERFAZ (UI) ---
        
        # Panel lateral (Menú)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AI Control\nPanel", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=30, padx=20)

        self.btn_start = ctk.CTkButton(self.sidebar_frame, text="▶ Iniciar Cámara", fg_color="green", hover_color="darkgreen", command=self.start_system)
        self.btn_start.pack(pady=10, padx=20)

        self.btn_stop = ctk.CTkButton(self.sidebar_frame, text="⏹ Detener", fg_color="red", hover_color="darkred", state="disabled", command=self.stop_system)
        self.btn_stop.pack(pady=10, padx=20)

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Estado: Apagado", text_color="gray")
        self.status_label.pack(pady=20, padx=20)

        # Guía rápida
        guia_texto = "✋ Guía de Gestos:\n\n☝️ 1 Dedo: Mover Mouse\n✊ Puño: Clic Izquierdo\n🤏 Pinza: Arrastrar\n✌️ 2 Dedos: Scroll\n\n(Mano 2)\n👍 Pulgar Arriba: Vol +\n👎 Pulgar Abajo: Vol -\n✊ Puño: Clic Derecho"
        self.guide_label = ctk.CTkLabel(self.sidebar_frame, text=guia_texto, justify="left", text_color="lightgray")
        self.guide_label.pack(side="bottom", pady=20, padx=10)

        # Área de Video Principal
        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.video_label = ctk.CTkLabel(self.video_frame, text="Presiona 'Iniciar' para encender la cámara")
        self.video_label.pack(fill="both", expand=True)

    # --- LÓGICA DE CONTROL ---

    def start_system(self):
        self.cam = Camera()
        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status_label.configure(text="Estado: ACTIVO", text_color="green")
        self.update_frame() # Inicia el bucle de video

    def stop_system(self):
        self.is_running = False
        if self.cam:
            self.cam.release()
            self.cam = None
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.status_label.configure(text="Estado: Apagado", text_color="gray")
        self.video_label.configure(image="", text="Cámara detenida")

    def update_frame(self):
        if not self.is_running:
            return

        frame = self.cam.get_frame()
        if frame is not None:
            # Procesamiento de MediaPipe
            landmarks = self.tracker.detect(frame)
            stable_gesture = None
            
            if landmarks:
                raw_gesture = self.classifier.classify(landmarks)
                if raw_gesture:
                    self.gesture_buffer.append(raw_gesture)
                    stable_gesture = mode(self.gesture_buffer)
                else:
                    self.gesture_buffer.clear()
                    
                if stable_gesture:
                    current_time = time.time()
                    
                    if stable_gesture in ["VOL_UP", "VOL_DOWN"]:
                        if current_time - self.last_volume_action_time > self.volume_cooldown:
                            self.control.execute(stable_gesture, landmarks)
                            self.last_volume_action_time = current_time
                    else:
                        self.control.execute(stable_gesture, landmarks)

            else:
                self.gesture_buffer.clear()

            # Auto-framing (El Zoom)
            frame_display = self.cam_tracker.process_frame(frame, landmarks)

            # Dibujar texto de estado en el video
            if stable_gesture:
                cv2.putText(frame_display, f"Gesto: {stable_gesture}", (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 100), 2)

            # Convertir la imagen de OpenCV (BGR) a formato para Tkinter (RGB)
            frame_rgb = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Actualizar la interfaz
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk, text="")

        # Llama a esta misma función cada 15 milisegundos (Bucle de video)
        if self.is_running:
            self.after(15, self.update_frame)

    def on_closing(self):
        self.stop_system()
        self.destroy()

if __name__ == "__main__":
    app = VirtualMouseApp()
    app.mainloop()