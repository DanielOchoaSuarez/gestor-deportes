import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base

db_user = os.getenv('DB_USER', 'laad')
db_password = os.getenv('DB_PASSWORD', 'laad')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'sport_app_db')

connect_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connect_string,
                       pool_size=5,
                       max_overflow=2,
                       pool_recycle=300,
                       pool_pre_ping=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from .deporte import Deporte
    from .ejercicio_deporte import EjercicioDeporte
    from .plan_ejercicio import PlanEjercicio
    Base.metadata.create_all(bind=engine)
