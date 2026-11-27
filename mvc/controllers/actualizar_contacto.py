import logging

import web

from mvc.controllers.comun import cargar_contacto, render, requerir_login
from mvc.controllers.imagenes import borrar_foto, guardar_foto
from mvc.models.contactos import ModelContactos
from mvc.models.seguridad import validar_firma

logger = logging.getLogger(__name__)


class ActualizarContacto:

    def GET(self) -> str:
        requerir_login()
        try:
            formulario = web.input(id_contacto="")
            contacto = cargar_contacto(formulario.id_contacto)
        except Exception as error:
            logger.error("ERROR 340: %s", error)
            contacto = None
        return render.actualizar_contacto(contacto, "")  # type: ignore

    def POST(self) -> str:
        requerir_login()
        try:
            formulario = web.input(id_contacto="", nombre="", email="", telefono="", foto={})
            id_contacto = validar_firma(formulario.id_contacto)
            modelo = ModelContactos()
            actual = modelo.buscar_contacto(id_contacto) if id_contacto is not None else None
            if id_contacto is None or actual is None:
                return render.mensaje("Contacto no encontrado")  # type: ignore

            nombre = formulario.nombre.strip()
            email = formulario.email.strip()
            telefono = formulario.telefono.strip()
            # Contacto con los valores escritos, por si hay que volver a mostrar el formulario
            editado = {**actual, "id_contacto": formulario.id_contacto,
                       "nombre": nombre, "email": email, "telefono": telefono}

            if not (nombre and email and telefono):
                return render.actualizar_contacto(editado, "Todos los campos son obligatorios")  # type: ignore

            try:
                foto_nueva = guardar_foto(formulario["foto"])
            except ValueError as error:
                return render.actualizar_contacto(editado, str(error))  # type: ignore

            if modelo.actualizar_contacto(id_contacto, nombre, email, telefono, foto_nueva):
                if foto_nueva:
                    borrar_foto(actual.get("foto"))  # se elimina la foto anterior
                return render.mensaje("Contacto actualizado correctamente")  # type: ignore

            borrar_foto(foto_nueva)
            return render.actualizar_contacto(editado, "No se pudo actualizar el contacto")  # type: ignore
        except Exception as error:
            logger.error("ERROR 341: %s", error)
            return render.mensaje("Ocurrió un error inesperado")  # type: ignore
