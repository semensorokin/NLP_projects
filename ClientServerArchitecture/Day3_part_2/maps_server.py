# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import json
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.add_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps([{
            "name": u"Какое-то название",
            "comment": u"Какой-то коммент",
            "lon": 56.322824,
            "lat": 44.010599
        }]))


def make_app():
    return tornado.web.Application([
        (r"/points", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8733)
    tornado.ioloop.IOLoop.current().start()


