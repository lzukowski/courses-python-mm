from typing import cast

from injector import Module, provider, singleton
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, Session, sessionmaker

Base = declarative_base()


class PersistenceModule(Module):
    @singleton
    @provider
    def _session(self) -> Session:
        engine = create_engine('sqlite:///')
        Base.metadata.create_all(engine)
        maker = sessionmaker(bind=engine)
        return cast(Session, scoped_session(maker))
