#####
# Middleware for session management in Nyelv
#####

from .db import DatabaseWrapper

cookiename = "talktomein-session"

class DatabaseMiddleware(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def process_request(self, req, resp):
        req.context["db"] = DatabaseWrapper(self.config_file)

    def process_response(self, req, resp, resource, req_succeeded):
        req.context["db"].disconnect()


class SessionMiddleware(object):
    # todo must be a lambda taking one argument, the user ID
    def set_user_then(self, req, then=lambda user: None):
        user = req.context["db"].get_token_user("logins", req.params["token"])
        if not user:
            return False
        req.context["user"] = user
        then(user)
        return True

    def process_request(self, req, resp):
        if req.path == "/":
            def set_cookie(user):
                resp.set_cookie(cookiename,
                                req.context["db"].add_token("session", user),
                                domain="myalect.com",
                                path="/",
                                max_age=3600,
                                http_only=False)

            if "token" in req.params and self.set_user_then(req, set_cookie):
                req.context["db"].delete_token("login", req.params["token"])
                del req.params["token"]

            elif cookiename in req.cookies:
                cookie = req.cookies[cookiename]
                if "action" in req.params and req.params["action"] == "logout":
                    req.context["db"].delete_token("session", cookie)
                    resp.unset_cookie(cookiename)
                else:
                    user = req.context["db"].get_token_user("session", cookie)
                    if user:
                        req.context["user"] = user
                    else:
                        resp.unset_cookie(cookiename)
