import web
from mvc.models.contactos import ModelContactos

render = web.template.render('mvc/views', base='template')


class Contactos:

    def GET(self):
        modelo = ModelContactos()
        datos = modelo.obtenerContactos()
        return render.contactos(datos)
