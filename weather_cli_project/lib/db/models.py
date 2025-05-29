from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    weather_reports = relationship('WeatherReport', back_populates='city', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}')>"

    @classmethod
    def create(cls, session, name):
        if not name.strip():
            raise ValueError("Oops! City name can't be empty.")
        city = cls(name=name.strip().title())
        session.add(city)
        session.commit()
        return city

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, city_id):
        return session.query(cls).filter_by(id=city_id).first()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()

    def delete(self, session):
        session.delete(self)
        session.commit()

class WeatherReport(Base):
    __tablename__ = 'weather_reports'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    temperature_c = Column(Float, nullable=False)
    description = Column(String(255))

    city = relationship('City', back_populates='weather_reports')

    def __repr__(self):
        return (f"<WeatherReport(id={self.id}, city_id={self.city_id}, date={self.date}, "
                f"temp_c={self.temperature_c}, desc='{self.description}')>")

    @classmethod
    def create(cls, session, city, temperature_c, description):
        if temperature_c < -100 or temperature_c > 100:
            raise ValueError("The temperature must be realistic.")
        report = cls(city=city, temperature_c=temperature_c, description=description.strip())
        session.add(report)
        session.commit()
        return report

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, report_id):
        return session.query(cls).filter_by(id=report_id).first()

    def delete(self, session):
        session.delete(self)
        session.commit()


def get_engine(db_url='sqlite:///weather.db'):
    return create_engine(db_url, echo=False)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
