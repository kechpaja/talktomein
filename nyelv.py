import falcon
import json
import MySQLdb

# Database helper functions
def fetchuserlangs(user, cnxn):
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

def fetchlangs(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("select * from languages")
    return cursor.fetchall()

# Page generation helper functions
def mkrow(lang):
    acc = "<tr id=\"" + lang[0] + "\" class=\"" + lang[2] + "\">"
    acc += "<td class=\"left-column\">"+("&bigstar;" if lang[2] == "N" else "")
    acc += "</td><td class=\"language\">" + lang[1] + "</td></tr>"
    return acc

def genpage(user, cnxn, title, scripts=False):
    query = fetchuserlangs(user, cnxn)

    # Expect query to be a list of lists or tuples containing the
    # language code, language, and level
    acc = "<html>\n    <head>\n        <title>" + title + "</title>"
    acc += '''
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="../css/styles.css">
'''

    acc += '''
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

        <p id="key">
        Key: <span class="C">fluent</span>, <span class="B">intermediate</span>,
        <span class="A">beginner</span>. Native languages are starred 
        (<span class="left-column">&bigstar;</span>).
        </p>
'''
    if scripts:
        langs = fetchlangs(cnxn)
        acc += "        <script>\n            var languages = {"
        acc += ",".join(['"' + l[0] + '":"' + l[1] + '"' for l in langs])
        acc += "};\n        var user = \"" + user + "\";\n        </script>\n"
        acc += '''
        <script type="text/javascript" src="../js/scripts.js"></script>
'''

    acc += '''
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
        resp.body = genpage(user, dbconnect(), user + " speaks:")
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

class UpdateListResource(object):
    def on_get(self, req, resp, user):
        resp.body = genpage(user, dbconnect(), "Edit language list", True)
        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, user):
        data = json.loads(req.stream.read().decode("utf-8"))
        #languages = [[]]
        #for language in data.keys():
        #    languages.append([user, language, data[language]])

        #cnxn = dbconnect()
        #cursor = cnxn.cursor()

        #cursor.execute("delete from whospeakswhat where user = %s", (user,))
        #if len(languages) > 0:
        #    sql = "insert into whospeakswhat values "
        #    sql += ",".join(["(%s,%s,%s)"]*len(languages))
        #    cursor.execute(sql, tuple(sum(languages, [])))

        #cnxn.commit()

        # TODO response body? 
        resp.status = falcon.HTTP_200

# TODO think about how to work authentication into update mechanism
# Probably just going to send the user a token, which will be verified when
# the GET request for the update page is processed. A session cookie will then
# be added? 
# Or maybe just require the token sent to user when save is posted. Can access
# update page for any user, but can't save without auth? 

# Start Falcon
app = falcon.API()
app.add_route("/ei/{user}", LanguageListResource())
app.add_route("/update/{user}", UpdateListResource())
