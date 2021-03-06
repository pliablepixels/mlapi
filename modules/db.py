from tinydb import TinyDB, Query, where
from passlib.hash import bcrypt
import modules.common_params as g
import getpass

class Database:

    def _get_hash(self,password):
        return bcrypt.hash(password)
    
    def __init__(self, prompt_to_create=True):
        db = g.config['db_path']+'/db.json'
        g.log.Debug (1,'Opening DB at {}'.format(db))
        self.db = TinyDB(db)
        self.users = self.db.table('users')
        self.query = Query()
        g.log.Debug (1,'DB engine ready')
        if not len(self.users) and prompt_to_create:
            g.log.Debug (1,'Initializing default users')

            print ('--------------- User Creation ------------')
            print ('Please configure atleast one user:')
            while True:
                name = input ('user name:')
                if not name:
                    print ('Error: username needed')
                    continue
                p1 = getpass.getpass('Please enter password:')
                if not p1:
                    print ('Error: password cannot be empty')
                    continue
                p2 = getpass.getpass('Please re-enter password:')
                if  p1 != p2:
                    print ('Passwords do not match, please re-try')
                    continue
                break  
            self.users.insert({'name':name, 'password':self._get_hash(p1)})
            print ('------- User: {} created ----------------'.format(name))

    
    def check_credentials(self,user, supplied_password):
        user_object = self.get_user(user)
        if not user_object:
            return False # user doesn't exist
        stored_password_hash = user_object.get('password')
       
        if not bcrypt.verify(supplied_password, stored_password_hash):
            g.log.Debug (1,'Hashes do NOT match: incorrect password')
            return False
        else:
            g.log.Debug (1,'Hashes are correct: password matched')
            return  True


    def get_all_users(self):
        return self.users.all()

    def get_user(self, user):
        return self.users.get(self.query.name == user)

    def delete_user(self,user):
        return self.users.remove(where('name')==user)

    def add_user(self, user,password):
        hashed_password = self._get_hash(password)
        return self.users.upsert({'name':user, 'password':hashed_password}, self.query.name == user)








