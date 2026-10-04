# 4. Sprint Backlog

Los 7 sprints coinciden exactamente con las actividades y duraciones ya definidas en el Plan de Trabajo y la Carta Gantt del proyecto, de modo que ambos documentos sean consistentes entre sí.

## Sprint 1 — Ensamblaje de Hardware (Semanas 1-2)
- **Objetivo del Sprint:** Tener el nodo físico armado y capturando señal cruda.
- **Product Backlog Items:** PB-01
- **Tareas técnicas:** Soldar componentes en PCB; conectar ESP32, disco piezoeléctrico y panel solar; flashear firmware base; validar captura de señal por puerto serie.
- **Responsable:** Pablo (principal), Alonso (apoyo)

## Sprint 2 — Recolección de Datos y Entrenamiento IA (Semanas 3-5)
- **Objetivo del Sprint:** Tener un primer modelo TinyML entrenado y validado localmente.
- **Product Backlog Items:** PB-02, PB-13, PB-15 (inicio)
- **Tareas técnicas:** Generar/recolectar dataset; extraer features; entrenar y cuantizar el modelo; validar con `probar_modelo.py`.
- **Responsable:** Pablo (principal), Alonso (apoyo)

## Sprint 3 — Backend y Gateway LoRa (Semanas 6-8)
- **Objetivo del Sprint:** El nodo transmite y el backend registra eventos reales en la base de datos.
- **Product Backlog Items:** PB-03, PB-04, PB-05, PB-06
- **Tareas técnicas:** Configurar Gateway/ChirpStack; implementar `POST /eventos` y `GET /nodos`; conectar a PostgreSQL (Supabase).
- **Responsable:** Alonso (principal), Pablo (apoyo)

## Sprint 4 — Dashboard de Administración (Semanas 9-11)
- **Objetivo del Sprint:** El Equipo AgroVox puede ver el estado de los nodos desde una interfaz web.
- **Product Backlog Items:** PB-09, PB-10
- **Tareas técnicas:** Construir vista de lista de nodos; consumir el endpoint de lectura; mostrar batería y estado de conexión.
- **Responsable:** Alonso (principal), Pablo (apoyo)

## Sprint 5 — Integración WhatsApp (Semanas 12-13)
- **Objetivo del Sprint:** La alerta llega realmente al celular del agricultor.
- **Product Backlog Items:** PB-07, PB-08, PB-11, PB-12
- **Tareas técnicas:** Configurar Meta for Developers; implementar el webhook de envío; lógica de reintento de notificación.
- **Responsable:** Alonso (principal), Pablo (apoyo)

## Sprint 6 — Pruebas Integrales (Semanas 14-16)
- **Objetivo del Sprint:** Validar el flujo completo de extremo a extremo y recoger evidencia con usuarios reales.
- **Product Backlog Items:** PB-14, validación cruzada de PB-01 a PB-12
- **Tareas técnicas:** Simulador de Gateway; pruebas de extremo a extremo; formulario de validación con agricultores y agrónomos.
- **Responsable:** Pablo y Alonso, en conjunto

## Sprint 7 — Preparación y Cierre (Semanas 17-18)
- **Objetivo del Sprint:** Informe final, presentación y cierre documentado del proyecto.
- **Product Backlog Items:** Documentación general
- **Tareas técnicas:** Redacción del informe final; ensayo del pitch; retrospectiva general del proyecto.
- **Responsable:** Pablo y Alonso, en conjunto
