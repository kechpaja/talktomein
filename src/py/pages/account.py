########
# Account Pages
########

from .base import base

# TODO localization of strings

deletefmt = '''
<p>
    Are you sure you want to delete your account?
    This action is not reversible.
</p>
<a id="deleteacct" href="/account/delete/finish?token=%s">
    Delete My Account
</a>
'''

def confirm_delete(token):
    return base("Confirm Account Deletion", deletefmt % token, ["general"])
