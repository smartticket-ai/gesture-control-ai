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
        self.click_ready = True 

    def _move_mouse(self, landmark_point):
        # Usamos el punto que nos pasen (ahora será el nudillo)
        margin = 0.2
        target_x = (landmark_point.x - margin) / (1 - 2 * margin)
        target_y = (landmark_point.y - margin) / (1 - 2 * margin)
        
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

        # --- PUNTOS CLAVE DE LA MANO PRINCIPAL ---
        index_tip = landmarks[0].landmark[8]    # Yema del índice (para scroll)
        index_base = landmarks[0].landmark[5]   # NUEVO: Nudillo del índice (para mover mouse sin temblar)
        middle_tip = landmarks[0].landmark[12]  # Yema del dedo medio (para arrastrar)

        # Reset de scroll y clics
        if gesture != "MODO_SCROLL":
            self.prev_scroll_y = None
        if gesture != "RIGHT_CLICK":
            self.is_right_clicking = False
        if gesture != "CLICK":
            self.click_ready = True

        # --- SOLTAR EL ARRASTRE ---
        if self.is_dragging and gesture != "DRAG":
            pyautogui.mouseUp()
            print("🖱️ Fin de arrastre")
            self.is_dragging = False

        # --- MODO MOUSE (AHORA SIGUE AL NUDILLO) ---
        if gesture == "MODO_MOUSE":
            self._move_mouse(index_base) # <- MAGIA: El ratón ignora tu yema y sigue el nudillo

        # --- CLICK NORMAL ---
        elif gesture == "CLICK":
            if self.click_ready:
                pyautogui.click()
                print("🖱️ Clic Izquierdo estático")
                self.click_ready = False  

        # --- MODO ARRASTRE ---
        elif gesture == "DRAG":
            if not self.is_dragging:
                pyautogui.mouseDown()
                print("🖱️ Inicio de arrastre")
                self.is_dragging = True
            self._move_mouse(middle_tip)

        # --- MODO SCROLL ---
        elif gesture == "MODO_SCROLL":
            index_y = index_tip.y
            if self.prev_scroll_y is None or abs(index_y - self.prev_scroll_y) > 0.2:
                self.prev_scroll_y = index_y
            delta_y = index_y - self.prev_scroll_y
            if abs(delta_y) > 0.01:
                pyautogui.scroll(int(-delta_y * 3000)) 
                self.prev_scroll_y = index_y 

        # --- CONTROLES DE LA SEGUNDA MANO ---
        elif gesture == "RIGHT_CLICK":
            if not self.is_right_clicking:
                pyautogui.click(button='right')
                print("🖱️ Clic Derecho")
                self.is_right_clicking = True

        elif gesture == "VOL_UP":
            pyautogui.press("volumeup")
            
        elif gesture == "VOL_DOWN":
            pyautogui.press("volumedown")