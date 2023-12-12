from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_CONNECTION

engine = create_engine(POSTGRES_CONNECTION)
Session = sessionmaker(engine)
 