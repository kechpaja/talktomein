###############
# Languages Page
###############

from .base import base

# TODO localization


rowfmt = '''
<tr id="{0}" class="{2}">
    <td class="level">{2}</td>
    <td class="language">{1}</td>
    {3}
</tr>
'''

remove_button = '''<td><button class="remove-button">X</button></td>'''

def one_row(lang, has_remove_button=False):
    return rowfmt.format(lang[0], # Code
                         lang[1], # Name
                         lang[2], # Level
                         remove_button if has_remove_button else "")

# TODO split this up into something more reasonable
def addlangrow(level, langlist):
    acc = "<tr class=\"" + level + "\">"
    acc += "<td class='level'>"+level+"</td><td><select id=\"add"+level+"\">"
    acc += "<option value=\"\"></option>"
    for l in langlist:
        acc += "<option value=\"%s\">%s</option>" % (l[0], l[1])
    acc += "</select></td>"
    return acc + "<td><button class='add-button'>+</button></td></tr>"


def table_innards(langs, all_langs=None):
    blocks = []
    for level in ["C", "B", "A"]:
        row = "".join([one_row(l, all_langs) for l in langs if l[2] == level])
        blocks.append(row + (addlangrow(level, langlist) if langlist else ""))
    return "".join([b for b in blocks if len(b) > 0]) 



framefmt = '''<h3>%s</h3>%s<table>%s</table>%s'''
displaytitlefmt = '''%s speaks...'''

def display(langs, user):
    title = displaytitlefmt % user
    body = framefmt % (title, "", table_innards(langs), "")
    return base(title, body, ["general"])


loggedinfmt = '''<p>Logged in as %s. <a href="/?action=logout">Logout</a></p>'''
bottomfmt = '''
<button id="save-button" disabled>Save Changes</button>
<a id="deleteacct" href="/account/delete">Delete Account</a>
<script>
    var languages = {%s};
</script>
'''

def update(langs, user, all_langs):
    title = "Edit language list" # TODO localize
    body = framefmt % (title,
                       loggedinfmt % user,
                       table_innards(langs, all_langs),
                       bottomfmt % ",".join('"%s":"%s"' % l for l in all_langs))
    return base(title, body, ["general", "update"], ["scripts"])
