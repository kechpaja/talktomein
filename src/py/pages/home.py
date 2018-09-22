#############
# Home Page
#############

from .base import base

# TODO This should be split up more, but I can't do that without adding
# another endpoint, which should happen in an entirely separate branch. 

def home(failmsg=None, newacct=False):
    if newacct:
        title = "Create a new account"
        body = '''<form method="POST">%s
            <input type="text" name="username" placeholder="Username" required>
            <input type="text" name="email" placeholder="Email" required>
            <button type="submit">Submit</button></form>'''
    else:
        title = "Log in to edit language list"
        body = '''<form method="POST">%s
            <input type="text" name="username" placeholder="Username" required>
            <button type="submit">Send login link</button>
            <button id="newacct">Create New Account</button></form>
            <script type="text/javascript" src="/js/home.js"></script>'''
    body = body % (("<p class='failmsg'>%s</p>" % failmsg) if failmsg else "")
    return base(title, body, ["general"])
