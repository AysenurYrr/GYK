import psycopg2

def create_genres_table():
    connection = psycopg2.connect(
        dbname="moviedb",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS genres (
        genre_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Genres table created successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_genres_table()