# Laboratorio IV.2 - Análisis de datos de telemetría de un nodo IoT
# Integrantes: Cristian  Vallejos Sebastian - Toftum Cristian
# URL del repositorio: https://github.com/seba5680181-eng/Laboratorio-4.2
# Necesario tener descargado openpyxl

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Levantamos el csv y usamos la columna timestamp como indice del dataframe
df = pd.read_csv("telemetria_nodo_iot.csv", parse_dates=["timestamp"])
df = df.set_index("timestamp")

# Separamos las columnas numericas que pide la consigna
variables = ["temperatura_C", "humedad_pct", "voltaje_bateria_V", "rssi_dbm"]

# Armamos el dataframe con las estadisticas descriptivas (punto 2 del laboratorio)
estadisticas = pd.DataFrame({
    "media": df[variables].mean(),
    "minimo": df[variables].min(),
    "maximo": df[variables].max(),
    "desvio_estandar": df[variables].std()
})

print("--- Estadísticas Descriptivas ---")
print(estadisticas, "\n")

# Convertimos a numpy array para hacer las mascaras booleanas (punto 3 del laboratorio)
voltaje = df["voltaje_bateria_V"].to_numpy()
rssi = df["rssi_dbm"].to_numpy()

# Criterios para las alertas: bateria baja o señal debil
alerta_bateria = voltaje < 3.5
alerta_rssi = rssi < -85
alerta = alerta_bateria | alerta_rssi  # con que salte una ya cuenta

print("--- Resumen de Alertas ---")
print(f"Batería baja: {np.sum(alerta_bateria)}")
print(f"Señal débil: {np.sum(alerta_rssi)}")
print(f"Total de alertas (al menos una): {np.sum(alerta)}\n")

# Metemos la columna nueva al df original para tenerla a mano al graficar
df["alerta"] = alerta

# Armamos el grafico de la evolucion temporal
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["temperatura_C"], label="Temp (°C)")
plt.plot(df.index, df["voltaje_bateria_V"], label="Voltaje (V)")

# Usamos un scatter arriba para marcar con una cruz roja donde hubo alertas
plt.scatter(
    df.index[df["alerta"]],
    df.loc[df["alerta"], "temperatura_C"],
    color="red",
    marker="x",
    label="Alerta detectada"
)

plt.xlabel("Fecha y hora")
plt.ylabel("Valores medidos")
plt.title("Evolución de Temperatura y Voltaje")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# Agrupamos dia por dia y saco el resumen con las metricas minimas (punto 5 del laboratorio)
resumen_diario = df.groupby(df.index.date).agg(
    temperatura_promedio=("temperatura_C", "mean"),
    temperatura_maxima=("temperatura_C", "max"),
    temperatura_minima=("temperatura_C", "min"),
    voltaje_bateria_promedio=("voltaje_bateria_V", "mean"),
    voltaje_bateria_minimo=("voltaje_bateria_V", "min"),
    cantidad_alertas=("alerta", "sum")
)

resumen_diario.index.name = "fecha"

print("--- Resumen Diario ---")
print(resumen_diario, "\n")

# Exportamos al excel en la hoja que pide el tp (NECESARIO AQUI TENER INSTALADO OPENPYXL COMO INDICAMOS EN PRINCIPIO)
resumen_diario.to_excel("resumen_telemetria_diario.xlsx", sheet_name="Resumen diario")
print("Listo, se guardó el archivo excel.")