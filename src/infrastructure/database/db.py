from sqlalchemy import MetaData , create_engine

DATABASE_URL = DATABASE_URL = "postgresql://abood:abood123@localhost:5432/db_project"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
