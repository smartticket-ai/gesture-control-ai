import pyautogui

class Controller:
    def __init__(self):
        # Desactivamos el "failsafe" para evitar que el programa se cierre 
        # si mueves el mouse muy rápido a una esquina (úsalo con cuidado)
        pyautogui.FAILSAFE = False
        self.screen_w, self.screen_h = pyautogui.size()

    def execute(self, gesture, hand_landmarks=None):
        if not gesture:
            return

        if gesture == "SOLO_INDICE" and hand_landmarks:
            # Usamos la punta del dedo índice (punto 8) para mover el cursor
            index_tip = hand_landmarks[0].landmark[8]
            
            # Convertimos coordenadas normalizadas (0-1) a pixeles de tu pantalla
            target_x = int(index_tip.x * self.screen_w)
            target_y = int(index_tip.y * self.screen_h)
            
            # Mover el mouse suavemente a esa posición
            pyautogui.moveTo(target_x, target_y, duration=0.1)
            print(f"Moviendo a: {target_x}, {target_y}")

        elif gesture == "PUÑO":
            # Si cierras la mano, que haga un click
            pyautogui.click()
            print("¡Click!")
