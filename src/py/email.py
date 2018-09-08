#######
# Emails
#######

#import requests

class Mailer(object):
    def __init__(self):
        self.apikey = "" # TODO get API token from file, etc
        self.uribase = "https://api.elasticemail.com/v2/"

    def mkreq(self, verb, options):
        newopts = dict((o, options[o]) for o in options)
        newopts["apikey"] = self.apikey
        return requests.get(self.uribase + verb, params=newopts)

    def send_link(self, token, address):
        options = {}
        options["msgTo"] = address

        # TODO Probably should give user more than just the link
        options["bodyText"] = "https://kechpaja.com/langlist?token=" + token

 #       resp = self.mkreq("email/send", options)
