"""
Ejercicio 2 - Modelo de productos, excepciones y persistencia (EcoTech Solutions)

Ejecutar:  python catalogo.py
Genera catalogo_ecotech.json en la misma carpeta que este archivo.
"""

import json
from pathlib import Path


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock inválido (negativo o no entero)."""


class DispositivoEcológico:
    """Clase base de los productos del catálogo."""

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock  # pasa por el setter: se valida también al construir

    # --- Encapsulamiento explícito del stock ---------------------------
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise StockInvalidoError(f"El stock debe ser un entero, se recibió: {valor!r}")
        if valor < 0:
            raise StockInvalidoError(f"El stock no puede ser negativo: {valor}")
        self._stock = valor

    # --- Comportamiento polimórfico ------------------------------------
    def ficha_tecnica(self):
        return (
            f"Dispositivo: {self.nombre} | Precio: ${self.precio:,.2f} | "
            f"Stock: {self.stock} unidades"
        )

    def to_dict(self):
        """Representación serializable (evita exponer el atributo privado _stock)."""
        return {
            "tipo": type(self).__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcológico):
    """Panel solar: agrega potencia y eficiencia por herencia."""

    def __init__(self, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia  # porcentaje, ej. 21.5

    def ficha_tecnica(self):  # polimorfismo: ficha comercial propia
        return (
            f"Panel Solar {self.nombre} | Potencia: {self.potencia_w} W | "
            f"Eficiencia: {self.eficiencia}% | Precio: ${self.precio:,.2f} | "
            f"Stock: {self.stock} unidades"
        )

    def to_dict(self):
        datos = super().to_dict()
        datos.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return datos


class GestorInventario:
    """Gestiona la persistencia del catálogo en disco."""

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo="catalogo_ecotech.json"):
        datos = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return ruta_archivo


def main():
    catalogo = []

    # Altas: la última tiene stock inválido y debe ser rechazada
    altas = [
        lambda: DispositivoEcológico("Cargador Solar Portátil", 45.90, 120),
        lambda: PanelSolar("EcoMax 450", 380.00, 35, 450, 21.5),
        lambda: PanelSolar("EcoMini 100", 95.50, -5, 100, 18.0),
    ]
    for crear in altas:
        try:
            catalogo.append(crear())
        except StockInvalidoError as error:
            print(f"[StockInvalidoError capturado al crear] {error}")

    # Asignación errónea sobre un producto ya existente
    try:
        catalogo[0].stock = -10
    except StockInvalidoError as error:
        print(f"[StockInvalidoError capturado al asignar] {error}")

    print("\nFichas técnicas (polimorfismo):")
    for dispositivo in catalogo:
        print(" -", dispositivo.ficha_tecnica())

    ruta = Path(__file__).resolve().parent / "catalogo_ecotech.json"
    GestorInventario().guardar_catalogo_json(catalogo, ruta)
    print(f"\nCatálogo exportado a '{ruta.name}' ({len(catalogo)} productos válidos).")


if __name__ == "__main__":
    main()
