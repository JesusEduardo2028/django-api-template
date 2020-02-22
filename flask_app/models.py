class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))
    facebook_id = db.Column(db.String(250))
    google_id = db.Column(db.String(250))

    def __init__(self, name, email, password, facebookId, googleId):
        self.name = name
        self.email = email
        self.password = password
        self.facebook_id = facebookId
        self.google_id = googleId