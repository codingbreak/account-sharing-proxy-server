from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(50), nullable=False)
    keys_values = db.Column(db.JSON)

    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", backref=db.backref("credentials", lazy=True))

    def __repr__(self):
        return "<Credential %r - %r>" % (self.user.username, self.website)


class Shared_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    credential_id = db.Column(db.ForeignKey('credential.id'), nullable=False)
    credential = db.relationship("Credential", backref=db.backref("shared_users", lazy=True))

    shared_user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    shared_user = db.relationship("User", backref=db.backref("shared_users"))
