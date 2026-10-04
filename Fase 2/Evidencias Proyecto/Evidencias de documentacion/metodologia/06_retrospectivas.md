# 6. Retrospectivas

Formato utilizado al cierre de cada sprint: tres preguntas simples que generan acciones concretas para el siguiente ciclo, no solo una lista de quejas o logros.

## Formato

| Pregunta | Respuesta |
|---|---|
| ¿Qué funcionó bien? | |
| ¿Qué no funcionó o se puede mejorar? | |
| ¿Qué acción concreta tomamos para el próximo sprint? | |

*(Se completa al cierre real de cada sprint, con la experiencia concreta del equipo.)*

## Ejemplo — Retrospectiva Sprint 1 (Ensamblaje de Hardware)

| Pregunta | Respuesta |
|---|---|
| ¿Qué funcionó bien? | La captura de señal por puerto serie se validó sin problemas una vez montado el circuito; el firmware base del ESP32 no presentó errores de compilación. |
| ¿Qué no funcionó o se puede mejorar? | Se detectó ruido eléctrico en el preamplificador que distorsionaba la lectura inicial del piezoeléctrico, retrasando la validación en banco. |
| ¿Qué acción concreta tomamos para el próximo sprint? | Reemplazar el LM358 por el OPA365 (mayor ancho de banda y menor ruido) antes de iniciar la recolección de datos del Sprint 2, para no arrastrar el problema a la etapa de entrenamiento del modelo. |

> Agregar aquí la retrospectiva de cada sprint siguiente (2 a 7) a medida que se cierran, siguiendo el mismo formato de 3 preguntas.
