import os
import hashlib
import hmac
import logging
from typing import Any, cast

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class ModelContactos:

    def __init__(self) -> None:
        try:
            self.supabase: Client = create_client(
                os.environ.get("SUPABASE_URL", ""),
                os.environ.get("SUPABASE_KEY", "")
            )
            # Mejor guardar la clave en el archivo .env (SECRET_KEY=...)
            self.SECRET_KEY = os.environ.get("SECRET_KEY", "mexico").encode("utf-8")
        except Exception as error:
            logger.error(f"ERROR 100: {str(error)}")
            print(f"ERROR 100: {str(error)}")

    def generar_hash(self, id: int) -> str:
        """Genera un hash único a partir del ID (formato id:firma)."""
        try:
            mensaje = str(id).encode("utf-8")
            firma = hmac.new(self.SECRET_KEY, mensaje, hashlib.sha256).hexdigest()
            return f"{id}:{firma}"
        except Exception as error:
            logger.error(f"ERROR 106: {str(error)}")
            return ""

    def validar_hash(self, hash_a_validar: str) -> int | None:
        """Devuelve el id si el hash es válido; si no, devuelve None."""
        try:
            id_str, sep, _ = hash_a_validar.partition(":")
            if sep and id_str.isdigit():
                token_esperado = self.generar_hash(int(id_str))
                if hmac.compare_digest(token_esperado, hash_a_validar):
                    return int(id_str)
            return None
        except Exception as error:
            print(f"ERROR 107: {str(error)}")
            return None

    def obtenerContactos(self) -> list[dict[str, Any]]:
        try:
            # SELECT * FROM contactos;
            response = self.supabase.table("contactos").select("*").execute()
            registros = response.data or []
            for registro in registros:
                id_num = int(registro["id_contacto"])  # type: ignore
                registro["id_contacto"] = self.generar_hash(id_num)  # type: ignore
            return cast(list[dict[str, Any]], registros)
        except Exception as error:
            logger.error("ERROR 101: %s", error)
            print(f"ERROR 101: {str(error)}")
            return []

    def buscarContacto(self, id_contacto: str):
        try:
            id = self.validar_hash(id_contacto)
            if id is None:
                return None
            # SELECT * FROM contactos WHERE id_contacto = ?;
            response = self.supabase.table("contactos").select("*").eq("id_contacto", id).execute()
            if response.data:
                contacto = response.data[0]
                # Devolvemos el id ya con hash para usarlo en los formularios
                contacto["id_contacto"] = self.generar_hash(id)  # type: ignore
                return contacto
            return None
        except Exception as error:
            logger.error("ERROR 102: %s", error)
            print(f"ERROR 102: {str(error)}")
            return None

    def insertarContacto(self, nombre: str, email: str, telefono: str, imagen: str = "default.png"):
        try:
            # INSERT INTO contactos(nombre,email,telefono,imagen) VALUES(?,?,?,?);
            data = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "imagen": imagen
            }
            response = self.supabase.table("contactos").insert(data).execute()
            return response.data
        except Exception as error:
            print(f"ERROR 103: {str(error)}")

    def borrarContacto(self, id_contacto: str):
        try:
            id = self.validar_hash(id_contacto)
            if id is None:
                return None
            # DELETE FROM contactos WHERE id_contacto = ?;
            response = self.supabase.table("contactos").delete().eq("id_contacto", id).execute()
            return response.data
        except Exception as error:
            print(f"ERROR 104: {str(error)}")

    def actualizarContacto(self, id_contacto: str, nombre: str, email: str, telefono: str, imagen: str | None = None):
        try:
            id = self.validar_hash(id_contacto)
            if id is None:
                return None
            # UPDATE contactos SET nombre=?, email=?, telefono=?, imagen=? WHERE id_contacto=?;
            data = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono
            }
            # Solo cambiamos la foto si se subió una nueva
            if imagen:
                data["imagen"] = imagen
            response = self.supabase.table("contactos").update(data).eq("id_contacto", id).execute()
            return response.data
        except Exception as error:
            print(f"ERROR 105: {str(error)}")
