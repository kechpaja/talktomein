################################################################################
# Email Sending Library                                                        #
################################################################################

import os

def send_link(token, address, update_address=False):
    msg = '''Subject: Login Link
From: kechpaja@kechpaja.com
To: %s

Login link: https://talktomein.com/?token=%s''' % (address, token)
    msg += ("&email=%s" % address if update_address else "")
    with os.popen("/usr/bin/sendmail -t", "w") as f:
        f.write(msg)
