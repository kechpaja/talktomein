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

remove_button = '<td><button class="remove-button">X</button></td>'

def one_row(lang, has_remove_button=False):
    return rowfmt.format(lang[0], # Code
                         lang[1], # Name
                         lang[2], # Level
                         remove_button if has_remove_button else "")


selectorfmt = '''
<select id="add%s">
    <option value="">-</option>
    %s
</select>
'''

optionfmt = '<option value=\"%s\">%s</option>'
add_button = "<td><button class='add-button'>+</button></td>"

def add_row(level, all_langs):
    selector = selectorfmt % (level, "".join(optionfmt % l for l in all_langs))
    return rowfmt.format("add-%s-tr" % level, selector, level, add_button)


def table_innards(langs, all_langs=None):
    blocks = []
    for level in ["C", "B", "A"]:
        row = "".join([one_row(l, all_langs) for l in langs if l[2] == level])
        blocks.append(row + (add_row(level, all_langs) if all_langs else ""))
    return "".join([b for b in blocks if len(b) > 0]) 


framefmt = '<h3>%s</h3><table>%s</table>%s'
displaytitlefmt = '%s speaks...'

def display(langs, user):
    title = displaytitlefmt % user
    body = framefmt % (title, table_innards(langs), "")
    return base(title, body, ["general"])


bottomfmt = '''
<button id="save-button" disabled>Save Changes</button>
<p>Logged in as %s.</p>
<div><a href="/account">Account Details</a><a href="/logout">Logout</a></div>
<script>
    var languages = {%s};
</script>
'''

def update(langs, user, all_langs):
    title = "Edit language list" # TODO localize
    body = framefmt % (title,
                       table_innards(langs, all_langs),
                       bottomfmt % (user,
                                    ",".join('"%s":"%s"'%l for l in all_langs)))
    return base(title, body, ["general", "update"], ["scripts"])
