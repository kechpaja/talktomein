#####
# Main 
####

import falcon
import json

from .middleware import DatabaseMiddleware
from .middleware import SessionMiddleware
from .pages import langpage
from .pages import homepage

class HomeResource(object):
    def on_get(self, req, resp):
        if "user" in req.context:
            db = req.context["db"]
            resp.body = langpage(db.user_langs(req.context["user"]), 
                                 langlist=db.all_langs())
        else:
            resp.body = homepage()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        if "user" in req.context["user"]:
            data = json.loads(req.stream.read().decode("utf-8"))
            languages = [[user, lang, data[lang]] for lang in data.keys()]
            req.context["db"].update_langs(req.context["user"], languages)

            # TODO response body? 
            resp.status = falcon.HTTP_200
        else:
            # TODO error response body
            resp.status = falcon.HTTP_401


class ListResource(object):
    def on_get(self, req, resp, user):
        resp.body = langpage(req.context["db"].user_langs(user), user=user)
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


config_file = "/home/protected/.nyelv-db.conf"
middleware = [DatabaseMiddleware(config_file), SessionMiddleware()]
app = falcon.API(middleware=middleware)

app.add_route("/{user}", ListResource())
app.add_route("/", HomeResource())
