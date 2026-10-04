# AgroVox — Monitoreo Acústico de Estrés Hídrico

Sistema IoT de bajo costo que detecta eventos de cavitación en el xilema de paltos (Hass) y cerezos mediante un sensor acústico piezoeléctrico y un modelo de Inteligencia Artificial embebido (Edge AI / TinyML), para generar alertas tempranas de estrés hídrico antes de que el daño sea visible, enviadas al agricultor por WhatsApp.

Proyecto de Título (Capstone, PTY4614) — Alonso Campusano y Pablo Vargas.

## Tabla de contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Ejecución local](#ejecución-local)
- [Integrantes y roles](#integrantes-y-roles)
- [Metodología](#metodología)
- [Modelo de datos](#modelo-de-datos)
- [Diagramas](#diagramas)
- [Documentación adicional](#documentación-adicional)

## Descripción

La mayoría de los agricultores de paltos y cerezos en Chile riega de forma reactiva (por calendario o por observación visual), cuando el árbol ya muestra signos de estrés hídrico y el daño sobre la producción es, en parte, irreversible. AgroVox resuelve esto con un nodo de hardware instalado en el tronco o rama del árbol que:

1. Captura emisión acústica (cavitación en el xilema) con un disco piezoeléctrico.
2. Clasifica el evento en el propio microcontrolador (ESP32) usando un modelo TinyML cuantizado, sin depender de conectividad constante.
3. Transmite el evento clasificado vía LoRa a un Gateway.
4. El backend evalúa el evento contra los umbrales de vulnerabilidad hídrica P50/P88 y, si corresponde, genera una alerta.
5. La alerta llega al agricultor por WhatsApp, en lenguaje simple, sin necesidad de interpretar gráficos o métricas técnicas.

A diferencia de alternativas satelitales (indirectas y de reacción tardía) o sensores invasivos de alto costo (como FloraPulse), AgroVox mide el evento físico directamente, sin perforar la planta, a una fracción del costo.

## Tecnologías

| Capa | Tecnologías |
|---|---|
| Percepción y Borde | ESP32, disco piezoeléctrico, preamplificador OPA365, panel solar, TensorFlow Lite Micro (TinyML) |
| Red | LoRa, Gateway LoRa–MQTT |
| Cloud y Backend | Node.js / Python, PostgreSQL, API REST |
| Frontend | Dashboard Web de administración |
| Notificaciones | WhatsApp Business API |
| IA / Modelado | Python, TensorFlow/Keras, scikit-learn, cuantización int8 |

## Arquitectura

El sistema se organiza en 3 capas:

1. **Percepción y Borde**: nodo ESP32 + sensor piezoeléctrico + modelo TinyML embebido.
2. **Red**: Gateway que traduce LoRa a MQTT para el backend.
3. **Cloud y Backend**: API, controlador de eventos, servicio de alertas, repositorio de datos, PostgreSQL, Dashboard Web y servicio de WhatsApp.

Ver diagrama completo en [`Fase 2/Evidencias Proyecto/Evidencias de documentacion/diagramas/`](Fase 2/Evidencias Proyecto/Evidencias de documentacion/diagramas/).

## Ejecución local

### Pipeline de Inteligencia Artificial (TinyML)

Requiere Python 3.11 (TensorFlow no es compatible con 3.12/3.13 al momento de este proyecto).

```bash
cd "Fase 2/Evidencias Proyecto/Evidencias de sistema/Aplicacion/agrovox_ia"
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt   # o: pip install tensorflow numpy scipy scikit-learn

python generar_datos_sinteticos.py
python extraer_features.py
python entrenar_modelo.py
python convertir_a_c_array.py
python probar_modelo.py
```

Esto genera `modelo_agrovox.h`, el header en C listo para compilar en el firmware del ESP32.

### Base de datos (PostgreSQL / Supabase)

1. Crear un proyecto en [Supabase](https://supabase.com).
2. Abrir el SQL Editor y ejecutar el script completo: [`Fase 2/Evidencias Proyecto/Evidencias de sistema/Base de datos/agrovox_schema.sql`](Fase 2/Evidencias Proyecto/Evidencias de sistema/Base de datos/agrovox_schema.sql).
3. Esto crea las 6 tablas núcleo, los índices, datos de ejemplo y una consulta de prueba de lectura.

## Integrantes y roles

| Integrante | Rol principal |
|---|---|
| Pablo Vargas | Hardware, firmware (ESP32) e Inteligencia Artificial (TinyML) |
| Alonso Campusano | Backend, base de datos, Dashboard e integración WhatsApp |

Ambos integrantes participan en conjunto en las pruebas integrales y en la preparación de la presentación final.

## Metodología

El proyecto se desarrolla bajo una metodología ágil (Scrum adaptado a un proyecto mixto de hardware y software), con 7 sprints alineados al Plan de Trabajo y la Carta Gantt. El detalle completo de los artefactos se encuentra en [`Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/`](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/):

- [Metodología declarada y justificada](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/01_metodologia_declarada_y_justificada.md)
- [Product Vision](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/02_product_vision.md)
- [Product Backlog](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/03_product_backlog.md)
- [Sprint Backlog](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/04_sprint_backlog.md)
- [Definition of Done](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/05_definition_of_done.md)
- [Retrospectivas](Fase 2/Evidencias Proyecto/Evidencias de documentacion/metodologia/06_retrospectivas.md)

## Modelo de datos

Ver [`Fase 2/Evidencias Proyecto/Evidencias de documentacion/modelo_datos.md`](Fase 2/Evidencias Proyecto/Evidencias de documentacion/modelo_datos.md) para el modelo entidad-relación y la justificación de cada tabla. Script ejecutable en [`Fase 2/Evidencias Proyecto/Evidencias de sistema/Base de datos/agrovox_schema.sql`](Fase 2/Evidencias Proyecto/Evidencias de sistema/Base de datos/agrovox_schema.sql).

## Diagramas

Todos los diagramas (fuente editable + imagen renderizada) están en [`Fase 2/Evidencias Proyecto/Evidencias de documentacion/diagramas/`](Fase 2/Evidencias Proyecto/Evidencias de documentacion/diagramas/):

- Diagrama de Componentes (arquitectura de 3 capas)
- Diagrama de Estado (ciclo de vida del nodo)
- Diagrama BPMN (proceso de detección y alerta, con manejo de errores de LoRa y WhatsApp)
- Diagramas de Casos de Uso (por actor: Nodo, Investigador, Equipo AgroVox, Agricultor)

## Documentación adicional

- Fuentes científicas que respaldan la detección acústica de cavitación: `Fuentes_AgroVox.docx`
- Informes de Fase 2 (Avance, Final, Autoevaluación): carpeta `Fase 2/`
