import web
from mvc.models.contactos import ModelContactos
from mvc.controllers.imagenes import guardar_imagen

render = web.template.render("mvc/views", base="template")


class ActualizarContacto:

    def GET(self):
        formulario = web.input()
        id_contacto = formulario.id_contacto

        contactos = ModelContactos()
        contacto = contactos.buscarContacto(id_contacto)

        if not contacto:
            raise web.seeother('/contactos')

        return render.actualizar_contacto(contacto)  # type: ignore

    def POST(self):
        formulario = web.input(image={})

        id_contacto = formulario.id_contacto
        nombre = formulario.nombre
        email = formulario.email
        telefono = formulario.telefono
        # None si no se eligió una foto nueva (se conserva la anterior)
        imagen = guardar_imagen(formulario["image"])

        contactos = ModelContactos()
        contactos.actualizarContacto(id_contacto, nombre, email, telefono, imagen)

        raise web.seeother('/contactos')
