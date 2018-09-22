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


addfmt = '''
<form method="POST">
    %s
    <input type="text" name="username" placeholder="Username" required>
    <input type="text" name="email" placeholder="Email" required>
    <p><input type="checkbox" name="permission" value="true" required>%s</p>
    <p><input type="checkbox" name="newsletter" value="true">%s</p>
    <p><input type="checkbox" name="marketing_emails" value="true">%s</p>
    <button type="submit">Create Account</button>
</form>'
'''

failmsgfmt = '<p class="failmsg">%s</p>'

permission_text = '''I grant permission for my email address and whatever 
language information I add to my account to be stored on and processed by 
server(s) controlled by the administrator(s) of TalkToMeIn.com. I understand
that my language information will be public, but that my email address will be
used only for authentication and site-related technical announcements.'''

newsletter_text = '''I would like to receive the TalkToMeIn newsletter (usually
no more than one message per month).'''

marketing_emails_text = '''I would like to receive marketing emails and 
announcements concerning products created or endorsed by the creator of
TalkToMeIn.com (no more than one message per month, and usually much less).
Email addresses are not shared with third parties.'''

def create(failmsg=None):
    return base("Create Account", 
                addfmt % (failmsgfmt % failmsg if failmsg else "", 
                          permission_text, 
                          newsletter_text, 
                          marketing_emails_text),
                ["general", "create-account"])
