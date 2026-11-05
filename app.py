import web
from mvc.controllers.index import Index


urls = (
    '/','Index',
)


app = web.application(urls, globals())

if __name__=="__main__":
    app.run()