import logging

import web

from mvc.controllers.comun import cargar_contacto, render, requerir_login

logger = logging.getLogger(__name__)


class VerContacto:

    def GET(self) -> str:
        requerir_login()
        try:
            formulario = web.input(id_contacto="")
            contacto = cargar_contacto(formulario.id_contacto)
        except Exception as error:
            logger.error("ERROR 320: %s", error)
            contacto = None
        return render.ver_contacto(contacto)  # type: ignore
