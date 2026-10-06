from nodos.nucleo.validacion import validar_contenido

CAMPOS = [
    {"nombre": "razon_social", "tipo": "texto", "obligatorio": True},
    {"nombre": "empleados", "tipo": "numero", "obligatorio": False},
    {"nombre": "alta", "tipo": "fecha", "obligatorio": True},
    {"nombre": "activo", "tipo": "booleano", "obligatorio": False},
    {"nombre": "etiquetas", "tipo": "lista", "obligatorio": False},
]


def test_valido():
    assert validar_contenido(CAMPOS, {"razon_social": "ACME", "alta": "2026-10-06", "empleados": 12,
                                      "activo": True, "etiquetas": ["a"]}) == []


def test_falta_obligatorio():
    errores = validar_contenido(CAMPOS, {"razon_social": "ACME"})
    assert len(errores) == 1 and "alta" in errores[0]


def test_campo_no_declarado():
    errores = validar_contenido(CAMPOS, {"razon_social": "ACME", "alta": "2026-10-06", "color": "rojo"})
    assert len(errores) == 1 and "color" in errores[0]


def test_tipos_incorrectos():
    errores = validar_contenido(CAMPOS, {"razon_social": 5, "alta": "06/10/2026", "empleados": "doce",
                                         "activo": "si", "etiquetas": "a"})
    assert len(errores) == 5


def test_booleano_no_es_numero():
    errores = validar_contenido(CAMPOS, {"razon_social": "ACME", "alta": "2026-10-06", "empleados": True})
    assert len(errores) == 1 and "empleados" in errores[0]


def test_contenido_no_dict():
    assert validar_contenido(CAMPOS, ["x"]) != []
