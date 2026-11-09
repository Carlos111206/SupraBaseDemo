import web
from mvc.controllers.index import Index
from mvc.controllers.contactos import Contactos
from mvc.controllers.insertar_contacto import InsertarContactos


urls = (
    '/', 'Index',
    '/contactos', 'Contactos',
    '/insertar_contacto', 'InsertarContactos',
    '/insertar-contactos', 'InsertarContactos',
)


app = web.application(urls, globals())

if __name__=="__main__":
    app.run()