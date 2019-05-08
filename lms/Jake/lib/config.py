import sqlite3
import os

""" Set up sql configurations here """
table_name = "Robot"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

name = ROOT_DIR +"/"
#print(name)
conn = sqlite3.connect(name+'Robot.db',check_same_thread=False)
cursor = conn.cursor()
try:
    cur = cursor.execute("SELECT * FROM {}".format(table_name))
except:
    columns = []
else:
    columns = [x[0] for x in cur.description]
cursor.close()