################################################################################
# Email Sending Library                                                        #
################################################################################

import os


msgfmt = '''Subject: [TalkToMeIn] %s
From: kechpaja@kechpaja.com
To: %s

%s: https://talktomein.com%s

If you receive several of these messages that you did not yourself send,
it may indicate that someone is attempting to hack into your account. If
you are concerned, feel free to contact us by replying to this message.
'''

def link(to, subject, msg, path, token=None):
    path += "?token=" + token if token else ""
    path = "/" + path if not path.startswith("/") else path
    with os.popen("/usr/bin/sendmail -t", "w") as f:
        f.write(msgfmt % (subject, to, msg, path))
