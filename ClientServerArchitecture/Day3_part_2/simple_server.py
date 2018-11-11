import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        res = {
            "http_method" : self.request.method,
            "params": self.request.arguments,
            "path": self.request.path
        }
        for a in self.request.arguments:
            res["params"][a] = self.request.arguments[a]
        self.write(res)

    def post(self):
        res = {
            "http_method": self.request.method,
            "params": self.request.arguments,
            "path": self.request.path,
            "body": self.request.body
        }
        for a in self.request.arguments:
            res["params"][a] = self.request.arguments[a]
        self.write(res)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


