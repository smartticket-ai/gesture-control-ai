import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, f1_score
import time

def generate_evaluation_report():
    print("--- SIMULADOR DE EVALUACIÓN DE RENDIMIENTO ---")
    print("Instrucciones: El sistema comparará las detecciones de la IA con la verdad de campo.")
    
    # Datos de ejemplo basados en una sesión de prueba real de 20 intentos
    # 1 = Clic detectado/real, 0 = Reposo
    y_true = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 10 clics reales, 10 reposos
    y_pred = [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0] # La IA falló en 2 clics y tuvo 1 falso positivo

    # 1. Cálculo de métricas detalladas
    f1 = f1_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=['Reposo', 'Clic'])
    
    print("\n✅ Métricas calculadas con éxito.")
    print(f"Métrica Principal (F1-Score): {f1:.2f}")
    print("\nReporte Detallado:")
    print(report)

    # 2. Visualización: Matriz de Confusión
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Predicho: Reposo', 'Predicho: Clic'],
                yticklabels=['Real: Reposo', 'Real: Clic'])
    
    plt.title('Punto 6: Matriz de Confusión - Validación de Gestos', fontsize=14)
    plt.xlabel('Predicción del Modelo')
    plt.ylabel('Realidad (Ground Truth)')
    
    # Guardar para la diapositiva
    plt.savefig('metrics_confusion_matrix.png')
    print("\n✅ Gráfica 'metrics_confusion_matrix.png' guardada para tu presentación.")
    plt.show()

    # 3. Visualización: MAE (Simulación de error de precisión)
    # Generamos errores aleatorios pequeños para simular la precisión del cursor
    errores = np.random.normal(0, 5, 100) # Media 0, desviación 5 píxeles
    plt.figure(figsize=(8, 4))
    sns.histplot(errores, kde=True, color='orange')
    plt.axvline(np.mean(np.abs(errores)), color='red', linestyle='--', label=f'MAE: {np.mean(np.abs(errores)):.2f}px')
    plt.title('Punto 6: Distribución del Error de Regresión (MAE)', fontsize=14)
    plt.xlabel('Error en Píxeles')
    plt.legend()
    plt.savefig('metrics_mae_error.png')
    plt.show()

if __name__ == "__main__":
    generate_evaluation_report()