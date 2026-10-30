import os
import pandas as pd
from source.database import get_engine

def run_3nf_transformation():
    """
    Lee los datos desde raw.data_jobs_raw, aplica la lógica de limpieza 
    y normalización, y los carga en un esquema estructurado (ej. 'silver').
    """
    print("📥 Conectando a PostgreSQL para extraer la capa RAW...")
    engine = get_engine()
    
    # 1. EXTRAER: Leer los datos crudos desde la base de datos
    query = "SELECT * FROM raw.data_jobs_raw;"
    try:
        df = pd.read_sql(query, con=engine)
    except Exception as e:
        print(f"❌ Error al leer la tabla raw: {e}")
        return False

    if df.empty:
        print("⚠️ Advertencia: La tabla raw.data_jobs_raw está vacía.")
        return False

    print(f"🔄 Procesando {len(df)} registros para la capa estructurada (3NF/Silver)...")

    # 2. TRANSFORMAR: Limpieza y Normalización
    # (Adapta estas operaciones según las columnas reales de tu CSV)
    
    # Ejemplo de limpieza general:
    # - Eliminar espacios en blanco en columnas de texto
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].str.strip()

    # - Manejo de nulos o duplicados
    df = df.drop_duplicates()

    # - Conversión de formatos (ejemplo: fechas o IDs si aplica)
    # df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'], errors='coerce')

    # (Opcional Avanzado 3NF): Si quieres dividir en tablas normalizadas, 
    # aquí puedes separar el DataFrame principal en tablas dimensionales (ej. empresas, ubicaciones)
    # y una tabla de hechos. Por ahora, una tabla limpia unificada es una excelente base "Silver".

    # 3. CARGAR: Guardar en el nuevo esquema estructurado
    target_schema = "silver"  # O puedes llamarlo 'model_3nf'
    target_table = "jobs_cleaned"

    print(f"📤 Cargando datos transformados en el esquema `{target_schema}`...")
    
    try:
        df.to_sql(target_table, con=engine, schema=target_schema, if_exists="replace", index=False)
        print(f"✅ ¡Transformación 3NF exitosa! Se cargaron {len(df)} registros limpios en `{target_schema}.{target_table}`.")
        return True
    except Exception as e:
        print(f"❌ Error al cargar los datos transformados: {e}")
        return False

if __name__ == "__main__":
    run_3nf_transformation()