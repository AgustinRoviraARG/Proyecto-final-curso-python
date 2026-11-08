"""Lógica de negocio: cálculo de huella de carbono y métricas por planta."""


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Devuelve las emisiones de CO2 (kg) = consumo (kWh) * factor de emisión.

    Lanza ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """Procesa un historial de consumos por planta industrial.

    `registros` es una lista de diccionarios con la forma
        {"planta": "Planta Norte", "consumo_kwh": 1200}
    Una misma planta puede aparecer varias veces: sus consumos se acumulan.

    Devuelve un diccionario con:
        total_emisiones       -> emisiones globales (kg CO2)
        planta_mayor_consumo  -> nombre de la planta con más consumo (None si no hay datos)
        consumo_por_planta    -> {planta: kWh acumulados}
        emisiones_por_planta  -> {planta: kg CO2}
    """
    consumo_por_planta = {}
    for registro in registros:
        planta = registro["planta"]
        consumo_por_planta[planta] = (
            consumo_por_planta.get(planta, 0) + registro["consumo_kwh"]
        )

    emisiones_por_planta = {
        planta: calcular_emisiones_carbono(consumo)
        for planta, consumo in consumo_por_planta.items()
    }

    planta_mayor_consumo = (
        max(consumo_por_planta, key=consumo_por_planta.get)
        if consumo_por_planta
        else None
    )

    return {
        "total_emisiones": sum(emisiones_por_planta.values()),
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_por_planta": consumo_por_planta,
        "emisiones_por_planta": emisiones_por_planta,
    }
