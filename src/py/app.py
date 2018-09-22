#####
# Main 
####

import falcon
import json
import re
from itsdangerous import URLSafeTimedSerializer
from urllib.parse import unquote

from . import db
from . import pages
from . import send
from .middleware import SessionMiddleware
from .page import homepage
from .page import langpage

class HomeResource(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, salt="login")

    def on_get(self, req, resp):
        if "user" in req.context and req.context["user"]:
            user = req.context["user"]
            resp.body = langpage(db.user_langs(user), user, db.all_langs())
        else:
            resp.body = homepage()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        # Form submission to send login link
        reqbody = req.stream.read().decode("utf-8")
        data = dict(tuple(f.split("=")) for f in reqbody.split("&"))
        if "username" in data and data["username"]:
            username = data["username"]
            address = db.get_user_email(username)
            if address and "email" in data and data["email"]:
                resp.body = homepage("Username is in use.", True)
            elif address:
                send.link(address, 
                          "Login Link",
                          "Click the link to log in",
                          "/",
                          {"token" : self.login_signer.dumps(username)})
                resp.body = pages.message.login_link_sent(username)
            elif "email" in data and data["email"]:
                address = unquote(data["email"])
                banned = ["login", "logout", "contact", "about", "api",
                          "account", "accounts", "blog"]
                if not re.match("\w+", username) or username in banned:
                    resp.body = homepage("Invalid username. ", True)
                elif not re.match("[^@]+\@([^@.]+.)+\.[^@.]", address):
                    resp.body = homepage("Invalid email. ", True)
                else:
                    send.link(address,
                              "Activation Link",
                              "Click the link to activate your account",
                              "/",
                              {"token" : self.login_signer.dumps(username),
                               "email" : address})
                    resp.body = pages.message.activation_link_sent(username)
            else:
                resp.body = homepage("Username not found.")
        else:
            resp.body = homepage()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class UpdateResource(object):
    def on_post(self, req, resp):
        try:
            data = json.loads(req.stream.read().decode("utf-8"))
            for l in data:
                if data[l] not in ["A", "B", "C"]:
                    del data[l]
            db.update_langs(req.context["user"], data)
            resp.body = "{\"ok\" : true}"
        except KeyError:
            raise falcon.HTTPForbidden()


class ListResource(object):
    def on_get(self, req, resp, user):
        resp.body = langpage(db.user_langs(user), user)
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class DeleteAccountResource(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, salt="login")

    def on_get(self, req, resp):
        if "user" in req.context and req.context["user"]:
            user = req.context["user"]
            send.link(db.get_user_email(user),
                      "Delete Account Link",
                      "Click the link to continue deleting your account",
                      "/account/delete/confirm",
                      {"token" : self.login_signer.dumps(user)})
            resp.body = pages.message.deletion_link_sent(user)
            resp.content_type = "text/html; charset=utf-8"
        else:
            raise falcon.HTTPMovedPermanently("/")


class ConfirmDeleteAccountResource(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, "login")

    def on_get(self, req, resp):
        token = self.login_signer.dumps(req.context["user"])
        resp.body = pages.confirm_delete_account(token)
        resp.content_type = "text/html; charset=utf-8"


class FinishDeleteAccountResource(object):
    def on_get(self, req, resp):
        db.delete_user(req.context["user"])
        resp.body = pages.message.account_deleted()
        resp.content_type = "text/html; charset=utf-8"


# Get the signing secret
with open("/home/protected/signing_secret", "rb") as f:
    secret = f.read()

app = falcon.API(middleware=[SessionMiddleware(secret)])

app.add_route("/account/delete", DeleteAccountResource(secret))
app.add_route("/account/delete/confirm", ConfirmDeleteAccountResource(secret))
app.add_route("/account/delete/finish", FinishDeleteAccountResource())
app.add_route("/update", UpdateResource())
app.add_route("/{user}", ListResource())
app.add_route("/", HomeResource(secret))
