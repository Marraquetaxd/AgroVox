"""
AgroVox - Entrenamiento del modelo TinyML
============================================
Entrena un clasificador binario pequeño (cavitación vs. ruido) sobre
las features extraídas, y lo exporta en 3 formatos:

  1. modelo.h5              -> modelo Keras completo (para seguir iterando)
  2. modelo.tflite           -> convertido a TensorFlow Lite (float32)
  3. modelo_quantizado.tflite -> cuantizado a int8 (el que de verdad
                                  cabe cómodo en la memoria de un ESP32)

------------------------------------------------------------------
CUANDO TENGAN GRABACIONES REALES:
Reemplacen la función `cargar_datos()` de más abajo para que lea sus
archivos reales en vez de generar datos sintéticos. Por ejemplo, si
guardan sus grabaciones como:

    data/reales/cavitacion/*.wav
    data/reales/ruido/*.wav

la función quedaría algo así (usando scipy.io.wavfile o librosa):

    def cargar_datos():
        import glob
        from scipy.io import wavfile
        señales, etiquetas = [], []
        for archivo in glob.glob("data/reales/cavitacion/*.wav"):
            fs, señal = wavfile.read(archivo)
            señales.append(señal.astype(np.float32) / 32768.0)
            etiquetas.append(1)
        for archivo in glob.glob("data/reales/ruido/*.wav"):
            fs, señal = wavfile.read(archivo)
            señales.append(señal.astype(np.float32) / 32768.0)
            etiquetas.append(0)
        return np.array(señales), np.array(etiquetas)

Todo lo demás (extracción de features, entrenamiento, exportación)
sigue funcionando exactamente igual sin tocar una línea más.
------------------------------------------------------------------
"""

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from generar_datos_sinteticos import generar_dataset
from extraer_features import extraer_features, NOMBRES_FEATURES

SEMILLA = 42
np.random.seed(SEMILLA)
tf.random.set_seed(SEMILLA)


def cargar_datos():
    """Fuente de datos actual: SINTÉTICA. Ver docstring de este archivo
    para cómo reemplazarla por grabaciones reales cuando estén listas."""
    return generar_dataset(n_por_clase=400, semilla=SEMILLA)


def construir_modelo(n_features):
    """
    Red densa pequeña a propósito: 3 capas, pocas neuronas. El objetivo
    no es maximizar accuracy a toda costa, sino que el modelo quepa y
    corra rápido en el ESP32 (pocos KB de RAM/flash disponibles).
    """
    modelo = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(n_features,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])
    modelo.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return modelo


def main():
    print("1) Cargando datos...")
    X_crudo, y = cargar_datos()
    print(f"   {len(y)} muestras totales ({(y==1).sum()} cavitación / {(y==0).sum()} ruido)")

    print("2) Extrayendo features...")
    X_feat = extraer_features(X_crudo)

    print("3) Separando train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_feat, y, test_size=0.2, random_state=SEMILLA, stratify=y
    )

    print("4) Normalizando features (media 0, desv. 1)...")
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    print("5) Entrenando modelo...")
    modelo = construir_modelo(n_features=X_feat.shape[1])
    historia = modelo.fit(
        X_train_s, y_train,
        validation_data=(X_test_s, y_test),
        epochs=30, batch_size=16, verbose=2,
    )

    loss, acc = modelo.evaluate(X_test_s, y_test, verbose=0)
    print(f"\n>>> Accuracy final en test: {acc*100:.1f}%  (loss={loss:.3f})")
    print(">>> Recuerda: este accuracy es sobre datos SINTÉTICOS.")
    print(">>> Sirve para validar que el pipeline funciona, NO como una")
    print(">>> métrica real del sistema hasta entrenar con grabaciones reales.\n")

    print("6) Guardando modelo Keras (.h5)...")
    modelo.save("/home/claude/agrovox_ia/modelo.h5")

    print("7) Convirtiendo a TensorFlow Lite (float32)...")
    converter = tf.lite.TFLiteConverter.from_keras_model(modelo)
    tflite_modelo = converter.convert()
    with open("/home/claude/agrovox_ia/modelo.tflite", "wb") as f:
        f.write(tflite_modelo)
    print(f"   modelo.tflite: {len(tflite_modelo)/1024:.1f} KB")

    print("8) Convirtiendo a TensorFlow Lite cuantizado (int8, para ESP32)...")

    def dataset_representativo():
        for i in range(min(100, len(X_train_s))):
            yield [X_train_s[i:i+1].astype(np.float32)]

    converter_q = tf.lite.TFLiteConverter.from_keras_model(modelo)
    converter_q.optimizations = [tf.lite.Optimize.DEFAULT]
    converter_q.representative_dataset = dataset_representativo
    converter_q.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter_q.inference_input_type = tf.int8
    converter_q.inference_output_type = tf.int8
    tflite_quant = converter_q.convert()
    with open("/home/claude/agrovox_ia/modelo_quantizado.tflite", "wb") as f:
        f.write(tflite_quant)
    print(f"   modelo_quantizado.tflite: {len(tflite_quant)/1024:.1f} KB")

    print("\n9) Guardando parámetros del normalizador (necesarios en el ESP32)...")
    np.savez(
        "/home/claude/agrovox_ia/scaler_params.npz",
        mean=scaler.mean_, scale=scaler.scale_, features=NOMBRES_FEATURES,
    )

    print("\nListo. Archivos generados en agrovox_ia/:")
    print("  - modelo.h5")
    print("  - modelo.tflite")
    print("  - modelo_quantizado.tflite  <- este es el que se carga al ESP32")
    print("  - scaler_params.npz         <- medias/desviaciones para normalizar en el firmware")

    return modelo, historia


if __name__ == "__main__":
    main()
