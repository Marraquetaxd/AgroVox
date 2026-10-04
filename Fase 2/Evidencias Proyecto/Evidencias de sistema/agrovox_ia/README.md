# AgroVox — Base del pipeline de IA (Edge AI / TinyML)

Esta es la **base** del modelo de clasificación acústica de AgroVox: cavitación vs. ruido.
Está construida sobre **datos sintéticos** porque todavía no hay grabaciones reales del
sensor piezoeléctrico — pero todo el pipeline (generación → features → entrenamiento →
exportación a ESP32) ya está funcionando de punta a punta, listo para el día que tengan
audio real.

## Qué hace cada archivo

| Archivo | Qué hace |
|---|---|
| `generar_datos_sinteticos.py` | Genera señales sintéticas de "cavitación" y "ruido" (viento, tonal) |
| `extraer_features.py` | Calcula 8 características de tiempo/frecuencia por señal |
| `entrenar_modelo.py` | Entrena el clasificador y exporta a `.h5`, `.tflite` y `.tflite` cuantizado |
| `convertir_a_c_array.py` | Convierte el modelo cuantizado a un header `.h` para el firmware del ESP32 |

## Cómo correrlo

```bash
pip install tensorflow numpy scipy scikit-learn

python3 generar_datos_sinteticos.py   # opcional, entrenar_modelo.py ya lo llama
python3 entrenar_modelo.py            # entrena y exporta los 3 formatos de modelo
python3 convertir_a_c_array.py        # genera modelo_agrovox.h para el ESP32
```

## Resultado de la última corrida

- Accuracy en test (datos sintéticos): **100%** — esperable, ya que las clases sintéticas
  son bastante separables. Esto valida que el *pipeline* funciona, **no** es una métrica
  real del sistema todavía.
- `modelo.tflite`: 3.2 KB
- `modelo_quantizado.tflite`: 3.4 KB — este tamaño es perfectamente viable para el ESP32
  (que típicamente tiene cientos de KB a un par de MB de flash disponibles).

## Cuándo tengan grabaciones reales

Solo necesitan tocar **una función**, en `entrenar_modelo.py`:

```python
def cargar_datos():
    return generar_dataset(n_por_clase=400, semilla=SEMILLA)  # <- reemplazar esto
```

Por una que lea sus archivos `.wav` reales (el docstring de `entrenar_modelo.py` trae un
ejemplo completo de cómo hacerlo con `scipy.io.wavfile`). Todo lo demás —extracción de
features, arquitectura del modelo, entrenamiento, exportación— sigue funcionando igual.

## Cómo usar el modelo en el ESP32

1. Copien `modelo_agrovox.h` a la carpeta de su proyecto (Arduino/PlatformIO/ESP-IDF)
2. Instalen la librería **TensorFlow Lite for Microcontrollers** (o **Arduino_TensorFlowLite**)
3. En el firmware, calculen las mismas 8 features (`extraer_features.py` documenta la
   fórmula de cada una) sobre la ventana de señal capturada, normalícenlas con los valores
   guardados en `scaler_params.npz`, y pásenlas al intérprete de TFLite Micro junto con
   `modelo_agrovox_tflite` y `modelo_agrovox_tflite_len`

## Sobre las features elegidas

No se entrena sobre la señal cruda (sería muy pesado para el ESP32). Se usan 8
características con justificación física, no arbitrarias — están documentadas con su
razón de ser en el docstring de `extraer_features.py`. Esto es importante para el informe:
pueden explicar *por qué* cada feature ayuda a distinguir cavitación de ruido, no solo que
"se metieron en una red neuronal".
