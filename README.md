# EcoTech Solutions – Ejercicios

```
ecotech/
├── ejercicio_1/   Sensores: limpieza y resumen estadístico
│   └── sensores.py
├── ejercicio_2/   Catálogo: clases, excepciones y persistencia JSON
│   └── catalogo.py
└── ejercicio_3/   Proyecto Django completo: tests + panel web
    ├── manage.py
    ├── requirements.txt
    ├── ecotech_project/   (configuración)
    └── sustentabilidad/   (app: lógica, vista, plantilla y tests)
```

## Ejercicios 1 y 2 (solo Python)

```
cd ejercicio_1
python sensores.py

cd ../ejercicio_2
python catalogo.py        # genera catalogo_ecotech.json
```

## Ejercicio 3 (Django)

Desde la carpeta `ejercicio_3`:

**Windows (PowerShell o CMD)**
```
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py test
python manage.py runserver
```

**Linux / macOS**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py test
python manage.py runserver
```

Luego abrir http://127.0.0.1:8000/ para ver el panel de sustentabilidad.

No hace falta ejecutar migraciones: el proyecto no usa base de datos.

## Dónde está cada parte del ejercicio 3

| Pedido del enunciado | Archivo |
|---|---|
| `calcular_emisiones_carbono` | `sustentabilidad/emisiones.py` |
| `obtener_metricas_consumo` | `sustentabilidad/emisiones.py` |
| `TestCalculoEmisiones` | `sustentabilidad/tests.py` |
| `vista_panel_sustentabilidad` | `sustentabilidad/views.py` |
| Plantilla `sustentabilidad/panel.html` | `sustentabilidad/templates/sustentabilidad/panel.html` |
