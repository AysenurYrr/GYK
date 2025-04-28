from sqlalchemy import create_engine
from database import DATABASE_URL, Base
import models  # Register models with Base

def main():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("All tables created successfully.")

if __name__ == '__main__':
    main()