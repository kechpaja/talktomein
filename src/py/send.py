################################################################################
# Email Sending Library                                                        #
################################################################################

import os


msgfmt = '''Subject: [TalkToMeIn] %s
From: kechpaja@kechpaja.com
To: %s

%s: https://talktomein.com%s
'''

def link(to, subject, msg, path, token=None):
    path += "?token=" + token if token else ""
    path = "/" + path if not path.startswith("/") else path
    with os.popen("/usr/bin/sendmail -t", "w") as f:
        f.write(msgfmt % (subject, to, msg, path))
