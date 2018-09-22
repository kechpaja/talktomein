###########
# Message Pages
###########

from .base import base

msgfmt = "<p>%s</p><p><a href=\"/\">Home</a></p>"

def message(title, msg):
    return base(title, msgfmt % msg, ["general"])

def login_link_sent(username):
    return message("Login Link Sent", 
                   "A login link has been sent to %s." % username)

def activation_link_sent(username):
    return message("Activation Link Sent",
                   "An activation link has been sent to %s." % username)

def account_activated():
    return message("Account Activated",
                   "Your account has been successfully activated.")

def deletion_link_sent(username):
    return message("Deletion Link Sent",
                   "An account deletion link has been sent to %s." % username)

def account_deleted():
    return message("Account Deleted", "Your account has been deleted.")

def logout():
    return message("Logged Out", "You have been logged out.")
