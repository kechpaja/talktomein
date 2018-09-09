#######
# Emails
#######

import os

class Mailer(object):
    def sendmsg(self, headers, body):
        hdrs = "\n".join([h + ": " + headers[h] for h in headers.keys()])
        with os.popen("/usr/bin/sendmail -t", "w") as f:
            f.write(hdrs + "\n\n" + body)

    def send_link(self, token, address):
        headers = {
            "To": address,
            "Subject": "Login Link"
        }
        body = "Login link: https://kechpaja.com/langlist?token=" + token
        self.sendmsg(headers, body)
