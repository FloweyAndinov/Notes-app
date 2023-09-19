#database for misc schema 



from . import db 
from sqlalchemy.sql import func

class DarkMode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    darkModeEnabled = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))