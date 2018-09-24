###############
# Languages Page
###############

from .base import base

# TODO localization

rowfmt = '''
<tr{0} class="{2}">
    <td class="level">{2}</td>
    {1}
    {3}
</tr>
'''

remove_button = '''
<td></td>
<td></td>
<td><button class="remove-button">X</button></td>
'''

def one_row(lang, has_remove_button=False):
    return rowfmt.format(' id="%s"' % lang[0], # Code
                         '<td class="language">%s</td>' % lang[1], # Name
                         lang[2], # Level
                         remove_button if has_remove_button 
                                       else "<td></td><td></td><td></td>")


optfmt = '<option value=\"%s\">%s</option>'
addfmt = '''
<tr class="add-row">
    <td class="level">?</td>
    <td><select id="add"><option value="">-</option>%s</select></td>
    <td><button class="add-button">A</button></td>
    <td><button class="add-button">B</button></td>
    <td><button class="add-button">C</button></td>
</tr>
'''

def table_innards(langs, all_langs=None):
    blocks = []
    for level in ["C", "B", "A"]:
        row = "".join([one_row(l, all_langs) for l in langs if l[2] == level])
        blocks.append(row)
    addrow = addfmt % "".join(optfmt%l for l in all_langs) if all_langs else ""
    return "".join([b for b in blocks if b]) + addrow


framefmt = '<h3>%s</h3><table>%s</table>%s'
displaytitlefmt = '%s speaks...'

def display(langs, user):
    title = displaytitlefmt % user
    body = framefmt % (title, table_innards(langs), "")
    return base(title, body, ["general"])


bottomfmt = '''
<p>Logged in as %s.</p>
<div><a href="/account">Account Details</a><a href="/logout">Logout</a></div>
'''

def update(langs, user, all_langs):
    title = "Edit language list" # TODO localize
    body = framefmt % (title,
                       table_innards(langs, all_langs),
                       bottomfmt % user)
    return base(title, body, ["general", "update"], ["scripts"])
