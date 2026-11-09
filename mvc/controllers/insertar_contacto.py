import web 
from mvc.controllers.contactos import ModelContactos

render = web.template.render("mvc/views")

class InsertarContactos:

    def GET(self):
        return render.insertar_contacto()

    def POST(self):
        formulario = web.input()

        nombre = formulario.nombre
        email = formulario.email
        telefono = formulario.telefono

        print(f"Nombre:{nombre}")
        print(f"Email:{email}")
        print(f"Telefono:{telefono}")

        contactos = ModelContactos()
        contactos.insertarContacto(nombre, email, telefono)

        raise web.seeother('/contactos')



