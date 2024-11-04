import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Crear la conexión a la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
