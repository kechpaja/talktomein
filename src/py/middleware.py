#####
# Middleware for session management in Nyelv
#####

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from .db import DatabaseWrapper

cookiename = "talktomein-session"

class SessionMiddleware(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, salt="login")
        self.session_signer = URLSafeTimedSerializer(secret, salt="session")

    def process_request(self, req, resp):
        if req.path in ["/", "/account/delete"]:
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
                if "email" in req.params and req.params["email"]:
                    # Add user or update user email
                    # TODO we can get rid of this is we create "is confirmed"
                    # TODO flag in users table of database.
                    # TODO Update DB so we don't need to create it here.
                    db = DatabaseWrapper("/home/protected/db.conf")
                    db.add_user(user, req.params["email"])
                return
            except BadSignature:
                # TODO this might have security implications. Log?
                pass
            except (SignatureExpired, KeyError):
                pass

            # This will work fine even if there's no cookie
            if "action" in req.params and req.params["action"] == "logout":
                resp.set_cookie(cookiename, 
                                "", 
                                domain="talktomein.com",
                                path="/",
                                max_age=0)
                return

            try:
                req.context["user"] = self.session_signer.loads(
                    req.cookies[cookiename],
                    max_age=21600
                )
            except BadSignature:
                pass # TODO log for security purposes
            except (SignatureExpired, KeyError):
                pass # Expired session or no cookie

        elif req.path in ["/account/delete/confirm", "/account/delete/finish"]:
            try:
                req.context["user"] = self.login_signer.loads(
                    req.params["token"],
                    max_age=600
                )
            except BadSignature:
                raise falcon.HTTPMovedPermanently("/") # TODO again,red flag
            except (SignatureExpired, KeyError):
                raise falcon.HTTPMovedPermanently("/") # TODO msg page?
