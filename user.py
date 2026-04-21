<<<<<<< HEAD
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
=======
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
>>>>>>> a4f7494f5e69b82888191170890e42a645601681
        self.id = id