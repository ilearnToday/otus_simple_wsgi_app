from core import Application

application = Application()

kitty_template = application.render_template(application.jinja_env, 'template_example.html', name="Kitty")
# application.redirect_if_no_trailing_slash = False


@application.register_route('/cat/')
def cat_handler(env):
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


@application.register_route('/fromtemplate/')
def from_template_handler(env):
    return {
        'text': kitty_template,
    }


@application.register_route('/')
def index_handler(env):
    return {
        "json": {"page": "Index Page"}
    }
