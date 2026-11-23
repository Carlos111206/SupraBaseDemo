import web
from mvc.models.contactos import ModelContactos
from mvc.controllers.imagenes import guardar_imagen

render = web.template.render("mvc/views", base="template")


class InsertarContactos:

    def GET(self):
        return render.insertar_contacto()

    def POST(self):
        formulario = web.input(image={})

        nombre = formulario.nombre
        email = formulario.email
        telefono = formulario.telefono
        imagen = guardar_imagen(formulario["image"]) or "default.png"

        contactos = ModelContactos()
        contactos.insertarContacto(nombre, email, telefono, imagen)

        raise web.seeother('/contactos')
