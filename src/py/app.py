#####
# Main 
####

import falcon
import json

from .email import Mailer
from .middleware import DatabaseMiddleware
from .middleware import SessionMiddleware
from .pages import homepage
from .pages import langpage
from .pages import linksentpage

class HomeResource(object):
    def __init__(self, mailer):
        self.mailer = mailer

    def on_get(self, req, resp):
        if "user" in req.context and req.context["user"]:
            db = req.context["db"]
            user = req.context["user"]
            resp.body = langpage(db.user_langs(user), user, db.all_langs())
        else:
            resp.body = homepage()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        if "user" in req.context and req.context["user"]:
            data = json.loads(req.stream.read().decode("utf-8"))
            req.context["db"].update_langs(req.context["user"], data)

            # TODO response body? 
            resp.status = falcon.HTTP_200
        else:
            # Form submission to sent login link
            reqbody = req.stream.read().decode("utf-8")
            data = dict(tuple(f.split("=")) for f in reqbody.split("&"))
            if "username" in data and data["username"]:
                email = req.context["db"].get_user_email(data["username"])
                if email:
                    token = req.context["db"].add_token(data["username"])
                    self.mailer.send_link(token, email) # TODO catch errors
                    resp.body = linksentpage(data["username"])
                else:
                    resp.body = homepage() # TODO Tell user what happened?
            else:
                resp.body = homepage() # TODO I think so, right?
            resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class ListResource(object):
    def on_get(self, req, resp, user):
        resp.body = langpage(req.context["db"].user_langs(user), user)
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


config_file = "/home/protected/.nyelv-db.conf"
middleware = [DatabaseMiddleware(config_file), SessionMiddleware()]
app = falcon.API(middleware=middleware)

app.add_route("/{user}", ListResource())
app.add_route("/", HomeResource(Mailer())) # TODO Mailer will take path to file
