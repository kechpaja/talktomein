import falcon
import MySQLdb

def fetchlangs(user, cnxn):
    sql = '''select
                languages.id,
                languages.name,
                whospeakswhat.level
            from languages join whospeakswhat 
                on whospeakswhat.language = languages.id
            where (whospeakswhat.user = %s)'''

    cursor = cnxn.cursor()
    cursor.execute(sql, (user,))
    return cursor.fetchall()

def mkrow(lang):
    acc = "<tr class=\"" + lang[2] + "\"><td class=\"left-column\">"
    acc += "&bigstar;" if lang[2] == "N" else ""
    acc += "</td><td class=\"language\">" + lang[1] + "</td></tr>"
    return acc

def genpage(user, cnxn):
    query = fetchlangs(user, cnxn)

    # Expect query to be a list of lists or tuples containing the
    # language code, language, and level
    acc = "<html>\n    <head>\n        <title>" + user + " speaks:</title>"
    acc += '''
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="../css/styles.css">
    </head>

    <body>
        <table>
'''

    # TODO make more Pythonic?
    blocks = []
    for level in ["N", "C", "B", "A"]:
        blocks.append("\n".join([mkrow(l) for l in query if l[2] == level]))
    blocks = [blocks[0] + blocks[1], blocks[2], blocks[3]]
    blocks = [b for b in blocks if len(b) > 0]
    acc += "\n\n<tr class=\"border\"><td></td><td></td></tr>\n\n".join(blocks)

    acc += '''
        </table>

        <p>
        Key: <span class="C">fluent</span>, <span class="B">intermediate</span>,
        <span class="A">beginner</span>. Native languages are starred 
        (<span class="left-column">&bigstar;</span>).
        </p>

    </body>
</html>
'''
    return acc

def dbconnect():
    return MySQLdb.connect(host="nyelv.db",
                           db="nyelv",
                           user="nyelv",
                           read_default_file="/home/protected/.nyelv-db.conf",
                           charset="utf8")

class LanguageListResource(object):
    def on_get(self, req, resp, user):
        resp.body = genpage(user, dbconnect())
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


# Start Falcon
app = falcon.API()
app.add_route("/ei/{user}", LanguageListResource())
