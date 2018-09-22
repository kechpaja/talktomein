#####
# Middleware for session management in Nyelv
#####

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from . import db

cookiename = "talktomein-session"

class SessionMiddleware(object):
    def __init__(self, secret):
        self.login_signer = URLSafeTimedSerializer(secret, salt="login")
        self.session_signer = URLSafeTimedSerializer(secret, salt="session")

    def unset_cookie(self, req, resp):
        cookies = req.cookies
        if cookiename in cookies and cookies[cookiename]:
            resp.set_cookie(cookiename,
                            "",
                            domain="talktomein.com",
                            path="/",
                            max_age=0)

    def set_cookie(self, req, resp):
        # TODO check if cookie exists and is for current user?
        # TODO perhaps require user to log out before they can log in again. 
        resp.set_cookie(cookiename,
                        self.session_signer.dumps(req.context["user"]),
                        domain="talktomein.com",
                        path="/",
                        max_age=21600, # XXX 6 hours
                        http_only=False)

    def process_request(self, req, resp):
        try:
            req.context["user"] = self.login_signer.loads(req.params["token"],
                                                          max_age=600)
            return
        except BadSignature:
            pass # TODO log security red flag
        except (SignatureExpired, KeyError):
            pass # Expired session or no token

        if req.path not in ["/account/delete/confirm","/account/delete/finish"]:
            try:
                req.context["user"] = self.session_signer.loads(
                    req.cookies[cookiename],
                    max_age=21600
                )
            except BadSignature:
                pass # TODO again,red flag
            except (SignatureExpired, KeyError):
                pass # TODO msg page?

    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            if "user" in req.context and req.context["user"]:
                self.set_cookie(req, resp)
            else:
                self.unset_cookie(req, resp)
