# Modelo de Datos — AgroVox

Base de datos relacional, implementada en **PostgreSQL** (hospedada en **Supabase**). Contiene 6 tablas núcleo que cubren el ciclo completo: predio → sector de riego → agricultor, y nodo → evento acústico → alerta.

Script ejecutable completo: [`agrovox_schema.sql`](schema/agrovox_schema.sql).

## Diagrama entidad-relación (resumen)

```
Predio (1) ──< SectorRiego (N)
Predio (1) ──< Agricultor (N)
SectorRiego (1) ──< Nodo (N)
Nodo (1) ──< EventoAcustico (N)
EventoAcustico (1) ──< Alerta (N) >── Agricultor (1)
```

## Tablas

### 1. Predio
Representa el fundo o terreno agrícola. Es la entidad raíz: todo sector de riego y agricultor está asociado a un predio.

| Campo | Tipo | Descripción |
|---|---|---|
| id_predio | SERIAL PK | Identificador único |
| nombre | VARCHAR(100) | Nombre del fundo |
| rut_propietario | VARCHAR(12) | RUT del propietario |
| ubicacion_lat / ubicacion_lng | DECIMAL(9,6) | Coordenadas geográficas |
| superficie_ha | DECIMAL(6,2) | Superficie en hectáreas |
| cultivo_principal | VARCHAR(30) | Palto o Cerezo |
| fecha_registro | TIMESTAMP | Fecha de alta en el sistema |

### 2. SectorRiego
Subdivisión del predio por variedad o zona de riego. Permite que un mismo predio tenga múltiples sectores con distintas necesidades hídricas.

| Campo | Tipo | Descripción |
|---|---|---|
| id_sector | SERIAL PK | Identificador único |
| id_predio | INT FK → Predio | Predio al que pertenece |
| nombre | VARCHAR(50) | Nombre del sector |
| poligono_geojson | JSONB | Geometría del sector (opcional) |
| variedad | VARCHAR(50) | Ej. Hass |
| superficie_ha | DECIMAL(6,2) | Superficie del sector |

### 3. Agricultor
Usuario final que recibe las alertas por WhatsApp.

| Campo | Tipo | Descripción |
|---|---|---|
| id_agricultor | SERIAL PK | Identificador único |
| id_predio | INT FK → Predio | Predio que administra |
| nombre | VARCHAR(100) | Nombre del agricultor |
| telefono_whatsapp | VARCHAR(15) | Número de contacto para alertas |
| email | VARCHAR(100) | Correo de contacto |
| fecha_registro | TIMESTAMP | Fecha de alta |

### 4. Nodo
Dispositivo físico (ESP32 + sensor) instalado en el tronco o rama del árbol.

| Campo | Tipo | Descripción |
|---|---|---|
| id_nodo | SERIAL PK | Identificador único |
| codigo_serie | VARCHAR(50) UNIQUE | Identificador físico del dispositivo |
| id_sector | INT FK → SectorRiego | Sector donde está instalado |
| latitud / longitud | DECIMAL(9,6) | Ubicación exacta del nodo |
| fecha_instalacion | DATE | Fecha de instalación en campo |
| estado | VARCHAR(20) | activo / mantenimiento / desconectado |
| nivel_bateria | INT (0–100) | Nivel de batería reportado |
| ultima_conexion | TIMESTAMP | Última vez que el nodo transmitió |
| version_firmware | VARCHAR(20) | Versión de firmware instalada |

### 5. EventoAcustico
Cada evento capturado y clasificado por el modelo TinyML embebido en el nodo.

| Campo | Tipo | Descripción |
|---|---|---|
| id_evento | SERIAL PK | Identificador único |
| id_nodo | INT FK → Nodo | Nodo que generó el evento |
| timestamp_evento | TIMESTAMP | Momento de la captura |
| conteo_pulsos | INT | Número de pulsos acústicos detectados |
| nivel_estres_estimado | DECIMAL(5,2) | Estimación de estrés hídrico (%) |
| nivel_confianza | DECIMAL(4,2) (0–1) | Confianza del modelo en la clasificación |
| procesado_edge_ai | BOOLEAN | Si fue clasificado en el borde (ESP32) o no |

### 6. Alerta
Notificación generada y enviada al agricultor cuando un evento supera el umbral P50/P88.

| Campo | Tipo | Descripción |
|---|---|---|
| id_alerta | SERIAL PK | Identificador único |
| id_evento | INT FK → EventoAcustico | Evento que originó la alerta |
| id_agricultor | INT FK → Agricultor | Destinatario |
| tipo_alerta | VARCHAR(30) | Ej. riego_urgente |
| mensaje | TEXT | Texto enviado al agricultor |
| canal | VARCHAR(20) | whatsapp (por defecto) |
| fecha_envio | TIMESTAMP | Momento del envío |
| estado_lectura | VARCHAR(20) | enviado / leído |

## Justificación del diseño

- Se separó **Predio** de **SectorRiego** porque un mismo fundo puede tener múltiples variedades o zonas con necesidades de riego distintas, y las alertas deben poder generarse a nivel de sector, no solo de predio completo.
- **Nodo** se modeló independiente de **Agricultor** (y asociado a **SectorRiego**) porque el nodo es un activo físico que puede sobrevivir a cambios de propietario o de agricultor asignado.
- **EventoAcustico** y **Alerta** se separaron en dos tablas porque no todo evento genera una alerta (solo los que superan el umbral P50/P88); esto permite mantener el historial completo de eventos para análisis posterior, aunque no todos hayan sido notificados.
- Los índices (`idx_evento_nodo`, `idx_evento_timestamp`, `idx_alerta_agricultor`, `idx_nodo_sector`) se definieron sobre las columnas usadas en las consultas más frecuentes del Dashboard (historial de eventos por nodo, ordenado por fecha).

## Prueba de escritura y lectura

El script [`agrovox_schema.sql`](schema/agrovox_schema.sql) incluye datos de ejemplo (`INSERT`) y una consulta de prueba (`SELECT ... JOIN`) que trae el historial de eventos de un nodo junto con su alerta asociada, validando que el modelo soporta tanto escritura como lectura relacional.
