#####
# Main 
####

import falcon
import json
import re
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from urllib.parse import unquote

from . import db
from . import pages
from . import send
from .middleware import SessionMiddleware

class HomeResource(object):
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
            token = login_signer.dumps(username)
            if address:
                send.link(address, 
                          "Login Link",
                          "Click the link to log in",
                          "/account/login/finish/" + token,
                          "")
                resp.body = pages.message.login_link_sent(username) 
            else:
                resp.body = pages.home("Username not found.")
        else:
            resp.body = pages.home()
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class FinishCreateAccountResource(object):
    def on_get(self, req, resp):
        try:
            data = create_signer.loads(req.params["token"])
            db.add_user(**data)
            req.context["user"] = data["username"]
            resp.body = pages.message.account_activated()
            resp.content_type = "text/html; charset=utf-8"
        except (BadSignature, SignatureExpired, KeyError):
            # TODO log secutiry issues
            falcon.HTTPMovedPermanently("/") # TODO redirect to error page


class CreateAccountResource(object):
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
                      "accounts", "blog", "news", "update"]
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
                          create_signer.dumps({
                              "username" : username,
                              "email" : email,
                              "permission" : int("permission" in data),
                              "newsletter" : int("newsletter" in data),
                              "marketing" : int("marketing_emails" in data)
                          }))
                resp.body = pages.message.activation_link_sent(username)
            resp.content_type = "text/html; charset=utf-8"
        else:
            raise falcon.HTTPBadRequest() # TODO error message?


class UpdateResource(object):
    def on_post(self, req, resp):
        try:
            data = json.loads(req.stream.read().decode("utf-8"))
            # TODO block malicious poster from adding junk language names
            if "level" in data and data["level"] not in ["A", "B", "C"]:
                resp.body = '{"ok" : false}'
            else:
                db.update_lang(req.context["user"], 
                               data["language"], 
                               data["level"] if "level" in data else None)
                resp.body = '{"ok" : true}'
        except KeyError:
            raise falcon.HTTPForbidden()


class ListResource(object):
    def on_get(self, req, resp, user):
        if db.get_user_email(user):
            resp.body = pages.display_languages(db.user_langs(user), user)
        else:
            resp.body = pages.message.no_such_user(user)
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


class DeleteAccountResource(object):
    def on_get(self, req, resp):
        if "user" in req.context and req.context["user"]:
            user = req.context["user"]
            send.link(db.get_user_email(user),
                      "Delete Account Link",
                      "Click the link to permanently delete your account",
                      "/account/delete/finish",
                      delete_signer.dumps(user))
            req.context["user"] = "" # Log user out
            resp.body = pages.message.deletion_link_sent(user)
            resp.content_type = "text/html; charset=utf-8"
        else:
            raise falcon.HTTPMovedPermanently("/")


class ConfirmDeleteAccountResource(object):
    def on_get(self, req, resp):
        try:
            resp.body = pages.confirm_delete_account()
            resp.content_type = "text/html; charset=utf-8"
        except KeyError:
            raise falcon.HTTPMovedPermanently("/")


class FinishDeleteAccountResource(object):
    def on_get(self, req, resp):
        if "user" not in req.context or not req.context["user"]:
            try:
                db.delete_user(delete_signer.loads(req.params["token"],
                                                   max_age=600))
                resp.body = pages.message.account_deleted()
            except (BadSignature, SignatureExpired, KeyError):
                raise falcon.HTTPMovedPermanently("/")
        else:
            resp.body = pages.message.cannot_delete_when_logged_in()
        resp.content_type = "text/html; charset=utf-8" 

class LogoutResource(object):
    def on_get(self, req, resp):
        req.context["user"] = ""
        resp.body = pages.message.logout()
        resp.content_type = "text/html; charset=utf-8"


class FinishLoginResource(object):
    def on_get(self, req, resp, token):
        try:
            req.context["user"] = login_signer.loads(token, max_age=600)
        except (BadSignature, SignatureExpired):
            pass # TODO log security red flags
        raise falcon.HTTPMovedPermanently("/")


class AccountResource(object):
    def on_get(self, req, resp):
        resp.body = pages.account()
        resp.content_type = "text/html; charset=utf-8"


# Get the signing secret and create signers
with open("/home/protected/signing_secret", "rb") as f:
    secret = f.read()

login_signer = URLSafeTimedSerializer(secret, salt="login")
create_signer = URLSafeTimedSerializer(secret, salt="create")
delete_signer = URLSafeTimedSerializer(secret, salt="delete")

app = falcon.API(middleware=[SessionMiddleware(secret)])

app.add_route("/account", AccountResource())
app.add_route("/account/create", CreateAccountResource())
app.add_route("/account/create/finish", FinishCreateAccountResource())
app.add_route("/account/delete", DeleteAccountResource())
app.add_route("/account/delete/confirm", ConfirmDeleteAccountResource())
app.add_route("/account/delete/finish", FinishDeleteAccountResource())
app.add_route("/account/login/finish/{token}", FinishLoginResource())
app.add_route("/logout", LogoutResource())
app.add_route("/update", UpdateResource())
app.add_route("/{user}", ListResource())
app.add_route("/", HomeResource())
