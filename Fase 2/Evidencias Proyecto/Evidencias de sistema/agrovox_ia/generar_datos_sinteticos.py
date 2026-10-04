"""
AgroVox - Generador de datos sintéticos
=========================================
Mientras no tengamos grabaciones reales del sensor piezoeléctrico,
este script genera señales SINTÉTICAS que imitan las dos clases que
el modelo debe aprender a distinguir:

  - "cavitacion": un transiente corto (attack rápido + decaimiento
    exponencial), con energía concentrada en 100 kHz - 1 MHz. Esto
    imita la forma descrita en la literatura (Milburn & Johnson 1966;
    Oletic et al. 2020) para eventos de cavitación en el xilema.

  - "ruido": ruido ambiental de banda ancha (viento), o un tono
    angosto sostenido (insectos, vibración mecánica) - los dos
    "falsos positivos" más comunes en campo.

IMPORTANTE: esto NO reemplaza datos reales. Es solo para dejar el
pipeline completo (features -> modelo -> TFLite) construido y
probado, de modo que el día que tengan grabaciones reales del
prototipo, solo deban reemplazar la función `cargar_datos_reales()`
en `entrenar_modelo.py` sin tocar el resto del código.
"""

import numpy as np

FS = 500_000          # Frecuencia de muestreo simulada (Hz). 500 kHz alcanza
                       # para representar el rango de interés (100 kHz-1 MHz
                       # queda parcialmente sub-muestreado, pero es suficiente
                       # para prototipar features realistas sin sobrecargar
                       # el generador; ajusten esto cuando tengan el ADC real).
DURACION_VENTANA = 0.004   # 4 ms por muestra (ventana corta, típica de un evento)
N_MUESTRAS = int(FS * DURACION_VENTANA)


def _ruido_base(amplitud=0.02):
    """Ruido de piso presente en ambas clases (ruido electrónico del sensor)."""
    return np.random.normal(0, amplitud, N_MUESTRAS)


def generar_evento_cavitacion(rng, amplitud=1.0, freq_min=100_000, freq_max=240_000):
    """
    Simula un pulso de cavitación: attack casi instantáneo y
    decaimiento exponencial, modulado por una frecuencia dominante
    dentro del rango típico reportado para xilema (limitado a 240 kHz
    por el límite de Nyquist de nuestra FS simulada de 500 kHz).
    """
    t = np.arange(N_MUESTRAS) / FS
    inicio = rng.integers(low=int(0.15 * N_MUESTRAS), high=int(0.35 * N_MUESTRAS))
    freq = rng.uniform(freq_min, freq_max)
    tau = rng.uniform(0.00005, 0.00015)  # constante de decaimiento (50-150 us)

    envolvente = np.zeros(N_MUESTRAS)
    t_rel = t - t[inicio]
    mask = t_rel >= 0
    envolvente[mask] = np.exp(-t_rel[mask] / tau)

    fase = rng.uniform(0, 2 * np.pi)
    portadora = np.sin(2 * np.pi * freq * t + fase)

    señal = amplitud * envolvente * portadora
    señal += _ruido_base()
    return señal.astype(np.float32)


def generar_ruido_viento(rng, amplitud=0.35):
    """Ruido de banda ancha (viento, hojas rozando la carcasa)."""
    señal = rng.normal(0, amplitud, N_MUESTRAS)
    # Filtro pasa-bajo simple para que se parezca a ruido de viento real
    kernel = np.ones(5) / 5
    señal = np.convolve(señal, kernel, mode="same")
    señal += _ruido_base()
    return señal.astype(np.float32)


def generar_ruido_tonal(rng, amplitud=0.4):
    """Tono sostenido de banda angosta (insecto, vibración mecánica)."""
    t = np.arange(N_MUESTRAS) / FS
    freq = rng.uniform(20_000, 80_000)  # fuera del rango típico de cavitación
    señal = amplitud * np.sin(2 * np.pi * freq * t)
    señal += _ruido_base()
    return señal.astype(np.float32)


def generar_dataset(n_por_clase=300, semilla=42):
    """
    Devuelve (X, y) donde X es un arreglo (N, N_MUESTRAS) de señales
    crudas, e y es 1 para "cavitacion" y 0 para "ruido" (viento o tonal,
    mitad y mitad).
    """
    rng = np.random.default_rng(semilla)
    señales, etiquetas = [], []

    for _ in range(n_por_clase):
        señales.append(generar_evento_cavitacion(rng))
        etiquetas.append(1)

    for _ in range(n_por_clase // 2):
        señales.append(generar_ruido_viento(rng))
        etiquetas.append(0)
    for _ in range(n_por_clase - n_por_clase // 2):
        señales.append(generar_ruido_tonal(rng))
        etiquetas.append(0)

    X = np.array(señales, dtype=np.float32)
    y = np.array(etiquetas, dtype=np.int32)

    # Mezclar
    idx = rng.permutation(len(y))
    return X[idx], y[idx]


if __name__ == "__main__":
    X, y = generar_dataset()
    print(f"Dataset sintético generado: {X.shape[0]} muestras, {X.shape[1]} puntos c/u")
    print(f"Cavitación: {(y==1).sum()}  |  Ruido: {(y==0).sum()}")
    np.savez("/home/claude/agrovox_ia/data/dataset_sintetico.npz", X=X, y=y)
    print("Guardado en data/dataset_sintetico.npz")
