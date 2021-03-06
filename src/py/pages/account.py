########
# Account Pages
########

from .base import base

# TODO localization of strings

permission_text = '''I grant permission for my email address and whatever 
language information I add to my account to be stored and processed in the 
EU, by the administrator(s) of TalkToMeIn.com. I understand that my language 
information will be public, and will occasionally be used in anonymized form to 
generate statistical analyses for publication, but that my email address will 
be used only for authentication and site-related technical announcements. I can 
permanently delete my account at any time, at which point my data will be 
deleted from TalkToMeIn's database immediately and from all backups within 30 
days.'''

marketing_emails_text = '''I would like to receive marketing emails and 
announcements concerning products created or endorsed by the creator of
TalkToMeIn.com (no more than one message per month, and usually much less).
Email addresses are not shared with third parties.'''


indexfmt = '''
<h3>Account Details</h3>
<form>
    <p><input type="checkbox" name="marketing" value="true" %s>%s</p>
</form>
<hr>
<a id="deleteacct" href="/account/delete/confirm">Delete Account</a>
<hr>
<a href="/">Back to edit page</a>
'''

def index(marketing_emails):
    return base("Account Details", 
                indexfmt % ("checked" if marketing_emails else "",
                            marketing_emails_text), 
                ["general", "account"],
                ["account"])


delete_text = '''
<p>
    Are you sure you want to delete your account?
    This action is not reversible.
</p>
<a id="deleteacct" href="/account/delete">Send Delete Link</a>
'''

def confirm_delete():
    return base("Confirm Account Deletion", delete_text, ["general"])


addfmt = '''
<form method="POST">
    %s
    <input type="text" name="username" placeholder="Username" required>
    <input type="text" name="email" placeholder="Email" required>
    <p><input type="checkbox" name="permission" value="true" required>%s</p>
    <p><input type="checkbox" name="marketing" value="true">%s</p>
    <button type="submit">Create Account</button>
</form>'
'''

failmsgfmt = '<p class="failmsg">%s</p>'

def create(failmsg=None):
    return base("Create Account", 
                addfmt % (failmsgfmt % failmsg if failmsg else "", 
                          permission_text,
                          marketing_emails_text),
                ["general", "create-account"])
