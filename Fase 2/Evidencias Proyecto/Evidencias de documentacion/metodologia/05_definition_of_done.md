# 5. Definition of Done (DoD)

Como AgroVox combina hardware y software, se definieron criterios de "terminado" diferenciados por tipo de tarea, además de un criterio general aplicable a toda historia de usuario.

## DoD — Tareas de Hardware / Firmware
- [ ] El componente fue soldado/ensamblado y pasó inspección visual.
- [ ] El firmware fue cargado al microcontrolador sin errores de compilación.
- [ ] La funcionalidad fue probada al menos una vez en banco, no solo verificada en teoría.
- [ ] Se documentó el consumo energético o el comportamiento relevante observado durante la prueba.

## DoD — Tareas de Software / Backend / Dashboard
- [ ] El código fue versionado en el repositorio con un mensaje de commit descriptivo.
- [ ] La funcionalidad fue probada manualmente o mediante un script de prueba (ej. `probar_modelo.py`, simulador de Gateway).
- [ ] No rompe funcionalidad previamente existente (revisión básica de regresión).
- [ ] Está documentada mínimamente (comentarios en el código o README actualizado).
- [ ] Fue revisada por el otro integrante del equipo antes de darse por cerrada.

## DoD General (aplica a toda historia de usuario)
- [ ] Cumple el criterio de aceptación definido en el Product Backlog.
- [ ] Fue demostrada en la revisión de cierre del sprint entre ambos integrantes.
