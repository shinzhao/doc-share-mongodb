# DocShare

## Requirements
- [Python3](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/)
- [Flask](http://flask.pocoo.org/)

## Install MongoDB
Go to MongoDB website provided above and download MongoDB local version.
Install MongoDB and run mongod to start server

## Initialize database
Go to folder **init_db**, open **init_mongo.py**.
Edit **MongoClient** to your database port(using 27017 by default).
Then run following command to initialize the database.
```
python init_mongo.py
```

## Start server
Go back to main directory and run the following command.
Port 8000 is being used.
```
python app.py
```

## Open app
Open your web broswer and go to [127.0.0.1:8000](127.0.0.1:8000) to use the app.