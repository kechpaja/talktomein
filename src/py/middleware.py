#####
# Middleware for session management in Nyelv
#####

from .db import DatabaseWrapper

cookiename = "nyelv-session"

class DatabaseMiddleware(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def process_request(self, req, resp):
        req.context["db"] = DatabaseWrapper(self.config_file)

    def process_response(self, req, resp, resource, req_succeeded):
        req.context["db"].disconnect()


class SessionMiddleware(object):
    def process_request(self, req, resp):
        if req.path == "/":
            if "token" in req.params:
                user = req.context["db"].get_token_user(req.params["token"])
                if user:
                    req.context["db"].delete_token(req.params["token"])
                    del req.params["token"] # XXX is this a good idea?

                    resp.set_cookie(cookiename,
                                    req.context["db"].add_token(user),
                                    domain="kechpaja.com",
                                    path="/nyelv/",
                                    max_age=3600,
                                    http_only=False)
                    req.context["user"] = user

            elif cookiename in req.cookies:
                cookie = req.cookies[cookiename]
                if req.params["action"] == "logout":
                    req.context["db"].delete_token(cookie)
                    resp.unset_cookie(cookiename)
                else:
                    user = req.context["db"].get_token_user(cookie)
                    if user:
                        req.context["user"] = user
                    else:
                        resp.unset_cookie(cookiename)
