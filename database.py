from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


if __name__ == "__main__":
    db.create_all()

    admin = User(username="admin", email="admin@example.com")
    guest = User(username="guest", email="guest@example.com")
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()

    admin_wsj_cre = Credential(website="https://www.wsj.com/",user=admin)
    db.session.add(admin_wsj_cre)
    db.session.commit()

    guest_friend = User(username="guest_friend", email="guest_friend@example.com")
    guest_wsj_cre_to_guest_friend = Shared_User(credential=guest_wsj_cre, shared_user=guest_friend)
    session.add(guest_friend)
    session.add(guest_wsj_cre_to_guest_friend)
    db.session.commit()
        
