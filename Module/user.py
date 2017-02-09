from Common.database import Database


class User(object):


    def __init__(self,name,account,password):
        self.name = name
        self.account = account
        self.password = password

    @staticmethod
    def is_login_valid(account,password):
        user_data = Database.find_one(collection='users',query={"account": account})
        if user_data == None:
            return False
        elif user_data['password'] != password:
            return False
        return True

    @staticmethod
    def register(name, account, password):
        user_data = Database.find_one(collection='users', query={"account": account})
        if user_data is not None:
            return False

        User(name, account, password).save_to_db()
        return True

    def save_to_db(self):
        Database.insert(collection='users',data=self.json())

    def json(self):
        return{
            "name": self.name,
            "account": self.account,
            "password": self.password
        }

    def find_user_data(account):
        user_data = Database.find_one(collection='users',query={"account":account})

        return user_data

