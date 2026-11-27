import logging

import web

from mvc.controllers.comun import render, requerir_login
from mvc.controllers.imagenes import FOTO_POR_DEFECTO, borrar_foto, guardar_foto
from mvc.models.contactos import ModelContactos

logger = logging.getLogger(__name__)


class InsertarContacto:

    def GET(self) -> str:
        requerir_login()
        return render.insertar_contacto("")  # type: ignore

    def POST(self) -> str:
        requerir_login()
        try:
            formulario = web.input(nombre="", email="", telefono="", foto={})
            nombre = formulario.nombre.strip()
            email = formulario.email.strip()
            telefono = formulario.telefono.strip()
            if not (nombre and email and telefono):
                return render.insertar_contacto("Todos los campos son obligatorios")  # type: ignore

            try:
                foto = guardar_foto(formulario["foto"])
            except ValueError as error:
                return render.insertar_contacto(str(error))  # type: ignore

            if ModelContactos().insertar_contacto(nombre, email, telefono, foto or FOTO_POR_DEFECTO):
                return render.mensaje("Contacto insertado correctamente")  # type: ignore

            borrar_foto(foto)
            return render.insertar_contacto("No se pudo insertar el contacto")  # type: ignore
        except Exception as error:
            logger.error("ERROR 330: %s", error)
            return render.insertar_contacto("Ocurrió un error inesperado")  # type: ignore
