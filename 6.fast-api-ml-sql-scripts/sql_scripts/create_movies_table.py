import psycopg2

def create_movies_table():
    connection = psycopg2.connect(
        dbname="moviedb",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        category_id INT REFERENCES categories(category_id),
        imdb_rating FLOAT,
        release_year INT,
        duration_minutes INT,
        description TEXT
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Movies table created successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_movies_table()