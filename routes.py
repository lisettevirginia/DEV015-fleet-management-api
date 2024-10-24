from flask import Blueprint, jsonify, request  # Librerías externas
from sqlalchemy.orm import joinedload
from database import SessionLocal  # Ahora SessionLocal viene de database.py
from models.models import Taxi, Trajectory # Importa los modelos desde models.py

# Definir el blueprint para las rutas
routes = Blueprint('routes', __name__)

# Endpoint para listar taxis con paginación y filtrado
@routes.route('/taxis', methods=['GET'])
def get_taxis():
    session = SessionLocal()
    try:
        # Obtener parámetros de paginación y filtrado
        plate_filter = request.args.get('plate')
        try:
            page = int(request.args.get('page', 1))
            if page < 1 or page > 10:
                page = 10
        except ValueError:
            page = 1  # Valor por defecto

        try:
            limit = int(request.args.get('limit', 10))
            if limit < 1 or limit > 10:
                limit = 10
        except ValueError:
            limit = 10  # Valor por defecto

        # Construir la consulta
        query = session.query(Taxi)
        if plate_filter:
            query = query.filter(Taxi.plate.ilike(f'%{plate_filter}%'))

        # Paginación
        taxis = query.offset((page - 1) * limit).limit(limit).all()

        # Preparar la respuesta
        result = [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis]
        return jsonify(result)
    
    finally:
        session.close()

# Endpoint para obtener el historial de ubicaciones por taxi y fecha
@routes.route('/trajectories', methods=['GET'])
def get_trajectories():
    session = SessionLocal()

    # Consulta a la base de datos para obtener trayectorias con la placa del taxi
    results = session.query(Trajectories).options(joinedload(Trajectories.taxi)).all()

    # Estructurar los datos de respuesta en formato JSON
    response = []
    for trajectories in results:
        response.append({
            "id": trajectories.id,
            "plate": trajectories.taxi.plate,  # Placa del taxi relacionada
            "taxiId": trajectories.taxi_id,
            "date": trajectories.date.isoformat(),  # Convertir a formato ISO
            "latitude": trajectories.latitude,
            "longitude": trajectories.longitude
        })

    session.close()

    return jsonify(response)

