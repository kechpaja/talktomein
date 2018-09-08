#######
# Pages
######

# XXX langlist = list of all possible languages

def generalpage(title, insides):
    return "<html><head><title>" + title + '''</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="/langlist/css/styles.css">
        </head><body>''' + insides + "</body></html>"

def mkrow(lang, langlist):
    acc = "<tr id=\"" + lang[0] + "\" class=\"" + lang[2] + "\">"
    if langlist:
        acc += "<td><button class=\"remove-button\">-</button></td>"
    acc += "<td>" + lang[2]
    return acc + "</td><td class=\"language\">" + lang[1] + "</td></tr>"

def addlangrow(level, langlist):
    acc = "<tr class=\"" + level + "\"><td>"
    acc += "<button class='add-button'>+</button></td><td>" + level
    acc += "</td><td><select id=\"add" + level + "\">"
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

    # TODO make more Pythonic?
    blocks = []
    for level in ["N", "C", "B", "A"]:
        row = "".join([mkrow(l, langlist) for l in langs if l[2] == level])
        blocks.append(row + (addlangrow(level, langlist) if langlist else ""))
    blocks = [blocks[0] + blocks[1], blocks[2], blocks[3]]
    blocks = [b for b in blocks if len(b) > 0]
    acc += "\n<tr class=\"border\"><td colspan=\"3\"></td></tr>\n".join(blocks)

    acc += '''</table><p id="key"> Key: <span class="C">fluent</span>, 
              <span class="B">intermediate</span>,
              <span class="A">beginner</span>.</p>'''
    if langlist:
        # TODO localize text?
        acc += "<button id=\"save-button\">Save changes</button>"
        acc += "<script>var languages = {"
        acc += ",".join(['"%s":"%s"' % t for t in langlist]) + '''};</script>
       <script type="text/javascript" src="/langlist/js/scripts.js"></script>'''

    return generalpage(title, acc)

def homepage():
    # TODO add new account dialog/boxes
    return generalpage("Log in to edit language list", '''<form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <button type="submit">Send login link</button></form>''')

def linksentpage(username):
    return generalpage("Login link sent", '''<p>A login link has been sent
        to ''' + username + ".</p>")
