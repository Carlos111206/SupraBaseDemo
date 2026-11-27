import logging

import web

from mvc.controllers.comun import render
from mvc.models.auth_users import Authenuser
from mvc.models.sesiones import ModelSesiones

logger = logging.getLogger(__name__)

MENSAJE_ERROR = "Credenciales incorrectas, verifique sus datos"


class Login:

    def GET(self) -> str:
        return render.login("")  # type: ignore

    def POST(self) -> str:
        token: str | None = None
        mensaje = MENSAJE_ERROR
        try:
            formulario = web.input(email="", password="")
            token = Authenuser().iniciar_sesion(formulario.email.strip(), formulario.password)
            if token and not ModelSesiones().registrar(token):
                token = None
                mensaje = "No se pudo registrar la sesión, intente de nuevo"
        except Exception as error:
            logger.error("ERROR 300: %s", error)
            token = None

        if not token:
            return render.login(mensaje)  # type: ignore

        web.setcookie("token", token, httponly=True)
        raise web.seeother("/")
