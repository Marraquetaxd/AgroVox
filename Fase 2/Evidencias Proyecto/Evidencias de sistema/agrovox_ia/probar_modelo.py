"""
AgroVox - Probar el modelo en tu PC (sin necesitar el ESP32)
================================================================
Este script hace dos cosas:

  1. Genera un puñado de señales NUEVAS (que el modelo nunca vio
     durante el entrenamiento) y le pregunta qué predice para cada
     una, para que puedas ver el modelo "en acción".

  2. Prueba el modelo usando el mismo intérprete de TensorFlow Lite
     que corre dentro de un microcontrolador (tf.lite.Interpreter),
     sobre el archivo YA CUANTIZADO (modelo_quantizado.tflite) - o
     sea, es la forma más fiel de probar "como si fuera el ESP32"
     sin tener la placa todavía.

Ejecutar con:  python probar_modelo.py
"""

import numpy as np
import tensorflow as tf

from generar_datos_sinteticos import generar_dataset
from extraer_features import extraer_features, NOMBRES_FEATURES

RUTA_MODELO_H5 = "modelo.h5"
RUTA_MODELO_TFLITE_QUANT = "modelo_quantizado.tflite"
RUTA_SCALER = "scaler_params.npz"


def cargar_scaler():
    datos = np.load(RUTA_SCALER, allow_pickle=True)
    return datos["mean"], datos["scale"]


def normalizar(X_feat, mean, scale):
    return (X_feat - mean) / scale


# =========================================================
# PARTE 1: probar el modelo Keras completo (.h5)
# =========================================================
def probar_modelo_h5(X_feat_norm, y_real):
    print("=" * 60)
    print("PARTE 1: Probando el modelo completo (modelo.h5)")
    print("=" * 60)

    modelo = tf.keras.models.load_model(RUTA_MODELO_H5)
    probs = modelo.predict(X_feat_norm, verbose=0).flatten()
    preds = (probs >= 0.5).astype(int)

    aciertos = 0
    for i in range(len(y_real)):
        etiqueta_real = "cavitacion" if y_real[i] == 1 else "ruido"
        etiqueta_pred = "cavitacion" if preds[i] == 1 else "ruido"
        correcto = "✓" if preds[i] == y_real[i] else "✗ (ERROR)"
        aciertos += int(preds[i] == y_real[i])
        print(f"  Real: {etiqueta_real:10s} | Predicho: {etiqueta_pred:10s} "
              f"(confianza {probs[i]*100:5.1f}%)  {correcto}")

    print(f"\nAccuracy en estas muestras nuevas: {aciertos}/{len(y_real)} "
          f"({aciertos/len(y_real)*100:.1f}%)\n")


# =========================================================
# PARTE 2: probar el modelo TFLite cuantizado (como en el ESP32)
# =========================================================
def probar_modelo_tflite(X_feat_norm, y_real):
    print("=" * 60)
    print("PARTE 2: Probando el modelo CUANTIZADO (como correría en el ESP32)")
    print("=" * 60)

    interprete = tf.lite.Interpreter(model_path=RUTA_MODELO_TFLITE_QUANT)
    interprete.allocate_tensors()

    entrada_info = interprete.get_input_details()[0]
    salida_info = interprete.get_output_details()[0]

    # El modelo cuantizado espera enteros int8, no decimales.
    # Hay que aplicar la misma transformación que TFLite usa internamente.
    escala_entrada, punto_cero_entrada = entrada_info["quantization"]
    escala_salida, punto_cero_salida = salida_info["quantization"]

    aciertos = 0
    for i in range(len(y_real)):
        x = X_feat_norm[i:i+1].astype(np.float32)
        x_int8 = (x / escala_entrada + punto_cero_entrada).astype(np.int8)

        interprete.set_tensor(entrada_info["index"], x_int8)
        interprete.invoke()
        salida_int8 = interprete.get_tensor(salida_info["index"])

        salida_float = (salida_int8.astype(np.float32) - punto_cero_salida) * escala_salida
        prob = float(salida_float[0][0])
        pred = int(prob >= 0.5)

        etiqueta_real = "cavitacion" if y_real[i] == 1 else "ruido"
        etiqueta_pred = "cavitacion" if pred == 1 else "ruido"
        correcto = "✓" if pred == y_real[i] else "✗ (ERROR)"
        aciertos += int(pred == y_real[i])
        print(f"  Real: {etiqueta_real:10s} | Predicho: {etiqueta_pred:10s} "
              f"(confianza {prob*100:5.1f}%)  {correcto}")

    print(f"\nAccuracy con el modelo cuantizado: {aciertos}/{len(y_real)} "
          f"({aciertos/len(y_real)*100:.1f}%)")
    print("(Si este número es parecido al de la Parte 1, la cuantización")
    print(" no perdió precisión relevante - buena señal para el ESP32)\n")


def main():
    print("\nGenerando 20 señales NUEVAS (con semilla distinta a las de entrenamiento)...\n")
    X_crudo, y_real = generar_dataset(n_por_clase=10, semilla=999)  # semilla distinta
    X_feat = extraer_features(X_crudo)
    mean, scale = cargar_scaler()
    X_feat_norm = normalizar(X_feat, mean, scale)

    probar_modelo_h5(X_feat_norm, y_real)
    probar_modelo_tflite(X_feat_norm, y_real)


if __name__ == "__main__":
    main()
