class User():
    def __init__(self, id, username, active=True):
        self.id = id
        self.username = username
        self.active = active

    def is_active(self):
        return True 
    
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id
    
USERS = {
    "1221" : User("1221", 'user1')
}