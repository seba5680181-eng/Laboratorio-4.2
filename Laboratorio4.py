# Laboratorio IV.2 - Análisis de datos de telemetría de un nodo IoT
# Integrantes: Cristian  Vallejos Sebastian - Toftum Cristian
# URL del repositorio: 

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