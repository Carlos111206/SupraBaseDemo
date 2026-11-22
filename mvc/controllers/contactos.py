import web 
from mvc.models.contactos import contactos

render = web.template.render('mvc/views/contactos/', base='template')

class Contactos:

    def GET(self):
        contactos = ModelContactos()
        datos = contactos.obtenerContactos()

        return render.contactos(datos) 