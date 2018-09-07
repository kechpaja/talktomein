#####
# Database Helper
#####

import MySQLdb
import uuid

class DatabaseWrapper(object):
    def __init__(self, config_file):
        self.cnxn = MySQLdb.connect(host="nyelv.db",
                                    db="nyelv",
                                    user="nyelv",
                                    read_default_file=config_file,
                                    charset="utf8")

    def disconnect(self):
        self.cnxn.close()

    def add_token(self,  user):
        # Token is auto-generated here
        cursor = self.cnxn.cursor()
        token = str(uuid.uuid4())
        cursor.execute("insert into tokens values (%s, %s)", (token, user))
        self.cnxn.commit()
        return token

    def delete_token(self, token):
        cursor = self.cnxn.cursor()
        cursor.execute("delete from tokens where id = %s", (token,))
        self.cnxn.commit()

    def get_token_user(self, token):
        cursor = self.cnxn.cursor()
        cursor.execute("select * from tokens where id = %s", (token,))
        session = cursor.fetchone()
        # TODO make sure token isn't too old
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
            langs = [[user, l, languages[l]] for l in languages.keys()]
            sql = "insert into whospeakswhat values "
            sql += ",".join(["(%s,%s,%s)"]*len(langs))
            cursor.execute(sql, tuple(sum(langs, [])))
        self.cnxn.commit()
