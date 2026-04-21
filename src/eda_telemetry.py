import sys
import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- CONFIGURACIÓN DE RUTAS ---
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.append(base_path)

try:
    from hand_tracker import HandTracker
    print("✅ Módulo HandTracker cargado.")
except ImportError:
    print("❌ Error: No se encontró hand_tracker.py en la carpeta src.")
    sys.exit()

def run_eda_capture():
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)
    
    data_points = []
    max_samples = 300 
    
    print("\nIniciando captura de telemetría...")

    while len(data_points) < max_samples:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        landmarks = tracker.detect(frame)
        
        if landmarks:
            idx_tip = landmarks[0].landmark[8]
            idx_base = landmarks[0].landmark[5]
            
            data_points.append({
                'index_x': idx_tip.x, 
                'index_y': idx_tip.y, 
                'base_y': idx_base.y,
                'click_dist': np.sqrt((idx_tip.x - idx_base.x)**2 + (idx_tip.y - idx_base.y)**2)
            })
            
        cv2.putText(frame, f"Muestras: {len(data_points)}/{max_samples}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Captura de Datos IA", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    
    if len(data_points) < max_samples: return

    # --- ANÁLISIS ESTADÍSTICO (EDA) ---
    df = pd.DataFrame(data_points)
    plt.figure(figsize=(15, 10))
    plt.suptitle("Análisis Exploratorio de Datos - Gesture Control AI", fontsize=16)

    # 1. Distribución de Movimiento
    plt.subplot(2, 2, 1)
    sns.histplot(df['index_x'], kde=True, color='blue')
    plt.title('Distribución de Posición Horizontal')

    # 2. Análisis de Ruido
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df[['index_y', 'base_y']])
    plt.title('Estabilidad: Punta vs Nudillo')

    # 3. Mapa de Calor (Uso de Pantalla)
    plt.subplot(2, 2, 3)
    plt.hexbin(df['index_x'], df['index_y'], gridsize=15, cmap='BuGn')
    plt.title('Densidad de Interacción')
    plt.gca().invert_yaxis()

    # 4. Correlación de Atributos
    plt.subplot(2, 2, 4)
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Matriz de Correlación')

    plt.tight_layout()
    
    # GUARDADO SEGURO
    try:
        # Intenta crear la carpeta docs si no existe
        root_path = os.path.dirname(base_path)
        docs_dir = os.path.join(root_path, 'docs')
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        
        save_path = os.path.join(docs_dir, 'eda_results.png')
        plt.savefig(save_path)
        print(f"\n✅ Gráfica guardada en: {save_path}")
    except Exception as e:
        # Si falla por permisos, guarda en la raíz
        plt.savefig('eda_results.png')
        print(f"\n⚠️ No se pudo acceder a /docs. Guardado en la raíz como 'eda_results.png'")

    plt.show()

if __name__ == "__main__":
    run_eda_capture()