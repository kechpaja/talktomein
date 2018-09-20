################################################################################
# Email Sending Library                                                        #
################################################################################

import os


msgfmt = '''Subject: [TalkToMeIn] %s
From: kechpaja@kechpaja.com
To: %s

%s: https://talktomein.com%s?%s
'''

def link(to, subject, msg, path, params):
    with os.popen("/usr/bin/sendmail -t", "w") as f:
        f.write(msgfmt % (subject, 
                          to, 
                          msg,
                          path,
                          "&".join("%s=%s" % p for p in params.items())))
