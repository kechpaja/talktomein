#####
# Middleware for session management in Nyelv
#####

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from .db import DatabaseWrapper

cookiename = "talktomein-session"

class DatabaseMiddleware(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def process_request(self, req, resp):
        req.context["db"] = DatabaseWrapper(self.config_file)

    def process_response(self, req, resp, resource, req_succeeded):
        req.context["db"].disconnect()


# TODO Revisit this entire class. It could use cleanup. 
class SessionMiddleware(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, salt="login")
        self.session_signer = URLSafeTimedSerializer(secret, salt="session")

    # "then" must be a lambda taking one argument, the user ID
    def set_user_then(self, req, then=lambda user: None):
        try:
            req.context["user"] = self.login_signer.loads(req.params["token"],
                                                          max_age=600)
        except BadSignature:
            # TODO what do we do here? Tell user why token failed?
            return False
        except SignatureExpired:
            return False # TODO probably tell user about this one
        then(req.context["user"])
        return True

    def process_request(self, req, resp):
        if req.path in ["/", "/account/delete"]:
            def set_cookie(user):
                resp.set_cookie(cookiename,
                                self.session_signer.dumps(user),
                                domain="talktomein.com",
                                path="/",
                                max_age=21600, # XXX 6 hours
                                http_only=False)

            if "token" in req.params and self.set_user_then(req, set_cookie):
                del req.params["token"]
                if "email" in req.params and req.params["email"]:
                    # Add user or update user email
                    req.context["db"].add_user(req.context["user"], 
                                               req.params["email"])
                    del req.params["email"]

            elif cookiename in req.cookies:
                cookie = req.cookies[cookiename]
                if "action" in req.params and req.params["action"] == "logout":
                    resp.unset_cookie(cookiename)
                else:
                    try:
                        req.context["user"] = self.session_signer.loads(
                            cookie,
                            max_age=21600
                        )
                    except BadSignature:
                        resp.unset_cookie(cookiename) # TODO this is troubling
                    except SignatureExpired:
                        resp.unset_cookie(cookiename)

        elif req.path in ["/account/delete/confirm", "/account/delete/finish"]:
            if "token" in req.params and self.set_user_then(req):
                del req.params["token"]
            else:
                raise falcon.HTTPMovedPermanently("/") # TODO "auth required"?
