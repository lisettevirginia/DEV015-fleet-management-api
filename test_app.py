import pytest
from unittest.mock import patch
from app import app, Taxi

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Simulación de la base de datos usando mock
@patch('app.SessionLocal')
def test_get_taxis(mock_session, client):
    # Crear un objeto taxi simulado
    mock_taxi = Taxi(id=1, plate='ABC123')

    # Crear una sesión simulada con los datos que queremos devolver
    mock_query = mock_session.return_value.query.return_value
    mock_query.offset.return_value.limit.return_value.all.return_value = [mock_taxi]

    # Realizar una solicitud GET al endpoint sin filtros ni paginación
    response = client.get('/taxis')

    # Verificar que la respuesta tenga un código 200
    assert response.status_code == 200

    # Verificar que el contenido JSON sea el esperado
    expected = [{"id": 1, "plate": "ABC123"}]
    assert response.get_json() == expected

    