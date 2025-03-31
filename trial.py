import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="annlita", passwd="aadannia@DB", db="NetGuardDB")
    print("Connected to MySQL successfully!")
except MySQLdb.OperationalError as e:
    print(f"Error: {e}")
