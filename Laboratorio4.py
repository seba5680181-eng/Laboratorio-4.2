# Laboratorio IV.2 - Análisis de datos de telemetría de un nodo IoT
# Integrantes: Cristian  Vallejos Sebastian - Toftum Cristian
# URL del repositorio: https://github.com/seba5680181-eng/Laboratorio-4.2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# 1. CARGAMOS  LOS DATOS

archivo = "telemetria_nodo_iot.csv"

datos = pd.read_csv(
    archivo,
    parse_dates=["timestamp"]
)

datos.set_index("timestamp", inplace=True)

print("Datos cargados correctamente.")
print(datos.head())

print("\nCantidad de registros:", len(datos))


# 2. ESTADÍSTICAS DESCRIPTIVAS


estadisticas = datos.describe().loc[
    ["mean", "min", "max", "std"]
]

print("\nEstadísticas descriptivas:")
print(estadisticas)

# 3. DETECCIÓN DE ALERTAS


# Convertir los datos a arrays de NumPy
voltaje = datos["voltaje_bateria_V"].to_numpy()
rssi = datos["rssi_dbm"].to_numpy()

# Criterios de alerta
alerta_bateria = voltaje < 3.5
alerta_rssi = rssi < -85

# Alerta general: batería baja O señal débil
alerta = alerta_bateria | alerta_rssi

# Cantidad de alertas
cantidad_bateria = np.sum(alerta_bateria)
cantidad_rssi = np.sum(alerta_rssi)
cantidad_alertas = np.sum(alerta)

print("\nAlertas:")
print("Batería baja:", cantidad_bateria)
print("Señal débil:", cantidad_rssi)
print("Al menos una alerta:", cantidad_alertas)

# 4. GRÁFICO DE TELEMETRÍA Y ALERTAS


plt.figure(figsize=(12, 6))

# Temperatura
plt.plot(
    datos.index,
    datos["temperatura_C"],
    label="Temperatura (°C)"
)

# Voltaje de batería
plt.plot(
    datos.index,
    datos["voltaje_bateria_V"],
    label="Voltaje batería (V)"
)

# Marcar los momentos donde hubo alguna alerta
datos_alerta = datos[alerta]

plt.scatter(
    datos_alerta.index,
    datos_alerta["temperatura_C"],
    marker="x",
    label="Alerta"
)

plt.xlabel("Fecha y hora")
plt.ylabel("Valor")
plt.title("Evolución temporal de la telemetría")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# Agrupo dia por dia y saco el resumen con las metricas minimas (punto 5)
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

# exporto al excel en la hoja que pide el tp (requiere openpyxl)
resumen_diario.to_excel("resumen_telemetria_diario.xlsx", sheet_name="Resumen diario")
print("Listo, se guardó el archivo excel.")


