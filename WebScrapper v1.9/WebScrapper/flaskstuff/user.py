from random import random
from uuid import uuid4
from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user
    
    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()
    
    @staticmethod
    def get_all():
        db=get_db()
        userdata=db.execute("SELECT * FROM user").fetchall()
        return userdata
        
class User2(UserMixin):
    
    def __init__(self, password, name, email, profile_pic):
        self.password = password
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        

    @staticmethod
    def get(email):
        db=get_db()
        user=db.execute(
            "SELECT * FROM newusers WHERE email = ?", (email,)
        ).fetchone()
        if not user:
            return None
        user=User(
            id_= user[4], name=user[0], email=user[1], profile_pic=user[3]
        )
        return user
    
    @staticmethod
    def create(name, email, password, profile_pic):
        unique_id=str(uuid4())
        db = get_db()
        db.execute(
            "INSERT INTO newusers (name, email, password, profile_pic, unique_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, email, password, profile_pic,unique_id),
        )
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (unique_id, name, email, profile_pic),
        )
        db.commit()
    
    @staticmethod
    def get_all():
        db=get_db()
        userdata=db.execute("SELECT * FROM newusers").fetchall()
        return userdata

    @staticmethod
    def get_pw(email):
        db=get_db()
        user=db.execute(
            "SELECT * FROM newusers WHERE email = ?", (email,)
        ).fetchone()
        if not user:
            return None
        
        user=User2(
            password=user[2], name=user[0], email=user[1], profile_pic=user[3]
        )
        return user.password
    
    @staticmethod
    def check_login(userID,pw):
        db=get_db()
        user=db.execute(
            "select * from newusers where email=? and password=?",(userID,pw,)
        ).fetchone()
        user=User(
            id_=user[4], name=user[0], email=user[1], profile_pic=user[3]
        )
        return user
