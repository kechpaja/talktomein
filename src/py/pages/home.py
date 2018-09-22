#############
# Home Page
#############

from .base import base

# TODO This should be split up more, but I can't do that without adding
# another endpoint, which should happen in an entirely separate branch. 

def home(failmsg=None):
    title = "Log in to edit language list"
    body = '''<form method="POST">%s
        <input type="text" name="username" placeholder="Username" required>
        <button type="submit">Send login link</button>
        <a id="newacct" href="/account/create">Create New Account</a></form>
        </script>'''
    body = body % (("<p class='failmsg'>%s</p>" % failmsg) if failmsg else "")
    return base(title, body, ["general"])
