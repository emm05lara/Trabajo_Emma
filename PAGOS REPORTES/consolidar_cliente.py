import pandas as pd

# Cargar el archivo de Excel
file_path = "sam.xlsx"  # Asegúrate de colocar la ruta correcta
df = pd.read_excel(file_path)

# Sumar la "Recuperación por Gestión" por cliente único
recuperacion_por_cliente = df.groupby("CU Completo", as_index=False)["Recuperación por Gestión"].sum()

# Contar cuántos pagos tuvo cada cliente en la semana
pagos_por_cliente = df.groupby("CU Completo", as_index=False).size()
pagos_por_cliente = pagos_por_cliente.rename(columns={"size": "Pagos en la Semana"})

# Obtener la primera fecha de recepción por cliente
fecha_primera_recepcion = df.groupby("CU Completo", as_index=False)["Fecha Recepción"].min()

# Mantener solo la primera aparición de cada cliente único (sin alterar otros datos)
df_consolidado = df.drop_duplicates(subset=["CU Completo"], keep="first")

# Unir las sumas y el conteo de pagos a la tabla consolidada
df_consolidado = df_consolidado.merge(recuperacion_por_cliente, on="CU Completo", how="left", suffixes=("", "_Total"))
df_consolidado = df_consolidado.merge(pagos_por_cliente, on="CU Completo", how="left")
df_consolidado = df_consolidado.merge(fecha_primera_recepcion, on="CU Completo", how="left", suffixes=("", "_Primera"))

# Reemplazar la columna original de "Recuperación por Gestión" con la suma total
df_consolidado["Recuperación por Gestión"] = df_consolidado["Recuperación por Gestión_Total"]
df_consolidado.drop(columns=["Recuperación por Gestión_Total"], inplace=True)

# Guardar el nuevo archivo de Excel con los datos consolidados
output_file = "sam_Consolidado.xlsx"
df_consolidado.to_excel(output_file, index=False)

print(f"Archivo consolidado guardado como: {output_file}")
