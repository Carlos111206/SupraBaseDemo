import logging

import web

from mvc.controllers.actualizar_contacto import ActualizarContacto
from mvc.controllers.borrar_contacto import BorrarContacto
from mvc.controllers.cerrar_sesion import CerrarSesion
from mvc.controllers.index import Index
from mvc.controllers.insertar_contacto import InsertarContacto
from mvc.controllers.lista_contactos import ListaContactos
from mvc.controllers.login import Login
from mvc.controllers.ver_contacto import VerContacto

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)

urls = (
    "/", "Index",
    "/login", "Login",
    "/cerrar_sesion", "CerrarSesion",
    "/lista_contactos", "ListaContactos",
    "/ver_contacto", "VerContacto",
    "/insertar_contacto", "InsertarContacto",
    "/actualizar_contacto", "ActualizarContacto",
    "/borrar_contacto", "BorrarContacto",
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
