import cv2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from hand_tracker import HandTracker

def run_eda_capture():
    tracker = HandTracker()
    cap = cv2.VideoCapture(0)
    data_points = []
    max_samples = 300  # Capturaremos 300 frames de datos
    
    print(f"Capturando {max_samples} muestras para el EDA. Mueve la mano frente a la cámara...")

    while len(data_points) < max_samples:
        ret, frame = cap.read()
        if not ret: break
        
        landmarks = tracker.detect(frame)
        if landmarks:
            # Extraemos coordenadas X, Y, Z de la punta del índice (punto 8) 
            # y el nudillo (punto 5) para comparar estabilidad
            idx_tip = landmarks[0].landmark[8]
            idx_base = landmarks[0].landmark[5]
            
            data_points.append({
                'tip_x': idx_tip.x, 'tip_y': idx_tip.y, 'tip_z': idx_tip.z,
                'base_x': idx_base.x, 'base_y': idx_base.y,
                'dist_click': np.sqrt((idx_tip.x - idx_base.x)**2 + (idx_tip.y - idx_base.y)**2)
            })
            
        cv2.putText(frame, f"Muestras: {len(data_points)}/{max_samples}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Captura de Datos para EDA", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()
    
    # --- PROCESAMIENTO ESTADÍSTICO ---
    df = pd.DataFrame(data_points)
    
    # 1. Medidas de Tendencia Central y Dispersión
    stats = df.describe()
    print("\n--- ESTADÍSTICA DESCRIPTIVA ---")
    print(stats)

    # 2. Visualización
    plt.figure(figsize=(15, 10))

    # Gráfico 1: Distribución de la posición X del mouse (Histograma)
    plt.subplot(2, 2, 1)
    sns.histplot(df['tip_x'], kde=True, color='blue')
    plt.title('Distribución de Probabilidad: Posición X (Punta del Índice)')
    plt.xlabel('Coordenada X normalizada')

    # Gráfico 2: Estabilidad (Boxplot) - Compara Ruido entre punta y nudillo
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df[['tip_y', 'base_y']])
    plt.title('Comparación de Variabilidad (Ruido): Punta vs Nudillo')
    plt.ylabel('Posición Vertical')

    # Gráfico 3: Relación X vs Y (Scatter Plot - Mapa de calor de uso)
    plt.subplot(2, 2, 3)
    plt.hexbin(df['tip_x'], df['tip_y'], gridsize=20, cmap='YlOrRd')
    plt.title('Densidad de Movimiento (Mapa de Calor)')
    plt.gca().invert_yaxis() # Invertir para que coincida con la cámara

    # Gráfico 4: Correlación entre variables (Heatmap)
    plt.subplot(2, 2, 4)
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Matriz de Correlación de Atributos')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_eda_capture()