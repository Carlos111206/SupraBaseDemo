import logging
from typing import Any

import web

from mvc.models.contactos import ModelContactos
from mvc.models.seguridad import generar_firma, validar_firma
from mvc.models.sesiones import ModelSesiones

logger = logging.getLogger(__name__)

render = web.template.render("mvc/views", base="template")


def requerir_login() -> None:
    """RNT01: sin cookie de token vigente en sesiones_abiertas, redirige a login."""
    try:
        token = web.cookies().get("token")
        if token and ModelSesiones().es_vigente(token):
            return
    except Exception as error:
        logger.error("ERROR 400: %s", error)
    raise web.seeother("/login")


def cargar_contacto(firma: str) -> dict[str, Any] | None:
    """Valida 'id:HASH', busca el contacto y le deja el id ya firmado."""
    id_contacto = validar_firma(firma)
    if id_contacto is None:
        return None
    contacto = ModelContactos().buscar_contacto(id_contacto)
    if contacto is None:
        return None
    contacto["id_contacto"] = generar_firma(id_contacto)
    return contacto
