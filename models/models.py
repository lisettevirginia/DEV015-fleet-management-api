from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Declarative base para los modelos
Base = declarative_base()

# Modelo para la tabla de taxis
class Taxi(Base):
    """
    Representa la tabla de taxis en la base de datos.
    """
    __tablename__ = "taxis"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, index=True)

# Modelo para la tabla de trayectorias
class Trajectory(Base):
    """
    Representa la tabla de trayectorias (ubicaciones) en la base de datos.
    """
    __tablename__ = "trajectories"
    id = Column(Integer, primary_key=True, index=True)
    taxi_id = Column(Integer, ForeignKey('taxis.id'))
    date = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)

    # Relación con la tabla de taxis
    taxi = relationship("Taxi", back_populates="trajectories")