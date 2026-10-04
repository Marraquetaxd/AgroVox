"""
AgroVox - Extracción de características (features)
=====================================================
No entrenamos el modelo sobre la señal cruda (sería demasiado pesado
para un ESP32). En su lugar, calculamos un puñado de características
de tiempo y frecuencia por cada ventana de señal — este es el mismo
enfoque que usan Edge Impulse y la mayoría de los pipelines de TinyML
para audio/vibración.

Cada feature está elegida porque tiene una razón física concreta para
ayudar a distinguir cavitación de ruido:

  - energia_total       -> un evento real tiene más energía que el piso de ruido
  - pico_amplitud        -> los eventos de cavitación tienen un pico marcado
  - tiempo_hasta_pico    -> attack rápido (cavitación) vs. gradual (viento)
  - frecuencia_dominante -> debe caer dentro de la banda esperada (100-240 kHz aquí)
  - centroide_espectral  -> "centro de masa" de la energía en frecuencia
  - ancho_banda          -> qué tan concentrada o dispersa está la energía
  - cruces_por_cero      -> proxy barato de contenido de alta frecuencia
  - curtosis             -> qué tan "puntiaguda" es la distribución de amplitud
"""

import numpy as np
from scipy.stats import kurtosis
from generar_datos_sinteticos import FS

NOMBRES_FEATURES = [
    "energia_total", "pico_amplitud", "tiempo_hasta_pico",
    "frecuencia_dominante", "centroide_espectral", "ancho_banda",
    "cruces_por_cero", "curtosis",
]


def extraer_features_una_señal(señal):
    n = len(señal)

    energia_total = float(np.sum(señal ** 2))
    pico_amplitud = float(np.max(np.abs(señal)))
    idx_pico = int(np.argmax(np.abs(señal)))
    tiempo_hasta_pico = idx_pico / FS

    # --- Dominio de la frecuencia (FFT) ---
    espectro = np.abs(np.fft.rfft(señal))
    freqs = np.fft.rfftfreq(n, d=1 / FS)

    # evitar división por cero si la señal es silencio total
    energia_espectral = espectro.sum() + 1e-9

    idx_dom = int(np.argmax(espectro))
    frecuencia_dominante = float(freqs[idx_dom])

    centroide_espectral = float(np.sum(freqs * espectro) / energia_espectral)
    ancho_banda = float(
        np.sqrt(np.sum(((freqs - centroide_espectral) ** 2) * espectro) / energia_espectral)
    )

    # --- Cruces por cero ---
    cruces_por_cero = int(np.sum(np.diff(np.sign(señal)) != 0))

    curt = float(kurtosis(señal))

    return np.array([
        energia_total, pico_amplitud, tiempo_hasta_pico,
        frecuencia_dominante, centroide_espectral, ancho_banda,
        cruces_por_cero, curt,
    ], dtype=np.float32)


def extraer_features(X):
    """X: (N, n_muestras) señales crudas -> devuelve (N, n_features)."""
    return np.array([extraer_features_una_señal(s) for s in X], dtype=np.float32)


if __name__ == "__main__":
    from generar_datos_sinteticos import generar_dataset

    X, y = generar_dataset(n_por_clase=5)
    feats = extraer_features(X)
    print("Features por muestra:", NOMBRES_FEATURES)
    for i in range(len(y)):
        etiqueta = "cavitacion" if y[i] == 1 else "ruido"
        print(f"[{etiqueta:10s}]", np.round(feats[i], 2))
