#######
# Pages
######

# XXX langlist = list of all possible languages

def generalpage(title, insides, css):
    acc = "<html><head><title>" + title + '''</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">'''
    for f in css:
        acc += "<link rel='stylesheet' type='text/css' href='%s'>" % f
    return acc + "</head><body>" + insides + "</body></html>"

def mkrow(lang, langlist):
    acc = "<tr id=\"" + lang[0] + "\" class=\"" + lang[2] + "\">"
    if langlist:
        acc += "<td><button class=\"remove-button\">X</button></td>"
    acc += "<td class='level'>" + lang[2]
    return acc + "</td><td class=\"language\">" + lang[1] + "</td></tr>"

def addlangrow(level, langlist):
    acc = "<tr class=\"" + level + "\">"
    acc += "<td><button class='add-button'>+</button></td><td class='level'>"
    acc += level + "</td><td><select id=\"add" + level + "\">"
    for l in langlist:
        acc += "<option value=\"%s\">%s</option>" % (l[0], l[1])
    return acc + "</select></td></tr>"

def langpage(langs, user, langlist=None):
    # Expect "langs" to be a list of lists or tuples containing the
    # language code, language, and level
    title = ("Edit language list" if langlist else user + " speaks...")

    acc = "<h3>" + title + "</h3>"
    if langlist:
        acc += "<p>Logged in as " + user
        acc += ". <a href='/langlist?action=logout'>Logout</a></p>"

    acc += "<table>"
    blocks = []
    for level in ["C", "B", "A"]:
        row = "".join([mkrow(l, langlist) for l in langs if l[2] == level])
        blocks.append(row + (addlangrow(level, langlist) if langlist else ""))
    acc += "".join([b for b in blocks if len(b) > 0]) + "</table>"

    if langlist:
        # TODO localize text?
        acc += "<button id=\"save-button\">Save changes</button>"
        acc += "<script>var languages = {"
        acc += ",".join(['"%s":"%s"' % t for t in langlist]) + '''};</script>
       <script type="text/javascript" src="/langlist/js/scripts.js"></script>'''

    css = ["general.css"] + (["update.css"] if langlist else [])
    return generalpage(title, acc, ["/langlist/css/%s" % c for c in css])

def homepage():
    title = "Log in to edit language list"
    # TODO add new account dialog/boxes
    body = '''<form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <button type="submit">Send login link</button></form>'''
    return generalpage(title, body, ["/langlist/css/general.css"])

def linksentpage(username):
    return generalpage("Login link sent", '''<p>A login link has been sent
        to ''' + username + ".</p>", ["/langlist/css/general.css"])
