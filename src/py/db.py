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

    def add_token(self, table, user):
        # Token is auto-generated here
        cursor = self.cnxn.cursor()
        token = str(uuid.uuid4())
        cursor.execute("insert into %s values (%s, %s)", (table, token, user))
        self.cnxn.commit()
        return token

    def delete_token(self, table, token):
        cursor = self.cnxn.cursor()
        cursor.execute("delete from %s where id = %s", (table, token))
        self.cnxn.commit()

    def get_token_user(self, table, token):
        cursor = self.cnxn.cursor()
        cursor.execute("select * from %s where id = %s", (table, token))
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

    def get_user_email(self, user):
        cursor = self.cnxn.cursor()
        cursor.execute("select email from users where id = %s", (user,))
        data = cursor.fetchone()
        if data:
            return data[0]
        return None
