from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from dbsetup import *

engine = create_engine('sqlite:///catlogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create fake users
User1 = User(name="Basma Ashour",
              email="basmaashouur@gmail.com",
              picture='https://lh6.googleusercontent.com/--Dj32gThDhg/AAAAAAAAAAI/AAAAAAAAEAE/wVzZWy-LLbg/photo.jpg')
session.add(User1)
session.commit()


# Create fake categories
Category1 = Category(title="Competitive programming",
                      user_id=1)
session.add(Category1)
session.commit()

Category2 = Category(title="Machine Learnining",
                      user_id=1)
session.add(Category2)
session.commit

Category3 = Category(title="Technology",
                      user_id=1)
session.add(Category3)
session.commit()

Category4 = Category(title="Academic",
                      user_id=1)
session.add(Category4)
session.commit()

Category5 = Category(title="Mathematics",
                      user_id=1)
session.add(Category5)
session.commit()

# Populate a category with items for testing
Item1 = Item(title="Computational geometry",
	         date=datetime.datetime.now(),
	         description="Finish the sheet",
	         img="https://i.pinimg.com/originals/23/09/13/230913a86ddd5b60a5a08ee49ebb11fe.png",
	         category_id=1,
	         user_id=1, 
	         cattitle="Competitive programming")
session.add(Item1)
session.commit()

Item2 = Item(title="Coursera machine learning",
	         date=datetime.datetime.now(),
	         description="Finish the course",
	         img="http://biginja.com/wp-content/uploads/2016/10/MLseries-1.png",
	         category_id=2,
	         user_id=1, 
	         cattitle="Machine Learnining")
session.add(Item2)
session.commit()

Item3 = Item(title="Full stack nanodegree udacity",
	         date=datetime.datetime.now(),
	         description="Finish the nanodegree",
	         img="http://geekreactor.net/wp-content/uploads/2017/01/Full-Stack-wallpaper-v2.jpg",
	         category_id=3,
	         user_id=1, 
	         cattitle="Technology")
session.add(Item3)
session.commit()

Item4 = Item(title="Operating system",
	         date=datetime.datetime.now(),
	         description="Finish reading the book",
	         img="https://wallpaperscraft.com/image/ubuntu_operating_system_heart_text_black_30926_3840x2160.jpg",
	         category_id=4,
	         user_id=1, 
	         cattitle="Academic")
session.add(Item4)
session.commit()

Item5 = Item(title="Discrete mathematics",
	         date=datetime.datetime.now(),
	         description="Finish number theory",
	         img="http://nihal111.github.io/WnCC/images/competitive3.png",
	         category_id=5,
	         user_id=1, 
	         cattitle="Mathematics")
session.add(Item5)
session.commit()


print "Your database has been populated with fake data!"
