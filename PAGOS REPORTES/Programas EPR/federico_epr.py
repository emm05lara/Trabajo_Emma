import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CARGA DE DATOS ---
df = pd.read_excel('federico.xlsx', sheet_name='Pagos Despacho 61073')

# --- 2. LIMPIEZA DE FECHAS Y FILTRO DE SEMANA 26 ---
df['Fecha'] = pd.to_datetime(df['Fecha Recepción'], format='%d/%m/%Y %H:%M:%S').dt.date
fecha_inicio = datetime.strptime('04/08/2025', '%d/%m/%Y').date()
fecha_fin = datetime.strptime('10/08/2025', '%d/%m/%Y').date()
df_semana26 = df[(df['Fecha'] >= fecha_inicio) & (df['Fecha'] <= fecha_fin)].copy()

# Mapear días de la semana a español
dias_espanol = {
    'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
    'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}
df_semana26['Día de la Semana'] = pd.to_datetime(df_semana26['Fecha']).dt.day_name().map(dias_espanol)

# --- 3. PARÁMETROS DE EPR ---
cuentas_por_segmento = {
    'Extrajudicial - 0 a 28 semanas de atraso': 579,
    'Extrajudicial - 29 a 39 semanas de atraso': 4,
    'Extrajudicial - 40 a 55 semanas de atraso': 528,
    'Mas 55 semanas de atraso': 2296
}

epr_ideal = {
    'Extrajudicial - 0 a 28 semanas de atraso': 76,
    'Extrajudicial - 29 a 39 semanas de atraso': 1119,
    'Extrajudicial - 40 a 55 semanas de atraso': 7,
    'Mas 55 semanas de atraso': 9
}

# --- 4. CÁLCULO DE EPR ALCANZADO ---
total_por_segmento = df_semana26.groupby('Segmento')['Recuperación por Gestión'].sum().reset_index()
total_por_segmento['EPR Alcanzado'] = total_por_segmento.apply(
    lambda x: x['Recuperación por Gestión'] / cuentas_por_segmento.get(x['Segmento'], 1), axis=1)
total_por_segmento['EPR Ideal'] = total_por_segmento['Segmento'].map(epr_ideal)

print("\n🔹 EPR por Segmento:")
print(total_por_segmento[['Segmento', 'Recuperación por Gestión', 'EPR Ideal', 'EPR Alcanzado']])

# --- 5, 6 y 7. GRÁFICOS POR SEGMENTO ---
orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

for segmento in cuentas_por_segmento.keys():
    df_segmento = df_semana26[df_semana26['Segmento'] == segmento].copy()

    if df_segmento.empty:
        print(f"\n⚠️ No hay datos para el segmento: {segmento}")
        continue

    total_por_dia = df_segmento.groupby('Día de la Semana')['Recuperación por Gestión'].sum().reset_index()
    total_por_dia['Día de la Semana'] = pd.Categorical(total_por_dia['Día de la Semana'], categories=orden_dias, ordered=True)
    total_por_dia = total_por_dia.sort_values('Día de la Semana')

    # Calcular cuotas
    epr_diario = epr_ideal[segmento] / 7
    cuota_diaria = cuentas_por_segmento[segmento] * epr_diario
    cuota_semanal = cuentas_por_segmento[segmento] * epr_ideal[segmento]
    total_por_dia['Recuperación Acumulada'] = total_por_dia['Recuperación por Gestión'].cumsum()

    # --- Gráfico 1: Diario con Plotly ---
    fig1 = px.line(total_por_dia,
                   x='Día de la Semana',
                   y='Recuperación por Gestión',
                   text='Recuperación por Gestión',
                   title=f"📈 Recuperación Diaria vs Cuota - {segmento}",
                   markers=True)

    fig1.update_traces(
        texttemplate="$%{y:,.0f}",
        textposition="top center",
        line=dict(color='blue', width=3),
        marker=dict(size=10)
    )

    fig1.add_hline(y=cuota_diaria,
                   line_dash="dash",
                   line_color="red",
                   annotation_text=f"Cuota diaria: ${cuota_diaria:,.0f}",
                   annotation_position="top right")

    fig1.update_layout(
        yaxis_title="Recuperación por Gestión ($)",
        xaxis_title="Día de la Semana",
        yaxis_tickformat="$.0f",  # Formato en eje Y
        legend_title=None,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig1.show()

    # --- Gráfico 2: Acumulado con Plotly ---
    fig2 = px.line(total_por_dia,
                   x='Día de la Semana',
                   y='Recuperación Acumulada',
                   text='Recuperación Acumulada',
                   title=f"📊 Recuperación Acumulada vs Cuota Semanal - {segmento}",
                   markers=True)

    fig2.update_traces(
        texttemplate="$%{y:,.0f}",
        textposition="top center",
        line=dict(color='green', width=3),
        marker=dict(size=10)
    )

    fig2.add_hline(y=cuota_semanal,
                   line_dash="dash",
                   line_color="orange",
                   annotation_text=f"Cuota semanal: ${cuota_semanal:,.0f}",
                   annotation_position="top right")

    fig2.update_layout(
        yaxis_title="Recuperación Acumulada ($)",
        xaxis_title="Día de la Semana",
        yaxis_tickformat="$.0f",  # Formato en eje Y
        legend_title=None,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig2.show()

    # --- Gráfico 3: Barra Acumulativa animada ---
    acumulado_barras = total_por_dia[['Día de la Semana', 'Recuperación por Gestión']].copy()
    acumulado_barras['Recuperación Acumulada'] = acumulado_barras['Recuperación por Gestión'].cumsum()
    acumulado_barras['Día Num'] = range(1, len(acumulado_barras) + 1)

    acumulado_barras['Color'] = acumulado_barras['Recuperación Acumulada'].apply(
        lambda x: 'seagreen' if x >= cuota_semanal else 'crimson'
    )

    fig3 = px.bar(acumulado_barras,
                  x='Recuperación Acumulada',
                  y='Día de la Semana',
                  orientation='h',
                  animation_frame='Día Num',
                  text='Recuperación Acumulada',
                  title=f"🧱 Progreso Acumulativo - {segmento}",
                  color='Color',
                  color_discrete_map='identity')

    fig3.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition='outside'
    )

    fig3.update_layout(
        xaxis_title='Recuperación Acumulada ($)',
        yaxis_title='Día de la Semana',
        xaxis_tickformat="$.0f",  # Formato en eje X
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=60, r=60, t=60, b=40)
    )

    fig3.add_vline(x=cuota_semanal,
               line_dash="dash",
               line_color="orange",
               annotation_text=f"🎯 Cuota semanal: ${cuota_semanal:,.0f}",
               annotation_position="top right")
               
    fig3.show()