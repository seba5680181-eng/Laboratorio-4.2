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
# ==========================================
# 3. DETECCIÓN DE ALERTAS
# ==========================================

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