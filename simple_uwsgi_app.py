from http.client import responses
import json
import os


class Application:
    redirect_if_no_trailing_slash = True

    def __init__(self, static_dir=None):
        self.handlers_map = {}

        if static_dir:
            self.static_dir = static_dir
        else:
            self.static_dir = "/static/"

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
        if 'text' in response:
            response_body = response['text']
        elif 'json' in response:
            response_body = json.dumps(response['json'])
            print(response_body)
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
        return [response_body.encode("utf-8")]

    def static_handler(self, env):
        path = env['PATH_INFO']
        if path.endswith('/'):
            path = path[:-1]
        if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + path):
            try:
                file_connection = open(os.path.dirname(os.path.abspath(__file__)) + path, 'r')
                content = file_connection.read()
                file_connection.close()
                return {
                    "text": content,
                    "extra_headers": {'Content-Type': self.detect_static_content_type(env)}
                }
            except (IOError, TypeError):
                print()
                return self.not_found_handler(env)
        else:
            return self.not_found_handler(env)

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
        Doesn't work with images
        :param env: dict
        :return: sting
        """
        path = env['PATH_INFO']
        if path.endswith(".css"):
            return "text/css"
        elif path.endswith(".html"):
            return "text/html"
        elif path.endswith(".js"):
            return "text/javascript"
        else:
            return TypeError



