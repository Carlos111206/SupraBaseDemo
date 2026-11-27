import logging

from mvc.controllers.comun import render, requerir_login
from mvc.models.contactos import ModelContactos
from mvc.models.seguridad import generar_firma

logger = logging.getLogger(__name__)


class ListaContactos:

    def GET(self) -> str:
        requerir_login()
        contactos = ModelContactos().obtener_contactos()
        for contacto in contactos:
            # RNT02: el id nunca sale sin firma
            contacto["id_contacto"] = generar_firma(int(contacto["id_contacto"]))
        return render.lista_contactos(contactos)  # type: ignore
