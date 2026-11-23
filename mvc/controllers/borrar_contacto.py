import web
from mvc.models.contactos import ModelContactos

render = web.template.render("mvc/views", base="template")


class BorrarContacto:

    def GET(self):
        formulario = web.input()
        id_contacto = formulario.id_contacto

        contactos = ModelContactos()
        contacto = contactos.buscarContacto(id_contacto)

        if not contacto:
            raise web.seeother('/contactos')

        return render.borrar_contacto(contacto)  # type: ignore

    def POST(self):
        formulario = web.input()
        id_contacto = formulario.id_contacto

        contactos = ModelContactos()
        contactos.borrarContacto(id_contacto)

        raise web.seeother('/contactos')
