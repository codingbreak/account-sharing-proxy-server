from account_sharing_db import *
from sqlalchemy import insert, select, bindparam


# Create user account
new_user = User(name="tientu", fullname="Tien Tu VO", email="votientu@gmail.com", password="nothing")

session.add(new_user)
