import falcon

# TODO Update CSS to match what we have here

def filterquery(query, level):
    return [[x[1], x[2], x[3]] for x in query if x[3] == level]

def mkrow(lang):
    acc = "<tr class=\"" + lang[2] + "\"><td class=\"left-column\">"
    if lang[2] == "N":
        # TODO update condition?
        acc += "&bigstar;"
    acc += "</td><td class=\"language\">" + lang[1] + "</td></tr>"
    return acc

def genpage(user, query):
    # Expect query to be a list of lists or tuples containing the
    # username, language code, language, and level
    acc = "<html>\n    <head>\n        <title>" + user + " speaks:</title>"
    acc += '''
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <lnk rel="stylesheet" type="text/css" href="../styles.css">
    </head>

    <body>
        <table>
'''

    # TODO make more Pythonic?
    blocks = []
    for level in ["N", "C", "B", "A"]:
        blocks.append("\n".join([mkrow(l) for l in filterquery(query, level)]))
    acc += "\n\n<tr class=\"border\"></td></td><td></td></tr>\n\n".join(blocks)

    acc += '''
        </table>

        <p>Key: <span class="fluent">fluent</span>, 
        <span class="intermediate">intermediate</span>, 
        <span class="beginner">beginner</span>. Native
        languages are starred (<span class="native">&bigstar;</span>).</p>

    </body>
</html>
'''
    return acc


class LanguageListResource(object):
    def on_get(self, req, resp):
        # TODO connect to database
        # TODO get languages associated with user
        # TODO generate display page
        # TODO return
        pass # TODO


####
# Start everything up
####

app = falcon.API()

app.add_route("/ei/{user}", LanguageListResource())
