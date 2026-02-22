import pyautogui

class Controller:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_w, self.screen_h = pyautogui.size()

    def execute(self, gesture, landmarks):
        if not gesture or not landmarks: return

        if gesture == "MODO_MOUSE":
            # Usar la coordenada del punto 8 (punta del índice)
            index_tip = landmarks[0].landmark[8]
            x = int(index_tip.x * self.screen_w)
            y = int(index_tip.y * self.screen_h)
            # Mover el mouse suavemente
            pyautogui.moveTo(x, y, duration=0.1)

        elif gesture == "PUÑO":
            # Hacer clic izquierdo
            pyautogui.click()
