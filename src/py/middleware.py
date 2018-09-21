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

    def process_request(self, req, resp):
        if req.path in ["/", "/account/delete"]:
            def unset_cookie():
                resp.set_cookie(cookiename,
                                "",
                                domain="talktomein.com",
                                path="/",
                                max_age=0)

            try:
                user = self.login_signer.loads(req.params["token"], 
                                               max_age=600)
                req.context["user"] = user
                resp.set_cookie(cookiename,
                                self.session_signer.dumps(user),
                                domain="talktomein.com",
                                path="/",
                                max_age=21600, # XXX 6 hours
                                http_only=False)
                del req.params["token"] # Not strictly necessary
                if "email" in req.params and req.params["email"]:
                    # Add user or update user email
                    # TODO we can get rid of this is we create "is confirmed"
                    # TODO flag in users table of database. 
                    req.context["db"].add_user(user, req.params["email"])
                    del req.params["email"] # Not strictly necessary
                return
            except BadSignature:
                # TODO this might have security implications. Log?
                pass
            except (SignatureExpired, KeyError):
                pass

            # This will work fine even if there's no cookie
            if "action" in req.params and req.params["action"] == "logout":
                unset_cookie()

            try:
                req.context["user"] = self.session_signer.loads(
                    req.cookies[cookiename]
                    max_age=21600
                )
            except BadSignature:
                unset_cookie() # TODO log for security purposes
            except (SignatureExpired, KeyError):
                pass # Expired session or no cookie

        elif req.path in ["/account/delete/confirm", "/account/delete/finish"]:
            try:
                req.context["user"] = self.login_signer.loads(
                    req.params["token"]
                    max_age=600
                )
                del req.params["token"]
            except BadSignature:
                raise falcon.HTTPMovedPermanently("/") # TODO again,red flag
            except (SignatureExpired, KeyError):
                raise falcon.HTTPMovedPermanently("/") # TODO msg page?
