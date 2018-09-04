#####
# Main 
####

import falcon
import json

# TODO import pages

# TODO port fetchuserlangs()

class BadTokenResource(object):
    def on_get(self, req, resp):
        pass # TODO page user lands on when login link is no longer usable. 
        # TODO should explain why, and explain possible security issues. 

class HomeResource(object):
    def on_get(self, req, resp):
        pass # TODO display home page, with login flow, some info about the
         # TODO website, and eventually also a flow to create an account

class ListResource(object):
    def on_get(self, req, resp, user):
        resp.body = pages.genpage(req.context["db"].user_langs(user),
                                  user + " speaks:")
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

class LoginResource(object):
    def on_get(self, req, resp):
        pass # TODO display login page (telling user they need to log in)
        # TODO there will be login logic on home as well, login page provides
        # TODO only the login flow, and nothing else

class UpdateResource(object):
    def on_get(self, req, resp):
        resp.body = genpage(req.context["db"].user_langs(req.context["user"]), 
                            "Edit language list",
                            req.context["db"].all_langs())
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode("utf-8"))
        languages = [[user, lang, data[lang]] for lang in data.keys()]
        req.context["db"].update_langs(req.context["user"], languages)

        # TODO response body? 
        resp.status = falcon.HTTP_200


# TODO create app, with middleware

# TODO create routes
