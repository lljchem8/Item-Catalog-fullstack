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

# create a public user
User1 = User(name='public', email='public@gmail.com')
session.add(User1)

User2 = User(name='private', email='private@gmail.com')
session.add(User2)
session.commit()

# item for privary coin
catalog1 = Catalog(catalogName="smart contract")

session.add(catalog1)
session.commit()

item1 = Item(user_id=1, itemName="Ethereum", description="""Ethereum is an open-source, public,
                 blockchain-based distributed computing platform and operating 
                 system featuring smart contract (scripting) functionality. 
                 It supports a modified version of Nakamoto consensus 
                 via transaction-based state transitions.""", catalog=catalog1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, itemName="NEO", description="""NEO (formerly Antshares) was founded in 2014 by 
    Da HongFei and Erik Zhang. NEO is an open-source, 
    community driven platform for decentralized applications. 
    Along with the rebranding from Antshares in 2017, 
    the vision to realise a “smart economy” was established. 
    It is to utilize blockchain technology and digital identity to digitize assets, 
    smart contracts are employed to automate the management of these digital assets.
""", catalog=catalog1)

session.add(item2)
session.commit()


item3 = Item(user_id=2, itemName="ADa", description="""ADA is a third generation of smart contract platform
""", catalog=catalog1)

session.add(item3)
session.commit()


# catalog 2
catalog2 = Catalog(catalogName="privacy coin")

session.add(catalog2)
session.commit()

item1 = Item(user_id=1, itemName="Zcash", description="""Zcash is a cryptocurrency aimed at 
    using cryptography to provide enhanced privacy for its users compared 
    to other cryptocurrencies such as Bitcoin. Like Bitcoin, 
        Zcash has a fixed total supply of 21 million units.""", catalog=catalog2)

session.add(item1)
session.commit()

item2 = Item(user_id=1, itemName="Monero", description="""Monero is an open-source cryptocurrency 
                  created in April 2014 that focuses on fungibility, 
                    privacy and decentralization. Monero uses an obfuscated public ledger, 
                    meaning anybody can broadcast or send transactions, 
                    but no outside observer can tell the source, amount or destination.""", catalog=catalog2)

session.add(item2)
session.commit()


print("added items!")
