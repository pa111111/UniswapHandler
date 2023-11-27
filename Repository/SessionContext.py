from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Repository.Settings import UNISWAP_DB_CONNECTION_STRING


class SessionContext:
    def __enter__(self):
        engine = create_engine(UNISWAP_DB_CONNECTION_STRING)
        session_factory = sessionmaker(bind=engine)
        self.session = session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
