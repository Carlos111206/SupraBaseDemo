import logging
import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

logger = logging.getLogger(__name__)


class ModelSesiones:
    """Acceso a la tabla sesiones_abiertas (token)."""

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", ""),
            )
        except Exception as error:
            logger.error("ERROR 110: %s", error)
            raise

    def registrar(self, token: str) -> bool:
        try:
            respuesta = self.supabase.table("sesiones_abiertas").insert({"token": token}).execute()
            return bool(respuesta.data)
        except Exception as error:
            logger.error("ERROR 111: %s", error)
            return False

    def eliminar(self, token: str) -> bool:
        try:
            self.supabase.table("sesiones_abiertas").delete().eq("token", token).execute()
            return True
        except Exception as error:
            logger.error("ERROR 112: %s", error)
            return False

    def es_vigente(self, token: str) -> bool:
        try:
            respuesta = (
                self.supabase.table("sesiones_abiertas")
                .select("token")
                .eq("token", token)
                .limit(1)
                .execute()
            )
            return bool(respuesta.data)
        except Exception as error:
            logger.error("ERROR 113: %s", error)
            return False
