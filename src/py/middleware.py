################################################################################
# Middleware for Session Management                                            #
################################################################################

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from . import db

cookiename = "talktomein-session"

class SessionMiddleware(object):
    def __init__(self, secret):
        self.session_signer = URLSafeTimedSerializer(secret, salt="session")

    def process_request(self, req, resp):
        # Bypass cookie checker for pages that require token
        if not re.match("/account/[^/]*/finish.*", req.path):
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
            # TODO check if cookie exists and is for current user?
            # TODO perhaps require user to log out before they can log in again. 
            resp.set_cookie(cookiename,
                            self.session_signer.dumps(req.context["user"]),
                            domain="talktomein.com",
                            path="/",
                            max_age=21600, # XXX 6 hours
                            http_only=False)
        else:
            cookies = req.cookies
            if cookiename in cookies and cookies[cookiename]:
                resp.set_cookie(cookiename,
                                "",
                                domain="talktomein.com",
                                path="/",
                                max_age=0)
