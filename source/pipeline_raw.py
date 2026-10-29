import os
import pandas as pd
from source.database import get_engine

# Obtener la ruta dinámica de la carpeta Descargas del usuario actual
USER_HOME = os.path.expanduser("~")
CSV_PATH = os.path.join(USER_HOME, "Downloads", "data_jobs.csv")

def run_raw_ingestion():
    """Lee el CSV desde la carpeta Descargas y lo carga en bruto en la tabla raw.data_jobs_raw"""
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encontró el archivo 'data_jobs.csv' en Descargas: {CSV_PATH}")
        print("💡 Asegúrate de que el archivo esté en tu carpeta Downloads.")
        return False

    print(f"📂 Leyendo archivo CSV desde Descargas: {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    engine = get_engine()
    print("📥 Conectando a PostgreSQL e insertando datos en la tabla `raw.data_jobs_raw`...")
    
    df.to_sql("data_jobs_raw", con=engine, schema="raw", if_exists="replace", index=False)
    
    print(f"✅ ¡Ingestión RAW exitosa! Se cargaron {len(df)} registros en PostgreSQL.")
    return True