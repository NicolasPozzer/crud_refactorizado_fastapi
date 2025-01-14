from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSW")
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_NAME")

URL_DATABASE = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"


# creamos motor de conexion y session
engine = create_engine(URL_DATABASE)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# luego utilizamos esto en el main para crear las tablas
Base = declarative_base()


# dependencia para obtener la session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()