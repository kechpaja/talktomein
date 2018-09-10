################################################################################
# Email Sending Library                                                        #
################################################################################

import os

def send_link(token, address):
    msg = '''Subject: Login Link
To: %s

Login link: https://kechpaja.com/langlist?token=%s''' % (address, token)
    with os.popen("/usr/bin/sendmail -t", "w") as f:
        f.write(msg)
