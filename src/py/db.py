#####
# Database Helper
#####

import MySQLdb

config_file = "/home/protected/db.conf"

def user_langs(user):
    sql = '''select languages.id, languages.name, whospeakswhat.level
             from languages join whospeakswhat 
                 on whospeakswhat.language = languages.id
             where (whospeakswhat.user = %s) order by languages.name'''
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute(sql, (user,))
    result =  cursor.fetchall()
    cnxn.close()
    return result

def all_langs():
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("select * from languages order by name")
    result = cursor.fetchall()
    cnxn.close()
    return result

def update_langs(user, languages):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("delete from whospeakswhat where user = %s", (user,))
    if len(languages) > 0:
        langs = [[user, l, languages[l]] for l in languages.keys()]
        sql = "insert into whospeakswhat values "
        sql += ",".join(["(%s,%s,%s)"]*len(langs))
        cursor.execute(sql, tuple(sum(langs, [])))
    cnxn.commit()
    cnxn.close()

def get_user_email(user):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("select email from users where id = %s", (user,))
    data = cursor.fetchone()
    cnxn.close()
    if data:
        return data[0]
    return None

def add_user(username, email, permission, newsletter, marketing):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("insert ignore into users values (%s, %s, %s, %s, %s)", 
                   (username, email, permission, newsletter, marketing))
    cnxn.commit()
    cnxn.close()

def delete_user(user):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("delete from whospeakswhat where user = %s", (user,))
    cursor.execute("delete from users where id = %s", (user,))
    cnxn.commit()
    cnxn.close()
