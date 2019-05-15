from pymongo import MongoClient
import datetime
from pprint import *


class DatabaseController():

    # Initialize connection to database  ***
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['doc-share']

    # Close connection to database  ***
    def __del__(self):
        self.client.close()

    #####################
    #  User Management
    #####################

    # Sign up a new user to database   ***
    def sign_up(self, username_in, password_in, email_in, firstName_in, lastName_in):
        qry = {"username": username_in}
        user_info = self.db.Users.find_one(qry)
        if user_info:
            print(f"DB: Username '{user_info['username']}' is taken")
            return False
        else:
            qry = {"_id": self.db.Users.count_documents({})+1,
                   "user_type": "user",
                   "username": username_in,
                   "password": password_in,
                   "email": email_in,
                   "firstName": firstName_in,
                   "lastName": lastName_in,
                   "is_banned": False}
            self.db.Users.insert_one(qry)
            return True

    # Log in   ***
    def log_in(self, username_in, password_in):
        qry = {"username": username_in}
        user_info = self.db.Users.find_one(qry)
        try:
            if password_in == user_info['password']:
                # Check if baned
                if user_info["is_banned"]:  # is_in_blacklist
                    print(f"DB: Login failed, account has been banned!")
                    return -1
                else:
                    print(f"DB: Login succeeds!")
                    return 1
            else:
                print(f"DB: Password doesn't match!")
                return 0
        except:
            print(f"DB: Username doesn't exist!")
            return 0

    # Get user type   ***
    def get_user_type(self, username_in):
        qry = {"username": username_in}
        user_info = self.db.Users.find_one(qry)
        user_type = user_info['user_type']
        return user_type

    # Get all users   ***
    def get_all_users(self):
        users = self.db.Users.find().sort("_id")
        return users

    # Make user   ***
    def make_user(self, id_in):
        qry = {"_id": int(id_in)}
        new_values = {"$set": {"user_type": "user"}}
        self.db.Users.update_one(qry, new_values)
        return

    # Make admin   ***
    def make_admin(self, id_in):
        qry = {"_id": int(id_in)}
        new_values = {"$set": {"user_type": "admin"}}
        self.db.Users.update_one(qry, new_values)
        return

    # Ban user   ***
    def ban_user(self, id_in):
        qry = {"_id": int(id_in)}
        new_values = {"$set": {"is_banned": True}}
        self.db.Users.update_one(qry, new_values)
        return

    # Unban user   ***
    def unban_user(self, id_in):
        qry = {"_id": int(id_in)}
        new_values = {"$set": {"is_banned": False}}
        self.db.Users.update_one(qry, new_values)
        return

    ##########################
    #   Document Management
    ##########################

    # Create document   ***
    def create_doc(self, title_in, owner_in, content_in, is_private_in):
        if is_private_in:
            status = "private"
        else:
            status = "public"

        id = self.db.Documents.find_one(sort=[("_id", -1)])["_id"] + 1
        qry = {"_id": id,
               "status": status,
               "title": title_in,
               "owner": owner_in,
               "content": content_in,
               "create_date": datetime.datetime.now(),
               "modify_date": datetime.datetime.now(),
               "history": {}}
        self.db.Documents.insert_one(qry)
        return True

    # Edit document, must be followed by edit_hist() function   ***
    def edit_doc(self, doc_id_in, title_in, content_in, is_private_in):
        if is_private_in:
            status = "private"
        else:
            status = "public"
        qry = {"_id": int(doc_id_in)}
        new_values = {"$set": {"title": title_in,
                               "status": status,
                               "content": content_in,
                               "modify_date": datetime.datetime.now()}}
        self.db.Documents.update_one(qry, new_values)
        return True

    # Write document history after editing, must follow edit_doc() function  ***
    def edit_hist(self, doc_id_in, title_in, user_in, content_in, date_in):
        qry = {"_id": int(doc_id_in)}
        doc = self.db.Documents.find_one(qry)
        if doc["history"]:
            record_id = doc["history"][-1]["record_id"] + 1
        else:
            record_id = 1
        hist = doc["history"]
        new_hist = {"record_id": record_id,
                    "title": title_in,
                    "user": user_in,
                    "content": content_in,
                    "modify_date": date_in}
        hist.append(new_hist)
        new_values = {"$set": {"history": hist}}
        self.db.Documents.update_one(qry, new_values)
        return True

    # Delete document   ***
    def delete_doc(self, doc_id_in):
        qry = {"_id": int(doc_id_in)}
        self.db.Documents.delete_one(qry)
        return True

    #############################
    #       Get Documents
    #############################

    # Get public documents for GUEST (non-user)!!!   ***
    def get_docs_public(self):
        qry = {"status": "public"}
        docs = self.db.Documents.find(qry)
        return docs

    # Get available documents for USER   ***
    def get_docs_user(self, username_in):
        qry = {"$or": [{"status": "public"}, {"owner": username_in}]}
        docs = self.db.Documents.find(qry)
        return docs

    # Get ALL documents for ADMIN   ***
    def get_docs_admin(self):
        docs = self.db.Documents.find()
        return docs

    # Get document history list   ***
    def get_hist_list(self, id_in, username_in):
        # Get doc info by id
        qry = {"_id": int(id_in)}
        doc = self.db.Documents.find_one(qry)
        
        # Return doc if it's public
        if doc['status'] == "public":
            return doc, True

        qry = {"username": username_in}
        user = self.db.Users.find_one(qry)
        if user['user_type'] == "admin":    # Admin gets everything
            return doc, True
        elif user['username'] == doc['owner']:  # Doc owner can view the doc
            return doc, True
        else:
            return False, False


    # Get document by id   ***
    def get_doc_by_id(self, id_in, username_in=''):
        # Get doc by id
        qry = {"_id": int(id_in)}
        doc = self.db.Documents.find_one(qry)

        # Return doc if it's public
        if doc['status'] == "public":
            return doc

        # User not logged in, doesn't have access to doc
        if username_in == '':
            return False

        # User is logged in
        else:
            qry = {"username": username_in}
            user = self.db.Users.find_one(qry)
            if user['user_type'] == "admin":    # Admin gets everything
                return doc
            elif user['username'] == doc['owner']:  # Doc owner can view the doc
                return doc
            else:
                return False


    # Get history version document by id   ***
    def get_doc_hist_by_id(self, doc_id, record_id_in, username_in=''):

        # Get doc info by id
        qry = {"_id": int(doc_id)}
        doc = self.db.Documents.find_one(qry)
        # Return doc if it's public
        if doc['status'] == "public":
            return doc["history"][int(record_id_in)-1]
        
        # User not logged in, doesn't have access to doc
        if username_in == '':
            return False

        # User is logged in
        else:
            qry = {"username": username_in}
            user = self.db.Users.find_one(qry)
            if user['user_type'] == "admin":    # Admin gets everything
                return doc["history"][int(record_id_in)-1]
            elif user['username'] == doc['owner']:  # Doc owner can view the doc
                return doc["history"][int(record_id_in)-1]
            else:
                return False
