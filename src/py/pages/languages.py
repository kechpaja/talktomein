###############
# Languages Page
###############

from .base import base

# TODO localization

rowfmt = '''
<tr id="{0}">
    <td class="language">{1}</td>
    <td class="level l{2}">{3}</td>
    <td class="level l{4}">{5}</td>
    <td class="level l{6}">{7}</td>
    <td class="level l{8}">{9}</td>
    <td>{10}</td>
</tr>
'''

removebtn = '<button class="remove-button">X</button>'

def expand_level(level):
    return "|" * level if level else "-"

def one_row(lang, edit=False):
    if edit:
        pass # TODO return something completely different

    return rowfmt.format(lang[0], 
                         lang[1],
                         lang[2], expand_level(lang[2]),
                         lang[3], expand_level(lang[3]),
                         lang[4], expand_level(lang[4]),
                         lang[5], expand_level(lang[5]),
                         removebtn if edit else "")


optfmt = '<option value=\"%s\">%s</option>'
levelselectfmt = '''
<select id="%s">
    <option value="0">-</option>
    <option value="5">|||||</option>
    <option value="4">||||</option>
    <option value="3">|||</option>
    <option value="2">||</option>
    <option value="1">|</option>
</select>
'''
addfmt = '''
<tr id="add-row">
    <td><select id="lang-selector"><option value="">-</option>%s</select></td>
    <td>{0}</td>
    <td>{1}</td>
    <td>{2}</td>
    <td>{3}</td>
    <td><button id="add-button">+</button></td>
</tr>
'''.format(levelselectfmt % "speaking-selector",
           levelselectfmt % "listening-selector",
           levelselectfmt % "reading-selector",
           levelselectfmt % "writing-selector")

def table_innards(langs, all_langs=None):
    innards = "".join([one_row(l, all_langs) for l in langs])
    if all_langs:
        user_lang_codes = next(zip(*langs)) if langs else []
        optlangs = [l for l in all_langs if l[0] not in user_lang_codes]
        innards += addfmt % "".join(optfmt % l for l in optlangs)
    return innards


framefmt = '''
<table>
    <tr class="table-header">
        <td></td>
        <td>&#128068;</td>
        <td>&#128066;</td>
        <td>&#128214;</td>
        <td>&#9999;</td>
    </tr>
    %s
</table>
%s
'''
displaytitlefmt = '%s\'s languages'
newacctlink = '<a href="/account/create">Create your own language list</a>'

def display(langs, user):
    body = framefmt % (table_innards(langs), newacctlink)
    return base(displaytitlefmt % user, body, ["general"])


bottomfmt = '''
<p>Logged in as %s.</p>
<div><a href="/account">Account Details</a><a href="/logout">Logout</a></div>
'''

def update(langs, user, all_langs):
    body = framefmt % (table_innards(langs, all_langs),
                       bottomfmt % user)
    # TODO localize?
    return base("Edit language list", body, ["general", "update"], ["scripts"])
