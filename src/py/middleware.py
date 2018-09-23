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
        if req.path in ["/account/create/finish", "/account/delete/finish"]:
            return # Bypass cookie checker for pages that require token

        if req.path.startswith("/account/login/finish/"):
            return # Same thing

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
        if "user" in req.context and req.context["user"]:
            self.set_cookie(req, resp)
        else:
            self.unset_cookie(req, resp)
