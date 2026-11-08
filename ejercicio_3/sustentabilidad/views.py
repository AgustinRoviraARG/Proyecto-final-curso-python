from django.shortcuts import render

from .datos import obtener_historial_consumos
from .emisiones import obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    """Calcula las métricas y renderiza sustentabilidad/panel.html."""
    metricas = obtener_metricas_consumo(obtener_historial_consumos())

    consumos = metricas["consumo_por_planta"]
    consumo_maximo = max(consumos.values(), default=0)

    # Filas ya listas para la tabla, ordenadas de mayor a menor consumo
    plantas = [
        {
            "nombre": planta,
            "consumo_kwh": consumo,
            "emisiones_kg": metricas["emisiones_por_planta"][planta],
            "porcentaje": round(consumo / consumo_maximo * 100) if consumo_maximo else 0,
        }
        for planta, consumo in sorted(consumos.items(), key=lambda par: par[1], reverse=True)
    ]

    contexto = {
        "titulo": "Panel de Sustentabilidad",
        "total_emisiones": round(metricas["total_emisiones"], 2),
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "plantas": plantas,
    }
    return render(request, "sustentabilidad/panel.html", contexto)
