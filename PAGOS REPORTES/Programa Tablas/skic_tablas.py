import pandas as pd
from datetime import datetime

# Cargar archivo
archivo_path = "skic.xlsx"  # Ajusta el nombre si es necesario
df = pd.read_excel(archivo_path)

# Convertir columna de fecha a datetime
df["Fecha Recepción"] = pd.to_datetime(df["Fecha Recepción"], dayfirst=True, errors="coerce")

# Obtener fecha actual
fecha_actual = datetime.today().date()

# Filtrar solo los registros con la fecha actual (sin hora)
df = df[df["Fecha Recepción"].dt.date == fecha_actual]

# Eliminar filas con recuperación = 0
df = df[df["Recuperación por Gestión"] != 0]

# Eliminar duplicados si se repite el CU y el importe es el mismo
df = df.drop_duplicates(subset=["CU Completo", "Recuperación por Gestión"])

# Guardar resultado
df.to_excel("skic_filtrado.xlsx", index=False)

print("Filtrado y limpieza completados. Archivo guardado como 'reporte_filtrado_sin_duplicados.xlsx'.")
