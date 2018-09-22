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

    def unset_cookie(self, rsp):
        rsp.set_cookie(cookiename,"",domain="talktomein.com",path="/",max_age=0)

    def set_cookie(self, req, resp):
        resp.set_cookie(cookiename,
                        self.session_signer.dumps(req.context["user"]),
                        domain="talktomein.com",
                        path="/",
                        max_age=21600, # XXX 6 hours
                        http_only=False)

    def process_request(self, req, resp):
        if req.path in ["/", "/account/delete", "/update"]:
            try:
                user = self.login_signer.loads(req.params["token"], 
                                               max_age=600)
                req.context["user"] = user
                self.set_cookie(req, resp)
                return
            except BadSignature:
                # TODO this might have security implications. Log?
                pass
            except (SignatureExpired, KeyError):
                pass

            # This will work fine even if there's no cookie
            if "action" in req.params and req.params["action"] == "logout":
                self.unset_cookie(resp)
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

    def process_response(self, req, resp, resource, req_succeeded):
        if req.path == "/account/delete/finish" and req_succeeded:
            self.unset_cookie(resp)

        elif req.path == "/account/create/finish" and req_succeeded:
            self.set_cookie(req, resp)
