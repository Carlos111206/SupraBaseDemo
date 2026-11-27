import logging
import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

logger = logging.getLogger(__name__)


class Authenuser:
    """Autenticación con Supabase Authentication (email y password)."""

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", ""),
            )
        except Exception as error:
            logger.error("ERROR 100: %s", error)
            raise

    def iniciar_sesion(self, email: str, password: str) -> str | None:
        """Devuelve el token JWT de la sesión, o None si las credenciales son inválidas."""
        try:
            respuesta = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if respuesta.session and respuesta.session.access_token:
                return respuesta.session.access_token
            logger.error("ERROR 101: Supabase no devolvió sesión")
            return None
        except Exception as error:
            logger.error("ERROR 102: %s", error)
            return None
