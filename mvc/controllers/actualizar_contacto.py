import web
from mvc.controllers.contactos import ModelContactos

render = web.template.render("mvc/views", base="template")

class   ActualizarContacto:

    def GET(self):
        formulario = web.input()


        id_contacto = formulario.id_contacto

        contactos = ModelContactos()
        contacto = contactos.buscarContacto(id_contacto)
        
        return render.actualizar_contacto(contacto) # type: ignore