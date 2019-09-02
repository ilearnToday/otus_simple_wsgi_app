import json
import os

from http.client import responses

from jinja2 import Environment, FileSystemLoader


class Application:
    redirect_if_no_trailing_slash = True

    def __init__(self, static_dir=None, template_dir=None):
        self.handlers_map = {}

        if static_dir:
            self.static_dir = static_dir
        else:
            self.static_dir = "/static/"

        if template_dir:
            self.template_dir = template_dir
        else:
            self.template_dir = "/home/goodei/PycharmProjects/uWSGI/static/templates"

        self.jinja_env = Environment(loader=FileSystemLoader(self.template_dir))

    def add_handler(self, path, handler_callable):
        self.handlers_map[path] = handler_callable

    def register_route(self, path):
        def decorator(f):
            self.add_handler(path, f)
            return f

        return decorator

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        if self.static_dir in path:
            print("{}:static dir {}: path".format(self.static_dir, path))
            handler = self.static_handler
        elif not path.endswith("/") and self.redirect_if_no_trailing_slash:
            handler = self.redirect_trailing_slash_handler
        else:
            handler = self.handlers_map.get(path, self.not_found_handler)

        response = handler(env)
        response_headers = {'Content-Type': 'text/html'}
        response_body = ''

        if 'data' in response:
            response_body = response['data']
        elif 'text' in response:
            response_body = response['text'].encode('utf-8')
        elif 'json' in response:
            response_body = json.dumps(response['json']).encode('utf-8')
            response_headers = {'Content-Type': 'text/json'}

        status_code = response.get('status_code', 200)
        extra_header = response.get('extra_headers', {})

        response_headers.update(extra_header)

        start_response('{} {}'.format(
            status_code,
            responses[status_code]
        ),
            list(response_headers.items())
        )
        return [response_body]

    def static_handler(self, env):
        path = env['PATH_INFO']
        if path.endswith('/'):
            path = path[:-1]
        if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + path):
            try:
                file_connection = open(os.path.dirname(os.path.abspath(__file__)) + path, 'rb')
                content = file_connection.read()
                file_connection.close()
                return {
                    "data": content,
                    "extra_headers": {'Content-Type': self.detect_static_content_type(env)}
                }
            except (IOError, TypeError):
                return self.not_found_handler(env)
        else:
            return self.not_found_handler(env)

    @staticmethod
    def render_template(env, template_name, *args, **kwargs):
        template = env.get_template(template_name)
        return template.render(*args, **kwargs)

    @staticmethod
    def not_found_handler(env):
        return {
            "text": 'Not Found',
            "status_code": 404
        }

    @staticmethod
    def redirect_trailing_slash_handler(env):
        path = env['PATH_INFO'] + '/'
        return {
            'status_code': 308,
            'extra_headers': {'Location': path}
        }

    @staticmethod
    def detect_static_content_type(env):
        """
        Return static files content type
        :param env: dict
        :return: string
        """
        path = env['PATH_INFO']
        if path.endswith(".css"):
            return "text/css"
        elif path.endswith(".html"):
            return "text/html"
        elif path.endswith(".js"):
            return "text/javascript"
        elif path.endswith(".jpg") or path.endswith(".jpeg"):
            return "image/jpeg"
        else:
            return TypeError



