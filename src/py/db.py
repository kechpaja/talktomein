#####
# Database Helper
#####

import MySQLdb
import uuid

class DatabaseWrapper(object):
    def __init__(self, config_file):
        self.cnxn = MySQLdb.connect(read_default_file=config_file)

    def disconnect(self):
        self.cnxn.close()

    # XXX Table argument to this and the next three functions *must not* contain
    # user data, as it is inserted into the DB query string unsanitized.
    def add_token(self, table, user):
        # Token is auto-generated here
        cursor = self.cnxn.cursor()
        token = str(uuid.uuid4())
        cursor.execute("insert into " + table + "_tokens values (%s, %s)",
                       (token, user))
        self.cnxn.commit()
        return token

    def delete_token(self, table, token):
        cursor = self.cnxn.cursor()
        cursor.execute("delete from " + table + "_tokens where id = %s", 
                       (token,))
        self.cnxn.commit()

    def get_token_user(self, table, token):
        cursor = self.cnxn.cursor()
        cursor.execute("select * from " + table + "_tokens where id = %s", 
                       (token,))
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

    def add_user(self, user, email):
        cursor = self.cnxn.cursor()
        cursor.execute("insert into users values (%s, %s)", (user, email))
        self.cnxn.commit()
