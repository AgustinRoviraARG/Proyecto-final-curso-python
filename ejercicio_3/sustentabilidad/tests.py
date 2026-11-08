import unittest
from unittest.mock import patch

from django.test import SimpleTestCase

from .emisiones import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """Auditoría del algoritmo de huella de carbono (Punto A)."""

    def test_calculo_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_calculo_con_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(250, 0.5), 125.0)

    def test_consumo_decimal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5), 5.0)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_mensaje_de_error(self):
        with self.assertRaises(ValueError) as contexto:
            calcular_emisiones_carbono(-50)
        self.assertIn("negativo", str(contexto.exception))


class TestObtenerMetricasConsumo(unittest.TestCase):
    """Procesamiento del historial de consumos (Punto B)."""

    def test_total_y_planta_mayor_consumo(self):
        registros = [
            {"planta": "Norte", "consumo_kwh": 1000},
            {"planta": "Sur", "consumo_kwh": 500},
            {"planta": "Norte", "consumo_kwh": 500},
            {"planta": "Este", "consumo_kwh": 1200},
        ]
        metricas = obtener_metricas_consumo(registros)
        self.assertEqual(metricas["consumo_por_planta"]["Norte"], 1500)
        self.assertEqual(metricas["planta_mayor_consumo"], "Norte")
        self.assertAlmostEqual(metricas["total_emisiones"], (1500 + 500 + 1200) * 0.4)

    def test_historial_vacio(self):
        metricas = obtener_metricas_consumo([])
        self.assertEqual(metricas["total_emisiones"], 0)
        self.assertIsNone(metricas["planta_mayor_consumo"])

    def test_consumo_negativo_propaga_value_error(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "Norte", "consumo_kwh": -10}])


class TestVistaPanelSustentabilidad(SimpleTestCase):
    """La vista responde y entrega el contexto esperado a la plantilla."""

    def test_panel_renderiza_con_contexto(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")
        self.assertEqual(respuesta.context["planta_mayor_consumo"], "Planta Este")
        self.assertAlmostEqual(respuesta.context["total_emisiones"], 1700.0)
        self.assertContains(respuesta, "Panel de Sustentabilidad")

    def test_panel_con_datos_simulados(self):
        datos = [{"planta": "A", "consumo_kwh": 10}, {"planta": "B", "consumo_kwh": 30}]
        with patch("sustentabilidad.views.obtener_historial_consumos", return_value=datos):
            respuesta = self.client.get("/")
        self.assertEqual(respuesta.context["planta_mayor_consumo"], "B")
        self.assertAlmostEqual(respuesta.context["total_emisiones"], 16.0)

    def test_panel_sin_registros(self):
        with patch("sustentabilidad.views.obtener_historial_consumos", return_value=[]):
            respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "No hay registros")
