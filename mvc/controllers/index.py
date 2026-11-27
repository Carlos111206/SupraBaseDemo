import logging

from mvc.controllers.comun import render, requerir_login

logger = logging.getLogger(__name__)


class Index:

    def GET(self) -> str:
        requerir_login()
        return render.index()  # type: ignore
