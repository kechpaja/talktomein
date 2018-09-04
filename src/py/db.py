#####
# Database Helper
#####

import MySQLdb


class DatabaseWrapper(object):
    def __init__(self, config_file):
        self.cnxn = MySQLdb.connect(host="nyelv.db",
                                    db="nyelv",
                                    user="nyelv",
                                    read_default_file=config_file,
                                    charset="utf8")

    def disconnect(self):
        self.cnxn.close()

    def add_session(self,  user):
        # Session ID is auto-generated here
        cursor = self.cnxn.cursor()
        session_id = "" # TODO generate
        cursor.execute("insert into sessions values (%s, %s)",(session_id,user))
        self.cnxn.commit()

    def delete_session(self, session_id):
        cursor = self.cnxn.cursor()
        cursor.execute("delete from sessions where id = %s", (session_id,))
        self.cnxn.commit()

    def session_user(self, session_id):
        cursor = self.cnxn.cursor()
        cursor.execute("select * from sessions where id = %s", (session_id,))
        session = cursor.fetchone()
        # TODO make sure session isn't too old
        if session:
            return session[1]
        return None

    def user_langs(self, user):
        sql = '''select languages.id, languages.name, whospeakswhat.level
                 from languages join whospeakswhat 
                     on whospeakswhat.language = languages.id
                 where (whospeakswhat.user = %s)'''
        cursor = self.cnxn.cursor()
        cursor.execute(sql, (user,))
        return cursor.fetchall()

    def all_langs(self):
        cursor = self.cnxn.cursor()
        cursor.execute("select * from languages")
        return cursor.fetchall()

    def update_langs(self, user, languages):
        cursor = self.cnxn.cursor()
        cursor.execute("delete from whospeakswhat where user = %s", (user,))
        if len(languages) > 0:
            sql = "insert into whospeakswhat values "
            sql += ",".join(["(%s,%s,%s)"]*len(languages))
            cursor.execute(sql, tuple(sum(languages, [])))
        self.cnxn.commit()



# TODO old (still in code in places)
class DatabaseMiddleware(object):
    def __init__(self, config_file):
        self.cnxn = MySQLdb.connect(host="nyelv.db",
                                    db="nyelv",
                                    user="nyelv",
                                    read_default_file=config_file,
                                    charset="utf8")

    def process_request(self, req, resp):
        req.context["db"] = self.cnxn

    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            req.context["db"].commit()
        req.context["db"].close()
