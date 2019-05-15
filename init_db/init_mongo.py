from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://localhost:27017')
client.drop_database('doc-share')  # Drop db if already exists
db = client['doc-share']

# Create users
users = [{"_id": 1,
          "user_type": "admin",
          "username": "xin",
          "password": "xin",
          "email": "test@gmail.com",
          "firstName": "xin",
          "lastName": "zhao",
          "is_banned": False},

         {"_id": 2,
          "user_type": "user",
          "username": "shin",
          "password": "shin",
          "email": "test@gmail.com",
          "firstName": "xin",
          "lastName": "zhao",
          "is_banned": False}]
db.Users.insert_many(users)

# Create Documents
docs = [{"_id": 1,
         "status": "private",
         "title": "xin1",
         "owner": "xin",
         "content": "test",
         "create_date": datetime.datetime.now(),
         "modify_date": datetime.datetime.now(),
         "history": []},

        {"_id": 2,
         "status": "private",
         "title": "xin2",
         "owner": "xin",
         "content": "test",
         "create_date": datetime.datetime.now(),
         "modify_date": datetime.datetime.now(),
         "history": []},

         {"_id": 3,
         "status": "private",
         "title": "shin1",
         "owner": "shin",
         "content": "test",
         "create_date": datetime.datetime.now(),
         "modify_date": datetime.datetime.now(),
         "history": []},

         {"_id": 4,
         "status": "private",
         "title": "shin2",
         "owner": "shin",
         "content": "test",
         "create_date": datetime.datetime.now(),
         "modify_date": datetime.datetime.now(),
         "history": []},

         {"_id": 5,
         "status": "public",
         "title": "shin3",
         "owner": "shin",
         "content": "test",
         "create_date": datetime.datetime.now(),
         "modify_date": datetime.datetime.now(),
         "history": []},]
db.Documents.insert_many(docs)