from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///fastapi.db"
SQLALCHEMY_DATABASE_URL =f"sqlite:///{settings.database_name}.db"

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@ip-address/hostname/"
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on')) # for sqlite3.x
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()