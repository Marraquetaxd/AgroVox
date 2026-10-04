# 3. Product Backlog

Historias de usuario priorizadas que representan el alcance completo del proyecto. La estimación usa puntos de historia (escala de Fibonacci: 1, 2, 3, 5, 8, 13) y la prioridad se revisa al cierre de cada sprint.

| ID | Épica | Historia de Usuario | Prioridad | Estimación |
|---|---|---|---|---|
| PB-01 | Captura acústica | Como investigador, quiero que el nodo capture la señal acústica del piezoeléctrico, para disponer de datos crudos de análisis. | Alta | 5 |
| PB-02 | Captura acústica | Como investigador, quiero clasificar el evento como cavitación o ruido usando TinyML embebido, para filtrar falsos positivos antes de transmitir. | Alta | 8 |
| PB-03 | Conectividad LoRa | Como sistema, quiero transmitir el evento clasificado vía LoRa al Gateway, para no depender de conectividad WiFi en campo. | Alta | 5 |
| PB-04 | Conectividad LoRa | Como sistema, quiero reintentar automáticamente la transmisión si falla, para no perder eventos críticos de estrés hídrico. | Media | 3 |
| PB-05 | Backend y datos | Como backend, quiero registrar cada evento recibido en PostgreSQL, para mantener un historial consultable por nodo. | Alta | 5 |
| PB-06 | Backend y datos | Como Dashboard, quiero consumir un endpoint de lectura por nodo, para mostrar datos reales y no simulados. | Alta | 3 |
| PB-07 | Lógica de alertas | Como backend, quiero evaluar si un evento supera el umbral P50/P88, para decidir si corresponde generar una alerta. | Alta | 5 |
| PB-08 | Lógica de alertas | Como backend, quiero reintentar el envío de una alerta si falla la entrega, para asegurar que el agricultor sea notificado. | Media | 3 |
| PB-09 | Dashboard admin | Como Equipo AgroVox, quiero ver el estado de batería y conexión de cada nodo, para dar soporte técnico a tiempo. | Media | 5 |
| PB-10 | Dashboard admin | Como Equipo AgroVox, quiero gestionar los sectores de riego desde el Dashboard, para administrar el huerto completo. | Baja | 8 |
| PB-11 | Notificación WhatsApp | Como agricultor, quiero recibir una alerta simple por WhatsApp, para saber cuándo regar sin interpretar datos técnicos. | Alta | 5 |
| PB-12 | Notificación WhatsApp | Como agricultor, quiero poder responder la alerta confirmando que regué, para que el sistema registre la acción tomada. | Baja | 5 |
| PB-13 | Validación IA | Como equipo de desarrollo, quiero comparar el modelo cuantizado contra el modelo completo, para validar que no se perdió precisión al optimizarlo. | Alta | 3 |
| PB-14 | Validación con usuarios | Como equipo de desarrollo, quiero validar el prototipo con agricultores reales mediante un formulario, para confirmar que la propuesta de valor es percibida como útil. | Alta | 5 |
| PB-15 | Datos reales | Como investigador, quiero reemplazar los datos sintéticos por grabaciones reales del sensor, para entrenar un modelo representativo del fenómeno físico real. | Alta | 8 |
