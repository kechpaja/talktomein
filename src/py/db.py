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

def update_lang(user, language, level):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    delete_sql = "delete from whospeakswhat where user = %s and language = %s"
    cursor.execute(delete_sql, (user, language))
    if level:
        cursor.execute("insert into whospeakswhat values (%s, %s, %s)",
                       (user, language, level))
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

def get_user_prefs(user):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("select newsletter, marketing from users where id = %s",
                   (user,))
    result = cursor.fetchone()
    cnxn.close()
    return result

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

def update_user(user, column, value):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    if column in ["newsletter", "marketing"]:
        cursor.execute("update users set " + column + " = %s where id = %s",
                       (value, user))
        cnxn.commit()
    cnxn.close()
