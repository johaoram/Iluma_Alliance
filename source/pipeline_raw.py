import os
import pandas as pd
from source.database import get_engine  # O simplemente from database import get_engine dependiendo de tu estructura de imports

# Rutas relativas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data_jobs.csv")

def run_raw_ingestion():
    """Lee el CSV desde la raíz y lo carga en bruto en la tabla raw.data_jobs_raw"""
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: No se encontró el archivo 'data_jobs.csv' en la ruta: {CSV_PATH}")
        print("💡 Asegúrate de colocar el archivo CSV directamente en la raíz de tu proyecto.")
        return False

    print(f"📂 Leyendo archivo CSV desde la raíz: {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    engine = get_engine()
    print("📥 Conectando a PostgreSQL e insertando datos en la tabla `raw.data_jobs_raw`...")
    
    df.to_sql("data_jobs_raw", con=engine, schema="raw", if_exists="replace", index=False)
    
    print(f"✅ ¡Ingestión RAW exitosa! Se cargaron {len(df)} registros en PostgreSQL.")
    return True
