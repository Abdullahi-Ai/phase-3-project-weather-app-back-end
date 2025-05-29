from lib.db.models import Base, get_engine

def create_tables():
    engine = get_engine()  
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
