"""
AgroVox - Convertir el modelo .tflite a un arreglo en C
===========================================================
El ESP32 no lee archivos .tflite directamente: el modelo se
incluye como un arreglo de bytes dentro del firmware. Este script
genera ese archivo .h, listo para copiar a la carpeta del proyecto
de Arduino/PlatformIO/ESP-IDF.
"""

MODELO_ENTRADA = "/home/claude/agrovox_ia/modelo_quantizado.tflite"
SALIDA_HEADER = "/home/claude/agrovox_ia/modelo_agrovox.h"
NOMBRE_VARIABLE = "modelo_agrovox_tflite"

with open(MODELO_ENTRADA, "rb") as f:
    datos = f.read()

with open(SALIDA_HEADER, "w") as f:
    f.write("// Archivo generado automáticamente - no editar a mano\n")
    f.write("// Modelo AgroVox: clasificador cavitación vs. ruido (TFLite Micro)\n")
    f.write(f"// Tamaño: {len(datos)} bytes\n\n")
    f.write("#ifndef MODELO_AGROVOX_H\n#define MODELO_AGROVOX_H\n\n")
    f.write(f"const unsigned int {NOMBRE_VARIABLE}_len = {len(datos)};\n")
    f.write(f"alignas(8) const unsigned char {NOMBRE_VARIABLE}[] = {{\n")

    for i, byte in enumerate(datos):
        f.write(f"0x{byte:02x}, ")
        if (i + 1) % 12 == 0:
            f.write("\n")

    f.write("\n};\n\n#endif  // MODELO_AGROVOX_H\n")

print(f"Header generado: {SALIDA_HEADER}")
print(f"Tamaño del modelo: {len(datos)} bytes ({len(datos)/1024:.2f} KB)")
print(f"Variable a usar en el firmware: {NOMBRE_VARIABLE}")
