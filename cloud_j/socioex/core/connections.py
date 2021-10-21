import pymongo 
import urllib.parse

# Admin username = edaivajobs_mongoadmin
# Admin Password = Admin@123

# MONGO_PREFIX = 'mongod'
# MONGO_USERNAME = CONFIG["MONGO_USERNAME"]
# MONGO_PASSWORD = CONFIG["MONGO_PASSWORD"]
# MONGO_IP_PORT = CONFIG["MONGO_IP_PORT"]
# MONGO_DB_WITH_AUTH = CONFIG["MONGO_DB_WITH_AUTH"]

# username = urllib.parse.quote_plus(MONGO_USERNAME)
# password = urllib.parse.quote_plus(MONGO_PASSWORD)

# myclient = pymongo.MongoClient("%s://%s:%s@%s/%s" % (MONGO_PREFIX, username, password, MONGO_IP_PORT, MONGO_DB_WITH_AUTH))
myclient = pymongo.MongoClient("mongodb://localhost:27017/cloud_socioex")

mydb = myclient.get_database()

def export_db_class():

    return mydb

print(mydb)