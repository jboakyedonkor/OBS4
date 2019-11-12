from server import db, ma

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String)

    def __init__(self, email, password, token):
        self.email = email
        self.password = password
        self.token = token

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'email', 'password', 'token')