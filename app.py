import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Crear la conexión a la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Iniciar la aplicación Flask
app = Flask(__name__)

# Definir el modelo Taxi
class Taxi(Base):
    __tablename__ = "taxis"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, index=True)

# Crear la base de datos
Base.metadata.create_all(bind=engine)

# Endpoint para listar taxis con paginación y filtrado
@app.route('/taxis', methods=['GET'])
def get_taxis():
    session = SessionLocal()
    # Obtener parámetros de paginación y filtrado
    plate_filter = request.args.get('plate')

    # Verificar que el número de página esté entre 1 y 10
    try:
        page = int(request.args.get('page', 1))
        if page < 1 or page > 10:
            page = 10
    except ValueError:
        page = 1  # Valor por defecto si no es un número válido

    # Verificar que el número de resultados por página esté entre 1 y 10
    try:
        limit = int(request.args.get('limit', 10))
        if limit < 1 or limit > 10:
            limit = 10
    except ValueError:
        limit = 10  # Valor por defecto si no es un número válido

    # Construir la consulta
    query = session.query(Taxi)
    if plate_filter:
        query = query.filter(Taxi.plate.ilike(f'%{plate_filter}%'))

    # Paginación
    taxis = query.offset((page - 1) * limit).limit(limit).all()

    # Preparar la respuesta
    result = [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis]
    # Retornar como JSON
    return jsonify(result)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
