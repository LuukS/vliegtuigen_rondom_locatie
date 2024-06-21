from connection import Config
if Config.database.lower() != 'mysql':
    exit("Configuratie is niet voor MySQL gemaakt.")

from connection import Connection

print ("start")
testen = Connection()
print(f"Database connectie geslaagd: {testen.isConnected()}")
if testen.isConnected():
    cur = testen.db.cursor()
    cur.execute("SELECT * FROM foo")
    myresult = cur.fetchall()
    for x in myresult:
      print(x)
    cur.execute("insert foo VALUES ()")
    cur.execute("COMMIT")
    cur.execute("SELECT * FROM foo")
    myresult = cur.fetchall()
    for x in myresult:
      print(x)

else:
    print("Omdat de connectie niet geslaagd was kan er geen testquery uitgevoerd worden")


print("stop")