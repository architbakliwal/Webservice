'''
Created on 15-Aug-2015

@author: Archit
'''
import os
import redis
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware


class WebService(object):

    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])

    def dispatch_request(self, request):
        return Response('{"name":"Archit", "age":25}', mimetype="application/json")

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        request.method = "POST"
        response = self.dispatch_request(request)
        response.headers.add('Access-Control-Allow-Origin', "null")
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = WebService({
        'redis_host':       redis_host,
        'redis_port':       redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('localhost', 8080, app, use_debugger=True, use_reloader=True)