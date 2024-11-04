from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models.models import Taxi, Trajectory  # Asegúrate de que el modelo se llama Trajectory en models.py

routes = Blueprint('routes', __name__)

@routes.route('/taxis', methods=['GET'])
def get_taxis():
    session = SessionLocal()
    try:
        plate_filter = request.args.get('plate')
        try:
            page = int(request.args.get('page', 1))
            if page < 1 or page > 10:
                page = 10
        except ValueError:
            page = 1

        try:
            limit = int(request.args.get('limit', 10))
            if limit < 1 or limit > 10:
                limit = 10
        except ValueError:
            limit = 10

        query = session.query(Taxi)
        if plate_filter:
            query = query.filter(Taxi.plate.ilike(f'%{plate_filter}%'))

        taxis = query.offset((page - 1) * limit).limit(limit).all()

        result = [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis]
        return jsonify(result)
    
    finally:
        session.close()

@routes.route('/trajectories', methods=['GET'])
def get_trajectories():
    session = SessionLocal()

    # Cambié Trajectories a Trajectory
    results = session.query(Trajectory).options(joinedload(Trajectory.taxi)).all()

    response = []
    for trajectory in results:
        response.append({
            "id": trajectory.id,
            "plate": trajectory.taxi.plate,
            "taxiId": trajectory.taxi_id,
            "date": trajectory.date.isoformat(),
            "latitude": trajectory.latitude,
            "longitude": trajectory.longitude
        })

    session.close()
    return jsonify(response)