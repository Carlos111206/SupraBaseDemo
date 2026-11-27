import logging
import os
import time
import uuid
from typing import Any

logger = logging.getLogger(__name__)

CARPETA_FOTOS = "static/fotos"
FOTO_POR_DEFECTO = "default.png"
EXTENSIONES_VALIDAS = (".jpg", ".jpeg", ".png", ".webp")
TAMANO_MAXIMO = 5 * 1024 * 1024  # 5 MB


def guardar_foto(archivo: Any) -> str | None:
    """Guarda la foto en static/fotos/ y devuelve su nombre.
    None si no se eligió archivo. ValueError (con mensaje para el usuario) si no es válida."""
    nombre_original = getattr(archivo, "filename", "") or ""
    if not nombre_original:
        return None

    extension = os.path.splitext(nombre_original)[1].lower()
    if extension not in EXTENSIONES_VALIDAS:
        raise ValueError("Formato de imagen no permitido (use .jpg, .jpeg, .png o .webp)")

    archivo.file.seek(0)
    contenido: bytes = archivo.file.read()
    if not contenido:
        return None
    if len(contenido) > TAMANO_MAXIMO:
        raise ValueError("La imagen supera el tamaño máximo de 5 MB")

    # Prefijo de timestamp + id aleatorio para evitar colisiones de nombres
    nombre = f"{int(time.time())}_{uuid.uuid4().hex[:8]}{extension}"
    try:
        os.makedirs(CARPETA_FOTOS, exist_ok=True)
        with open(os.path.join(CARPETA_FOTOS, nombre), "wb") as destino:
            destino.write(contenido)
    except OSError as error:
        logger.error("ERROR 500: %s", error)
        raise ValueError("No se pudo guardar la imagen en el servidor") from error
    return nombre


def borrar_foto(nombre: str | None) -> None:
    """Elimina el archivo físico si existe (nunca la imagen por defecto)."""
    try:
        if not nombre or nombre == FOTO_POR_DEFECTO:
            return
        ruta = os.path.join(CARPETA_FOTOS, os.path.basename(nombre))
        if os.path.exists(ruta):
            os.remove(ruta)
    except OSError as error:
        logger.error("ERROR 501: %s", error)
