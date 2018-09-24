###############
# Languages Page
###############

from .base import base

# TODO localization

rowfmt = '''
<tr id="{0}" class="{2}">
    <td class="level">{2}</td>
    <td class="language">{1}</td>
    <td></td>
    <td></td>
    <td>{3}</td>
</tr>
'''

removebtn = '<button class="remove-button">X</button>'

def one_row(lang, edit=False):
    return rowfmt.format(lang[0], lang[1], lang[2], removebtn if edit else "")


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
    innards = "".join([b for b in blocks if b])
    if all_langs:
        user_lang_codes = next(zip(*langs))
        optlangs = [l for l in all_langs if l[0] not in user_lang_codes]
        innards += addfmt % "".join(optfmt % l for l in optlangs)
    return innards


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
