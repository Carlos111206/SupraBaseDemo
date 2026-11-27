import logging

import web

from mvc.controllers.comun import cargar_contacto, render, requerir_login
from mvc.controllers.imagenes import borrar_foto
from mvc.models.contactos import ModelContactos
from mvc.models.seguridad import validar_firma

logger = logging.getLogger(__name__)


class BorrarContacto:

    def GET(self) -> str:
        requerir_login()
        try:
            formulario = web.input(id_contacto="")
            contacto = cargar_contacto(formulario.id_contacto)
        except Exception as error:
            logger.error("ERROR 350: %s", error)
            contacto = None
        return render.borrar_contacto(contacto)  # type: ignore

    def POST(self) -> str:
        requerir_login()
        try:
            formulario = web.input(id_contacto="")
            id_contacto = validar_firma(formulario.id_contacto)
            modelo = ModelContactos()
            actual = modelo.buscar_contacto(id_contacto) if id_contacto is not None else None
            if id_contacto is None or actual is None:
                return render.mensaje("Contacto no encontrado")  # type: ignore

            if modelo.borrar_contacto(id_contacto):
                borrar_foto(actual.get("foto"))
                return render.mensaje("Contacto eliminado correctamente")  # type: ignore
            return render.mensaje("No se pudo eliminar el contacto")  # type: ignore
        except Exception as error:
            logger.error("ERROR 351: %s", error)
            return render.mensaje("Ocurrió un error inesperado")  # type: ignore
