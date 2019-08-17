from simple_uwsgi_app import Application


"""def index_handler(env):
    return {
        "json": {"page": "Index Page"}
    }"""






application = Application(static_dir='/static/')
#application.redirect_if_no_trailing_slash = True
#application.add_handler('/', index_handler)
#application.add_handler('/catalog/', catalog_handler)

@application.register_route('/cat/')
def catalog_handler(env):
    return {
        "text": '<!DOCTYPE html>'
'<html lang="en">'
'<head>'
    '<meta charset="UTF-8">'
    '<title>Title</title>'
    '<h1>Hello World!</h1>'
    '<link rel="stylesheet" href="/static/css/style.css">'
'</head>'
'<body>'
'<img src="/static/img/picture.jpeg">'
'</body>'
'</html>'
    }


@application.register_route('/')
def index_handler(env):
    return {
        "json": {"page": "Index Page"}
    }

