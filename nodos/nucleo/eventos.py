"""Eventos: un módulo AVISA que pasó algo y otros módulos REACCIONAN, sin conocerse entre sí.

Ejemplo: el módulo `lotes` avisa "lote_borrado"; el módulo `relaciones`, si está activo, reacciona
quitando las flechas de ese lote. Si quitás el módulo `relaciones`, `lotes` sigue funcionando igual.
"""
_suscriptores = {}   # nombre del evento → lista de funciones a llamar


def suscribir(evento, funcion):
    """Anota `funcion` para que se ejecute cada vez que ocurra `evento`."""
    lista = _suscriptores.setdefault(evento, [])
    if funcion not in lista:
        lista.append(funcion)


def emitir(evento, conn, **datos):
    """Avisa que ocurrió `evento`: llama a cada función suscripta con la conexión y los datos."""
    for funcion in _suscriptores.get(evento, []):
        funcion(conn, **datos)
