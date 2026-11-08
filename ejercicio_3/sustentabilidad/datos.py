"""Origen de datos del panel.

Aquí se simula el historial de consumos. En un sistema real esta función
consultaría la base de datos (ORM de Django) o una API de los medidores.
"""


def obtener_historial_consumos():
    return [
        {"planta": "Planta Norte", "consumo_kwh": 1200},
        {"planta": "Planta Sur", "consumo_kwh": 950},
        {"planta": "Planta Este", "consumo_kwh": 1800},
        {"planta": "Planta Norte", "consumo_kwh": 300},
    ]
