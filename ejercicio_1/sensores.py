"""
Ejercicio 1 - Sanitización y análisis estadístico de sensores (EcoTech Solutions)

Ejecutar:  python sensores.py
"""

import re

UBICACION_POR_DEFECTO = "Sin ubicación"


def limpiar_registro_sensor(registro_raw):
    """Normaliza un registro crudo de sensor y devuelve un diccionario nuevo.

    - sensor_id: sin espacios sobrantes.
    - temperatura: float sin sufijo de unidad (None si falta o es inválida).
    - ubicacion: valor por defecto seguro si no fue registrada.
    """
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    temperatura = None
    bruto = registro_raw.get("temperatura")
    if bruto is not None:
        if isinstance(bruto, (int, float)):
            temperatura = float(bruto)
        else:
            # Extrae el número (con signo y decimales) ignorando la unidad: "24.5C", " 30 °C"
            coincidencia = re.search(r"-?\d+(?:[.,]\d+)?", str(bruto))
            if coincidencia:
                temperatura = float(coincidencia.group().replace(",", "."))

    ubicacion = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion).strip() if ubicacion is not None else ""
    if not ubicacion:
        ubicacion = UBICACION_POR_DEFECTO

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve la tupla (lista_sensores_alerta, promedio_temperatura).

    Un sensor está en alerta si su temperatura supera estrictamente el umbral.
    Los registros sin temperatura válida se ignoran. Si no hay lecturas
    válidas, el promedio es 0.0.
    """
    validos = [s for s in lista_sensores_limpios if s.get("temperatura") is not None]
    lista_sensores_alerta = [
        s["sensor_id"] for s in validos if s["temperatura"] > umbral_temperatura
    ]
    promedio_temperatura = (
        sum(s["temperatura"] for s in validos) / len(validos) if validos else 0.0
    )
    return lista_sensores_alerta, promedio_temperatura


def main():
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.2 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": "  SENSOR-003", "temperatura": "28C"},
        {"sensor_id": "SENSOR-004 ", "temperatura": "35.8C", "ubicacion": "   "},
        {"sensor_id": "SENSOR-005", "temperatura": "error"},
    ]

    # 1) Limpieza de los registros crudos
    limpios = [limpiar_registro_sensor(r) for r in registros_crudos]

    # 2) Resumen estadístico
    umbral = 30.0
    alertas, promedio = generar_resumen_sensores(limpios, umbral)

    # 3) Reporte formateado
    print("=" * 56)
    print("REPORTE DE SENSORES - ECOTECH SOLUTIONS")
    print("=" * 56)
    print(f"{'ID':<12}{'Temp (°C)':>10}  Ubicación")
    print("-" * 56)
    for s in limpios:
        temp = f"{s['temperatura']:.1f}" if s["temperatura"] is not None else "N/D"
        print(f"{s['sensor_id']:<12}{temp:>10}  {s['ubicacion']}")
    print("-" * 56)
    print(f"Umbral de alerta      : {umbral:.1f} °C")
    print(f"Sensores en alerta    : {', '.join(alertas) if alertas else 'ninguno'}")
    print(f"Promedio de la planta : {promedio:.2f} °C")


if __name__ == "__main__":
    main()
