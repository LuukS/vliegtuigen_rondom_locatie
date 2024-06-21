import time
import subprocess

while True:
    print("this will run after every 30 sec")
    subprocess.call([r"python", r".\vliegtuigen_rond_locatie\Python\vliegtuigen_rondom_locatie_mysql.py"], timeout=30)
    time.sleep(30)