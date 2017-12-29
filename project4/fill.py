from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Category, Item

engine = create_engine('sqlite:///catlogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


category1 = Category(title="Study")
session.add(category1)
session.commit()

Item1 = Item(title="db", description="must", category=category1)
session.add(Item1)
session.commit()


