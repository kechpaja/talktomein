import falcon
import MySQLdb

def mkrow(lang):
    acc = "<tr class=\"" + lang[2] + "\"><td class=\"left-column\">"
    acc += "&bigstar;" if lang[2] == "N" else ""
    acc += "</td><td class=\"language\">" + lang[1] + "</td></tr>"
    return acc

def genpage(user, query):
    # Expect query to be a list of lists or tuples containing the
    # language code, language, and level
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
        blocks.append("\n".join([mkrow(l) for l in query if l[2] == level]))
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
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        
        # TODO do all of this elsewhere
        #self.connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        #self.connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

        #self.cursor = self.connection.cursor()
        #self.cursor.execute("use nyelv;") # TODO variable?

    def on_get(self, req, resp, user):
        sql = '''select
                    languages.id,
                    languages.name,
                    whospeakswhat.level
                from languages join whospeakswhat 
                    on whospeakswhat.language = languages.id
                where (whospeakswhat.user = ?)'''
        self.cursor.execute(sql, user)
        resp.body = genpage(self.cursor.fetchall()) # TODO a tad dangerous?

        resp.content_type = "text/html; charset=utf-8"
        resp.status = falcon.HTTP_200


####
# Start everything up
####

# Set up database connection
db = MySQLdb.connect(host="nyelv.db",
                     db="nyelv",
                     read_default_file="~/.nyelv-db.conf",
                     charset="utf8")

# Start Falcon
app = falcon.API()
app.add_route("/ei/{user}", LanguageListResource(db))
