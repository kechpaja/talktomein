#####
# Main 
####

import falcon
import json
import re
from urllib.parse import unquote

from . import send
from .middleware import DatabaseMiddleware
from .middleware import SessionMiddleware
from .pages import deletepage
from .pages import homepage
from .pages import langpage
from .pages import msgpage

class HomeResource(object):
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
            for l in data:
                if data[l] not in ["A", "B", "C"]:
                    del data[l]
            req.context["db"].update_langs(req.context["user"], data)
            resp.body = "{\"ok\" : true}"
        else:
            # Form submission to send login link
            reqbody = req.stream.read().decode("utf-8")
            data = dict(tuple(f.split("=")) for f in reqbody.split("&"))
            if "username" in data and data["username"]:
                username = data["username"]
                address = req.context["db"].get_user_email(username)
                if address and "email" in data and data["email"]:
                    resp.body = homepage("Username is in use.", True)
                elif address:
                    token = req.context["db"].add_token("login", username)
                    send.link(address, 
                              "Login Link",
                              "Click the link to log in",
                              "/",
                              {"token" : token})
                    resp.body = msgpage(
                        "Login Link Sent",
                        "A login link has been sent to %s." % username
                    )
                elif "email" in data and data["email"]:
                    address = unquote(data["email"])
                    banned = ["login", "logout", "contact", "about", "api",
                              "account", "accounts", "blog"]
                    if not re.match("\w+", username) or username in banned:
                        resp.body = homepage("Invalid username. ", True)
                    elif not re.match("[^@]+\@([^@.]+.)+\.[^@.]", address):
                        resp.body = homepage("Invalid email. ", True)
                    else:
                        token = req.context["db"].add_token("login", username)
                        send.link(address,
                                  "Activation Link",
                                  "Click the link to activate your account",
                                  "/",
                                  {"token" : token, "email" : address})
                        resp.body = msgpage(
                            "Activation Link Sent",
                            "An activation link has been sent to %s." % username
                        )
                else:
                    resp.body = homepage("Username not found.")
            else:
                resp.body = homepage()
            resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class ListResource(object):
    def on_get(self, req, resp, user):
        resp.body = langpage(req.context["db"].user_langs(user), user)
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class DeleteAccountResource(object):
    def on_get(self, req, resp):
        if "user" in req.context and req.context["user"]:
            user = req.context["user"]
            token = req.context["db"].add_token("login", req.context["user"])
            send.link(req.context["db"].get_user_email(req.context["user"]),
                      "Delete Account Link",
                      "Click the link to continue deleting your account",
                      "/account/delete/confirm",
                      {"token" : token})
            resp.body = msgpage(
                "Deletion Link Sent",
                "An account deletion link has been sent to %s." % user
            )
            resp.content_type = "text/html; charset=utf-8"
        else:
            raise falcon.HTTPMovedPermanently("/")


class ConfirmDeleteAccountResource(object):
    def on_get(self, req, resp):
        token = req.context["db"].add_token("login", req.context["user"])
        resp.body = deletepage(token)
        resp.content_type = "text/html; charset=utf-8"


class FinishDeleteAccountResource(object):
    def on_get(self, req, resp):
        req.context["db"].delete_user(req.context["user"])
        resp.body = msgpage("Account Deleted", "Your account has been deleted.")
        resp.content_type = "text/html; charset=utf-8"


config_file = "/home/protected/db.conf"
middleware = [DatabaseMiddleware(config_file), SessionMiddleware()]
app = falcon.API(middleware=middleware)

app.add_route("/account/delete", DeleteAccountResource())
app.add_route("/account/delete/confirm", ConfirmDeleteAccountResource())
app.add_route("/account/delete/finish", FinishDeleteAccountResource())
app.add_route("/{user}", ListResource())
app.add_route("/", HomeResource())
