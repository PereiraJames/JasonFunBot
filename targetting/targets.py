import mysql.connector
import jasontools

db_config = jasontools.parseEnvFile("DB_CONFIG")

def insertUser(username,userid,whitelisted="None",blacklisted="None",realname="Null"):
    
    query = """
        INSERT INTO telegramUsers (username, userid, whitelisted, blacklisted, realname)
        VALUES (%s,%s,%s,%s,%s)
    """

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    cursor.execute(query, (
        username, userid, whitelisted, blacklisted, realname
    ))
    
    print(f"Imported {username} | {realname} | {userid}")

    db.commit()

def findUser(username):
    
    query = """
        SELECT *
        FROM telegramUsers
        WHERE username = (%s)
    """

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    cursor.execute(query, (username,))

    response = cursor.fetchall()

    collectedata = []

    for row in response:
        rowData = {
            "username" : row[0],
            "userid" : row[1],
            "whitelistsed" : row[2],
            "blacklisted" : row[3],
            "realanem" : row[4]
        }

        collectedata.append(rowData)

    cursor.close()
    db.close()

    if collectedata:
        return True
    else:
        return False


def updateUser(username,userid,realname):

    if findUser(username):
        print("Already in database")
        return False
    else:
        insertUser(username,userid,realname=realname)
        return True
    

# findUser('Markryannasdas')

# updateUser("Markryann", "39705690", "mark")
# updateUser("Markryanna", "1230912390", "gaymark")

# insertUser(username="Markryann", userid="39705690",realname="mark")
