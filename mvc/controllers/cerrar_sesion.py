import logging

import web

from mvc.models.sesiones import ModelSesiones

logger = logging.getLogger(__name__)


class CerrarSesion:

    def GET(self) -> None:
        try:
            token = web.cookies().get("token")
            if token:
                ModelSesiones().eliminar(token)
        except Exception as error:
            logger.error("ERROR 310: %s", error)
        web.setcookie("token", "", expires=-1)
        raise web.seeother("/login")
