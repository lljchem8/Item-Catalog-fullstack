from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Item, Base, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# items = session.query(Item).order_by(Item.id.desc()).limit(10)
# for item in items:
#     print(item.serialize)

items = session.query(Item).all()
for item in items:
    print(item.user_id)

users = session.query(User).all()
for user in users:
    if user.picture:
        print(user.picture)


# catalogs = session.query(Catalog).all()
# for catalog in catalogs:
#     # print("catalog_id: {}, name: {}".format(catalog.id, catalog.name))
#     print(catalog.serialize)
