import pyautogui
import math

class Controller:
    def __init__(self):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0 
        self.screen_w, self.screen_h = pyautogui.size()
        
        self.prev_x, self.prev_y = 0, 0
        self.smooth_factor = 0.5 
        self.prev_scroll_y = None
        
        self.is_dragging = False 
        self.is_right_clicking = False
        self.click_ready = True  # Seguro para evitar spam de clics normales

    def _move_mouse(self, tip_landmark):
        margin = 0.2
        target_x = (tip_landmark.x - margin) / (1 - 2 * margin)
        target_y = (tip_landmark.y - margin) / (1 - 2 * margin)
        
        target_x = max(0.0, min(1.0, target_x))
        target_y = max(0.0, min(1.0, target_y))

        curr_x = int(target_x * self.screen_w)
        curr_y = int(target_y * self.screen_h)

        smooth_x = self.prev_x + (curr_x - self.prev_x) * self.smooth_factor
        smooth_y = self.prev_y + (curr_y - self.prev_y) * self.smooth_factor

        pyautogui.moveTo(int(smooth_x), int(smooth_y))
        self.prev_x, self.prev_y = smooth_x, smooth_y

    def execute(self, gesture, landmarks):
        if not gesture or not landmarks: return

        index_tip = landmarks[0].landmark[8]
        middle_tip = landmarks[0].landmark[12]

        if gesture != "MODO_SCROLL":
            self.prev_scroll_y = None

        if gesture != "RIGHT_CLICK":
            self.is_right_clicking = False
            
        # Reactivamos el clic normal cuando dejas de hacer la pinza del índice
        if gesture != "CLICK":
            self.click_ready = True

        # --- LÓGICA DE SOLTAR EL ARRASTRE ---
        if self.is_dragging and gesture != "DRAG":
            pyautogui.mouseUp()
            print("🖱️ Fin de arrastre")
            self.is_dragging = False

        # --- CLICK NORMAL (Pulgar + Índice) ---
        if gesture == "CLICK":
            if self.click_ready:
                pyautogui.click()
                print("🖱️ Clic Normal")
                self.click_ready = False  # Bloqueamos hasta que se separen los dedos

        # --- MODO ARRASTRE (Pulgar + Medio) ---
        elif gesture == "DRAG":
            if not self.is_dragging:
                pyautogui.mouseDown()
                print("🖱️ Inicio de arrastre")
                self.is_dragging = True
            
            # Movemos el ratón guiándonos por el dedo medio mientras arrastramos
            self._move_mouse(middle_tip)

        # --- MOVIMIENTO DEL RATÓN NORMAL ---
        elif gesture == "MODO_MOUSE":
            self._move_mouse(index_tip)

        # --- CLICK DERECHO (Con 2 manos) ---
        elif gesture == "RIGHT_CLICK":
            if not self.is_right_clicking:
                pyautogui.click(button='right')
                print("🖱️ Clic Derecho ejecutado")
                self.is_right_clicking = True

        # --- VOLUMEN ---
        elif gesture == "VOL_UP":
            pyautogui.press("volumeup")
        elif gesture == "VOL_DOWN":
            pyautogui.press("volumedown")

        # --- RUEDA DE SCROLL ---
        elif gesture == "MODO_SCROLL":
            index_y = index_tip.y
            if self.prev_scroll_y is None or abs(index_y - self.prev_scroll_y) > 0.2:
                self.prev_scroll_y = index_y
                
            delta_y = index_y - self.prev_scroll_y
            if abs(delta_y) > 0.01:
                pyautogui.scroll(int(-delta_y * 3000)) 
                self.prev_scroll_y = index_y