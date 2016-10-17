# import numpy as np
# import pandas as pd 
# import matplotlib.pyplot as plt

# initialize
import sys
sys.path.append('/home/chong/anaconda2/lib/python2.7/site-packages')
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=False)


# create users table

from sqlalchemy import Column, Integer, String
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	password = Column(String)

	def __repr__(self):
		return "<User(name='%s', fullname='%s', password='%s')>" % (
	            self.name, self.fullname, self.password)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# Base.metadata.create_all(engine)
User.__table__.create(engine)


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# DO SOME QUERYING

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'),
	User(name='mary', fullname='Mary Contrary', password='xxg527'), 
	User(name='fred', fullname='Fred Flinstone', password='blah')])
session.commit()

our_user = session.query(User).filter_by(name='ed').first()
print our_user

ed_user.password = 'f8s7ccs'
our_user = session.query(User).filter_by(name='ed').first()
print our_user

session.rollback() #rolls back to the last commit
our_user = session.query(User).filter_by(name='ed').first()
print our_user


# add another table with a relationship

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
	__tablename__ = 'addresses'
	id = Column(Integer, primary_key=True)
	email_address = Column(String, nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship("User", back_populates="addresses")

	def __repr__(self):
		return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

Address.__table__.create(engine)

