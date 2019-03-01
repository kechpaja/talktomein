################################################################################
# Middleware for Session Management                                            #
################################################################################

from . import db

cookiename = "talktomein-session"

class SessionMiddleware(object):
    def process_request(self, req, resp):
        cookies = req.cookies
        if cookiename in cookies and cookies[cookiename]:
            user = db.get_token_user("sessions", cookies[cookiename])
            if user:
                req.context["user"] = user
        # TODO message page if session is expired or not present?

    def process_response(self, req, resp, resource, req_succeeded):
        if "user" in req.context and req.context["user"]:
            cookies = req.cookies
            user = req.context["user"]
            if cookiename in cookies and cookies[cookiename] \
                and user != db.get_token_user("sessions", cookies[cookiename]):
                db.end_session(cookies[cookiename])
                token = str(db.add_token("sessions", req.context["user"]))
            elif cookiename in cookies and cookies[cookiename]:
                token = cookies[cookiename]
            else:
                token = str(db.add_token("sessions", req.context["user"]))

            resp.set_cookie(cookiename,
                            token,
                            domain="talktomein.com",
                            path="/",
                            max_age=21600,
                            http_only=False)

        else:
            cookies = req.cookies
            if cookiename in cookies and cookies[cookiename]:
                db.end_session(cookies[cookiename])
                resp.set_cookie(cookiename,
                                "",
                                domain="talktomein.com",
                                path="/",
                                max_age=0)
