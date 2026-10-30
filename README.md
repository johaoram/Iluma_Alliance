# Iluma_Alliance
Proyecto para presentar pruebas técnicas en proceso de selección en Iluma Alliance.

# 🚀 ETL Pipeline: Ingesta y Normalización de Ofertas de Empleo (Data Jobs)

Pipeline de datos modular desarrollado en Python y Docker para la ingesta, limpieza, procesamiento y estructuración de datos de empleos tecnológicos desde archivos locales (CSV) hacia una base de datos relacional PostgreSQL.

---

## 🏗️ Arquitectura del Proyecto

El proyecto implementa un flujo ETL por capas modularizado:

1. **Capa Raw / Bronze (`raw` schema):** Lectura e ingesta directa de los datos en bruto desde el archivo CSV local (`data_jobs.csv` en Descargas) a la base de datos sin alterar la estructura original.
2. **Capa Silver / 3NF (`silver` schema):** Transformación, normalización de textos, limpieza de datos, tipado estricto y estructuración en tablas dimensionales y de hechos bajo el modelo relacional de Tercera Forma Normal (3NF).

---

## 📂 Estructura del Repositorio

```text
mi_proyecto_etl/
│
├── source/
│   ├── database.py          # Conexión centralizada a PostgreSQL (SQLAlchemy)
│   ├── pipeline_raw.py      # Ingesta inicial desde CSV (Downloads) al esquema raw
│   └── pipeline_3nf.py      # Transformación y carga hacia la capa normalizada (Silver)
│
├── .env                     # Variables de entorno y credenciales (local)
├── docker-compose.yml       # Configuración y orquestación del contenedor PostgreSQL
├── README.md                # Documentación principal del repositorio
├── requirements.txt         # Dependencias y librerías del entorno de Python
```

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.12+
* **Procesamiento de datos:** Pandas
* **Base de datos & ORM:** PostgreSQL & SQLAlchemy (`psycopg2`)
* **Infraestructura:** Docker & Docker Compose
* **Gestión de variables:** `python-dotenv`

---

## ⚙️ Configuración e Instalación

### 1. Requisitos Previos
* Tener instalado [Docker Desktop](https://www.docker.com/) y asegurarse de que esté en ejecución.
* Tener instalado Python 3.12 o superior.

### 2. Configuración de Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto (asegurando guardarlo en codificación UTF-8) con las siguientes variables:

```env
DB_USER=postgres
DB_PASSWORD=TuPasswordSeguro
DB_NAME=data_jobs_db
DB_PORT=5432
DB_HOST=localhost
```

### 3. Instalación de Dependencias
Instala los paquetes necesarios listados en el proyecto:

```bash
pip install -r requirements.txt
```

### 4. Despliegue de la Base de Datos (Docker)
Inicia el servicio de PostgreSQL en segundo plano:

```bash
docker compose up -d
```

---

## 🚀 Ejecución del Pipeline

### Paso 1: Ingesta RAW (Bronze)
Asegúrate de que el archivo `data_jobs.csv` esté en tu carpeta local de **Descargas** (*Downloads*). Luego ejecuta:

```bash
python -m source.pipeline_raw
```

### Paso 2: Transformación y Carga Normalizada (Silver / 3NF)
Aplica las reglas de limpieza, normalización e inserción en el esquema estructurado ejecutando:

```bash
python -m source.pipeline_3nf
```

---

## 🔍 Verificación e Inspección de Datos

Puedes verificar el contenido cargado ingresando directamente a la consola interactiva de PostgreSQL en Docker:

```bash
docker exec -it data_jobs_postgres psql -U postgres -d data_jobs_db
```

Comandos útiles dentro de `psql`:
* `\l` : Listar bases de datos.
* `\dt raw.*` : Listar tablas del esquema RAW.
* `\dt silver.*` : Listar tablas del esquema Silver/3NF.
* `SELECT COUNT(*) FROM raw.data_jobs_raw;` : Contar registros cargados en crudo.
* `\q` : Salir de la consola.