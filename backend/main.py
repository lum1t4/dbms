import oracledb
import os
import dotenv



dotenv.load_dotenv()


DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABSE_DSN = os.environ.get("DATABSE_DSN")
connection = oracledb.connect(user=DATABASE_USER, password=DATABASE_PASSWORD, dsn=DATABSE_DSN)

cursor = connection.cursor()
cursor.execute("SELECT sysdate FROM dual")
for row in cursor:
    print(row)

cursor.close()
connection.close()
