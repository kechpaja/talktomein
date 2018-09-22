#######
# Pages
######

# XXX langlist = list of all possible languages

def generalpage(title, insides, css):
    acc = "<html><head><title>" + title + '''</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">'''
    for f in css:
        acc += "<link rel='stylesheet' type='text/css' href='/css/%s'>" % f
    return acc + "</head><body>" + insides + "</body></html>"

def mkrow(l, langlist):
    acc = "<tr id=\"" + l[0] + "\" class=\"" + l[2] + "\"><td class='level'>" 
    acc += l[2] + "</td><td class=\"language\">" + l[1] + "</td>"
    if langlist:
        acc += "<td><button class=\"remove-button\">X</button></td>"
    return acc + "</tr>"

def addlangrow(level, langlist):
    acc = "<tr class=\"" + level + "\">"
    acc += "<td class='level'>"+level+"</td><td><select id=\"add"+level+"\">"
    acc += "<option value=\"\"></option>"
    for l in langlist:
        acc += "<option value=\"%s\">%s</option>" % (l[0], l[1])
    acc += "</select></td>"
    return acc + "<td><button class='add-button'>+</button></td></tr>"

def langpage(langs, user, langlist=None):
    # Expect "langs" to be a list of lists or tuples containing the
    # language code, language, and level
    title = ("Edit language list" if langlist else user + " speaks...")

    acc = "<h3>" + title + "</h3>"
    if langlist:
        acc += "<p>Logged in as " + user
        acc += ". <a href='/?action=logout'>Logout</a></p>"

    acc += "<table>"
    blocks = []
    for level in ["C", "B", "A"]:
        row = "".join([mkrow(l, langlist) for l in langs if l[2] == level])
        blocks.append(row + (addlangrow(level, langlist) if langlist else ""))
    acc += "".join([b for b in blocks if len(b) > 0]) + "</table>"

    if langlist:
        acc += "<button id=\"save-button\" disabled>Save changes</button>"
        acc += "<a id=\"deleteacct\" href=\"/account/delete\">"
        acc += "Delete Account</a><script>var languages = {"
        acc += ",".join(['"%s":"%s"' % t for t in langlist]) + '''};</script>
       <script type="text/javascript" src="/js/scripts.js"></script>'''

    css = ["general.css"] + (["update.css"] if langlist else [])
    return generalpage(title, acc, css)
