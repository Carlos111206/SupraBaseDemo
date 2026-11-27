import hashlib
import hmac
import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# RTT05: clave fija en el código (no es lo ideal). Si existe SECRET_KEY en .env se usa esa.
CLAVE_SECRETA: bytes = os.environ.get("SECRET_KEY", "mexico").encode("utf-8")


def generar_firma(id_contacto: int) -> str:
    """Devuelve 'id_contacto:HASH' (HMAC-SHA256). Cadena vacía si falla."""
    try:
        mensaje = str(id_contacto).encode("utf-8")
        hash_hex = hmac.new(CLAVE_SECRETA, mensaje, hashlib.sha256).hexdigest()
        return f"{id_contacto}:{hash_hex}"
    except Exception as error:
        logger.error("ERROR 200: %s", error)
        return ""


def validar_firma(valor: str) -> int | None:
    """Devuelve el id_contacto si la firma es válida; si no, None."""
    try:
        id_texto, separador, _ = valor.partition(":")
        if separador and id_texto.isdigit():
            if hmac.compare_digest(generar_firma(int(id_texto)), valor):
                return int(id_texto)
        return None
    except Exception as error:
        logger.error("ERROR 201: %s", error)
        return None
