import logging
import os
from typing import Any, cast

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

logger = logging.getLogger(__name__)


class ModelContactos:
    """Acceso a la tabla contactos (id_contacto, nombre, email, telefono, foto)."""

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", ""),
            )
        except Exception as error:
            logger.error("ERROR 100: %s", error)
            raise

    def obtener_contactos(self) -> list[dict[str, Any]]:
        try:
            respuesta = self.supabase.table("contactos").select("*").order("id_contacto").execute()
            return cast(list[dict[str, Any]], respuesta.data or [])
        except Exception as error:
            logger.error("ERROR 101: %s", error)
            return []

    def buscar_contacto(self, id_contacto: int) -> dict[str, Any] | None:
        try:
            respuesta = (
                self.supabase.table("contactos")
                .select("*")
                .eq("id_contacto", id_contacto)
                .execute()
            )
            if respuesta.data:
                return cast(dict[str, Any], respuesta.data[0])
            return None
        except Exception as error:
            logger.error("ERROR 102: %s", error)
            return None

    def insertar_contacto(self, nombre: str, email: str, telefono: str, foto: str) -> bool:
        try:
            datos = {"nombre": nombre, "email": email, "telefono": telefono, "foto": foto}
            respuesta = self.supabase.table("contactos").insert(datos).execute()
            return bool(respuesta.data)
        except Exception as error:
            logger.error("ERROR 103: %s", error)
            return False

    def actualizar_contacto(
        self, id_contacto: int, nombre: str, email: str, telefono: str, foto: str | None = None
    ) -> bool:
        try:
            datos: dict[str, Any] = {"nombre": nombre, "email": email, "telefono": telefono}
            if foto:  # solo se cambia la foto si se subió una nueva
                datos["foto"] = foto
            respuesta = (
                self.supabase.table("contactos")
                .update(datos)
                .eq("id_contacto", id_contacto)
                .execute()
            )
            return bool(respuesta.data)
        except Exception as error:
            logger.error("ERROR 104: %s", error)
            return False

    def borrar_contacto(self, id_contacto: int) -> bool:
        try:
            respuesta = (
                self.supabase.table("contactos")
                .delete()
                .eq("id_contacto", id_contacto)
                .execute()
            )
            return bool(respuesta.data)
        except Exception as error:
            logger.error("ERROR 105: %s", error)
            return False
