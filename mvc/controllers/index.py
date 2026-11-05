import web 

render = web.template.render('mvc/views',base='temaplate')

class Index:
     
     def GET(self):
          return render.index()
