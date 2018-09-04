#####
# Middleware for session management in Nyelv
#####

# TODO import database from our code

cookiename = "nyelv-session"

class DatabaseMiddleware(object):
    def __init__(self, config_file):
        self.db = db.DatabaseWrapper(config_file)

    def process_request(self, req, resp):
        req.context["db"] = self.db

    def process_response(self, req, resp, resource, req_succeeded):
        req.context["db"].disconnect()


class SessionMiddleware(object):
    def process_request(self, req, resp):
        # TODO should there be a cookie-deleting logout page?
        if req.path == "/update":
            if "token" in req.params:
                user = req.context["db"].get_token_user(req.params["token"])
                if not user:
                    pass # TODO redirect to login link failure page
                    return
                req.context["db"].delete_token(req.params["token"])
                del req.params["token"] # XXX is this a good idea?

                resp.set_cookie(cookiename,
                                req.context["db"].add_token(user),
                                domain="kechpaja.com",
                                path="/nyelv/",
                                max_age=3600,
                                http_only=False)
                req.context["user"] = user
                return

            elif cookiename in req.cookies:
                user = req.context["db"].get_token_user(req.cookies[cookiename])
                if user:
                    req.context["user"] = user
                    return

            req.path = "/login" # Change route to login page
        elif req.path == "/logout": # TODO do this with JS query?
            if cookiename in req.cookies:
                req.context["db"].delete_token(req.cookies[cookiename])
                resp.unset_cookie(cookiename)
            req.path = "/"

    def process_resource(self, req, resp, resource, params):
        if req.context["user"]:
            resource.user = req.context["user"]
