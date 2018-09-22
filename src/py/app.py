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

class HomeResource(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, salt="login")

    def on_get(self, req, resp):
        if "user" in req.context and req.context["user"]:
            user = req.context["user"]
            resp.body = pages.update_languages(db.user_langs(user), 
                                               user, 
                                               db.all_langs())
        else:
            resp.body = pages.home()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        # Form submission to send login link
        reqbody = req.stream.read().decode("utf-8")
        data = dict(tuple(f.split("=")) for f in reqbody.split("&"))
        if "username" in data and data["username"]:
            username = data["username"]
            address = db.get_user_email(username)
            if address:
                send.link(address, 
                          "Login Link",
                          "Click the link to log in",
                          "/",
                          self.login_signer.dumps(username))
                resp.body = pages.message.login_link_sent(username) 
            else:
                resp.body = pages.home("Username not found.")
        else:
            resp.body = pages.home()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class FinishCreateAccountResource(object):
    def __init__(self, secret):
        self.create_signer = URLSafeTimedSerializer(secret, salt="create")

    def on_get(self, req, resp):
        try:
            data = self.create_signer.loads(req.params["token"])

            # TODO check if user is already there
            db.add_user(data["username"], data["email"])
            req.context["user"] = data["username"]
            resp.body = pages.message.account_activated()
            resp.content_type = "text/html; charset=utf-8"
        except (BadSignature, SignatureExpired, KeyError):
            # TODO log secutiry issues
            falcon.HTTPMovedPermanently("/") # TODO redirect to error page


class CreateAccountResource(object):
    def __init__(self, secret):
        self.create_signer = URLSafeTimedSerializer(secret, salt="create")

    def on_get(self, req, resp):
        resp.body = pages.create_account()
        resp.content_type = "text/html; charset=utf-8"

    def on_post(self, req, resp):
        reqbody = req.stream.read().decode("utf-8")
        data = dict(tuple(f.split("=")) for f in reqbody.split("&"))
        required_fields = ["username", "email", "permission"]
        if all(k in data.keys() for k in required_fields):
            username = data["username"]
            email = unquote(data["email"])
            banned = ["login", "logout", "contact", "about", "api", "account", 
                      "accounts", "blog", "update"]
            if db.get_user_email(data["username"]):
                resp.body = pages.create_account("Username is taken")
            elif not re.match("\w+", username) or username in banned:
                resp.body = pages.create_account("Invalid username")
            elif not re.match("[^@]+\@([^@.]+.)+\.[^@.]", email):
                resp.body = pages.create_account("Invalid email")
            else:
                send.link(email,
                          "Activation Link",
                          "Click the link to activate your account",
                          "/account/create/finish",
                          self.create_signer.dumps({"username" : username,
                                                    "email" : email}))
                resp.body = pages.message.activation_link_sent(username)
            resp.content_type = "text/html; charset=utf-8"
        else:
            raise falcon.HTTPBadRequest() # TODO error message?


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
        resp.body = pages.display_languages(db.user_langs(user), user)
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
                      self.login_signer.dumps(user))
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

app.add_route("/account/create", CreateAccountResource(secret))
app.add_route("/account/create/finish", FinishCreateAccountResource(secret))
app.add_route("/account/delete", DeleteAccountResource(secret))
app.add_route("/account/delete/confirm", ConfirmDeleteAccountResource(secret))
app.add_route("/account/delete/finish", FinishDeleteAccountResource())
app.add_route("/update", UpdateResource())
app.add_route("/{user}", ListResource())
app.add_route("/", HomeResource(secret))
