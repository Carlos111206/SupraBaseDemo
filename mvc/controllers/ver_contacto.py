import web 
from mvc.controllers.contactos import ModelContactos

render = web.template.render("mvc/views", base="template")

class   VerContacto:

    def GET(self):
        formulario = web.input()

        id_contacto = formulario.id_contacto

        contactos = ModelContactos()

        contacto = contactos.buscarContacto(id_contacto)

        return render.ver_contacto(contacto) # type: ignore