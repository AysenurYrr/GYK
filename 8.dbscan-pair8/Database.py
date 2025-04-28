from sqlalchemy import create_engine

# Database connection information
user = 'postgres'
password = "x"
host = 'localhost'
port = '5432'
database = "YZ2Northwind"


engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
