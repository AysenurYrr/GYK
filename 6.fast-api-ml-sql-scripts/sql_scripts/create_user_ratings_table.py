import psycopg2

def create_user_ratings_table():
    connection = psycopg2.connect(
        dbname="moviedb",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_ratings (
        user_id INT,
        movie_id INT,
        rating FLOAT,
        PRIMARY KEY (user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("User Ratings table created successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_user_ratings_table()