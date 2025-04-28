import psycopg2

def create_users_table():
    connection = psycopg2.connect(
        dbname="moviedb",
        user="postgres",
        password="!37Selaminsan",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        watched_movies INT[]
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Users table created successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_users_table()