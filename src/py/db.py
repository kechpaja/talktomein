#####
# Database Helper
#####

import MySQLdb
import time

config_file = "/home/gunicorn/.my.cnf"

def user_langs(user):
    sql = '''select languages.id, languages.name, whospeakswhat.speaking,
                    whospeakswhat.listening, whospeakswhat.reading,
                    whospeakswhat.writing
             from languages join whospeakswhat 
                 on whospeakswhat.language = languages.id
             where (whospeakswhat.user = %s)
             order by whospeakswhat.speaking desc, whospeakswhat.listening desc,
                      whospeakswhat.reading desc, whospeakswhat.writing desc,
                      languages.name'''
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute(sql, (user,))
    result =  cursor.fetchall()
    cnxn.close()
    return result

## TODO above this line not done

def all_langs():
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("select * from languages order by name")
    result = cursor.fetchall()
    cnxn.close()
    return result

def update_lang(user, language, speaking=0, listening=0, reading=0, writing=0):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    delete_sql = "delete from whospeakswhat where user = %s and language = %s"
    cursor.execute(delete_sql, (user, language))
    if speaking or listening or reading or writing:
        cursor.execute("insert into whospeakswhat values (%s,%s,%s,%s,%s,%s)",
                       (user, language, speaking, listening, reading, writing))
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

# TODO for GDPR compliance, add date, version of site, and loc lang to each 
# TODO insert and update to users table. Perhaps merge marketing and newsletter
# TODO items into a single option?
def get_user_prefs(user):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("select marketing from users where id = %s",
                   (user,))
    result = cursor.fetchone()
    cnxn.close()
    return result

def add_user(username, email, marketing, timestamp, version, loclang):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("insert ignore into users values (%s, %s, %s, %s, %s, %s)", 
                   (username, email, marketing, timestamp, version, loclang))
    cnxn.commit()
    cnxn.close()

def delete_user(user):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    cursor.execute("delete from whospeakswhat where user = %s", (user,))
    cursor.execute("delete from users where id = %s", (user,))
    cnxn.commit()
    cnxn.close()

# TODO consider getting rid of this and just adding another row
def update_user(user, column, value):
    cnxn = MySQLdb.connect(read_default_file=config_file)
    cursor = cnxn.cursor()
    if column in ["marketing"]:
        cursor.execute("update users set " + column + " = %s where id = %s",
                       (value, user))
        cursor.execute("update users set timestamp = %s where id = %s",
                       (str(time.time()), user))
        cnxn.commit()
    cnxn.close()
