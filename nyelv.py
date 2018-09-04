import falcon
import json
import MySQLdb

def gencookie(user):
    # TODO generate and store actual token
    return json.dumps({"user" : user, "token" : "token"})

def chklogin(cookies):
    if "nyelv-session" not in cookies:
        return None

    cookiedict = json.loads(cookies["nyelv-session"])
    # TODO retrieve and verify actual token; check age
    if cookiedict["token"] == "token":
        return cookiedict["user"]
    else:
        return None

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
    acc = "<html><head><title>" + title + '''</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="/nyelv/css/styles.css">
        </head><body><table>'''

    # TODO make more Pythonic?
    blocks = []
    for level in ["N", "C", "B", "A"]:
        blocks.append("\n".join([mkrow(l) for l in query if l[2] == level]))
    blocks = [blocks[0] + blocks[1], blocks[2], blocks[3]]
    blocks = [b for b in blocks if len(b) > 0]
    acc += "\n<tr class=\"border\"><td colspan=\"3\"></td></tr>\n".join(blocks)

    acc += '''</table><p id="key"> Key: <span class="C">fluent</span>, 
        <span class="B">intermediate</span>,<span class="A">beginner</span>.
        Native languages are starred 
        (<span class="left-column">&bigstar;</span>).</p>'''
    if scripts:
        acc += "<script>var languages = {"
        acc += ",".join(['"%s":"%s"' % t for t in fetchlangs(cnxn)])
        acc += "};var user = \"" + user + '''";</script>
        <script type="text/javascript" src="/nyelv/js/scripts.js"></script>'''

    return acc + "</body></html>"

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

class LoginResource(object):
    def on_get(self, req, resp, user, code):
        # TODO verify code against something in database
        if code == "passw0rd":
            # TODO set additional cookie fields
            resp.set_cookie("nyelv-session",
                            gencookie(user),
                            domain="kechpaja.com",
                            path="/nyelv/",
                            max_age=3600, # TODO update as necessary
                            http_only=False)
            resp.body = genpage(user, dbconnect(), "Edit language list", True)
            resp.content_type = "text/html; charset=utf-8"
            resp.status = falcon.HTTP_200
        else:
            # TODO set body to some sort of "login failed" page
            # This will do for now:
            # But eventually we should tell the user if code has already been
            # used, since the codes I eventually intend to send out will be
            # single-use (and will eventually expire). 
            resp.body = '''<html><head><title>Login failed</title></head>
                <body><h1>Login failed</h1></body></html>'''
            resp.status = falcon.HTTP_200 # TODO ??? 401?

class LoginPageResource(object):
    def on_get(self, req, resp):
        pass # TODO display login page

class BadTokenPageResource(object):
    def on_get(self, req, resp):
        pass # TODO display bad token page

class UpdateListResource(object):
    def on_post(self, req, resp):
        user = chklogin(req.cookies)
        if not user:
            # TODO redirect to some failure page?
            resp.status = falcon.HTTP_401
            return

        data = json.loads(req.stream.read().decode("utf-8"))
        languages = [[user, lang, data[lang]] for lang in data.keys()]

        cnxn = dbconnect()
        cursor = cnxn.cursor()

        cursor.execute("delete from whospeakswhat where user = %s", (user,))
        if len(languages) > 0:
            sql = "insert into whospeakswhat values "
            sql += ",".join(["(%s,%s,%s)"]*len(languages))
            cursor.execute(sql, tuple(sum(languages, [])))

        cnxn.commit()
        cnxn.close()

        # TODO response body? 
        resp.status = falcon.HTTP_200

# TODO think about how to work authentication into update mechanism
# Probably just going to send the user a token, which will be verified when
# the GET request for the update page is processed. A session cookie will then
# be added? 

# Start Falcon
app = falcon.API()
app.add_route("/ei/{user}", LanguageListResource())
app.add_route("/login/{user}/{code}", LoginResource())
app.add_route("/update", UpdateListResource())
