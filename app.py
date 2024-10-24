from dotenv import load_dotenv  # Librería externa
from flask import Flask  # Librería externa
from routes import routes  # Importación local (routes)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


# Iniciar la aplicación Flask
app = Flask(__name__)

# Registrar las rutas del blueprint
app.register_blueprint(routes)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
