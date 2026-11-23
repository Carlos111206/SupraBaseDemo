import os
import uuid

CARPETA_IMAGENES = "static/images"
EXTENSIONES_VALIDAS = (".png", ".jpg", ".jpeg")


def guardar_imagen(archivo) -> str | None:
    """Guarda la imagen subida en static/images y devuelve el nombre del archivo.
    Si no se subió ninguna imagen (o no es válida) devuelve None."""
    if not archivo or not getattr(archivo, "filename", ""):
        return None

    extension = os.path.splitext(archivo.filename)[1].lower()
    if extension not in EXTENSIONES_VALIDAS:
        return None

    # Nombre único para que dos fotos no se sobreescriban
    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    archivo.file.seek(0)
    with open(os.path.join(CARPETA_IMAGENES, nombre_archivo), "wb") as f:
        f.write(archivo.file.read())
    return nombre_archivo
