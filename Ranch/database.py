from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import settings

conf = settings.Configure()
engine = create_engine(conf.database_connection_string, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import Ranch.models
    Base.metadata.create_all(bind=engine)
