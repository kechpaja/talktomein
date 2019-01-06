###############
# Languages Page
###############

from .base import base

# TODO localization

rowfmt = '''
<tr id="{0}">
    <td class="language">{1}</td>
    <td>{2}</td>
    <td>{3}</td>
    <td>{4}</td>
    <td>{5}</td>
    <td>{6}</td>
</tr>
'''

removebtn = '<button class="remove-button">X</button>'

def expand_level(level):
    # TODO allow update
    return "&#x258b;" * level

def one_row(lang, edit=False):
    return rowfmt.format(lang[0], 
                         lang[1],
                         expand_level(lang[2]),
                         expand_level(lang[3]),
                         expand_level(lang[4]),
                         expand_level(lang[5]),
                         removebtn if edit else "")


optfmt = '<option value=\"%s\">%s</option>'
levelselectfmt = '''
<select id="%s">
    <option value="0">-</option>
    <option value="5">&#x258b;&#x258b;&#x258b;&#x258b;&#x258b;</option>
    <option value="4">&#x258b;&#x258b;&#x258b;&#x258b;</option>
    <option value="3">&#x258b;&#x258b;&#x258b;</option>
    <option value="2">&#x258b;&#x258b;</option>
    <option value="1">&#x258b;</option>
</select>
'''
addfmt = '''
<tr class="add-row">
    <td><select id="lang-selector"><option value="">-</option>%s</select></td>
    <td>{0}</td>
    <td>{1}</td>
    <td>{2}</td>
    <td>{3}</td>
    <td><button class="add-button">+</button></td>
</tr>
'''.format(levelselectfmt % "speaking",
           levelselectfmt % "listening",
           levelselectfmt % "reading",
           levelselectfmt % "writing")

def table_innards(langs, all_langs=None):
    innards = "".join([one_row(l, all_langs) for l in langs])
    if all_langs:
        user_lang_codes = next(zip(*langs))
        optlangs = [l for l in all_langs if l[0] not in user_lang_codes]
        innards += addfmt % "".join(optfmt % l for l in optlangs)
    return innards


framefmt = '<h3>%s</h3><table>%s</table>%s'
displaytitlefmt = '%s speaks...'
newacctlink = '<a href="/account/create">Create your own language list</a>'

def display(langs, user):
    title = displaytitlefmt % user
    body = framefmt % (title, table_innards(langs), newacctlink)
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
