from .models import Base, get_engine, get_session, City, WeatherReport

def seed_data():
    engine = get_engine()
    Base.metadata.create_all(engine)
    session = get_session(engine)

  
    session.query(WeatherReport).delete()
    session.query(City).delete()
    session.commit()

   
    city1 = City.create(session, "Nairobi")
    city2 = City.create(session, "Mombasa")
    city3 = City.create(session, "Kisumu")

 
    WeatherReport.create(session, city1, 22.5, "Sunny and warm")
    WeatherReport.create(session, city1, 18.0, "Cool with clouds")
    WeatherReport.create(session, city2, 30.0, "Hot and humid")
    WeatherReport.create(session, city3, 20.0, "Light rain showers")

    print("Database seeded.")
