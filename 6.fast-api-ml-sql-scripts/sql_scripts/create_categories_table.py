import psycopg2

def create_categories_table():
    connection = psycopg2.connect(
        "dbname=your_database user=your_user password=your_password host=localhost port=5432 options='-c client_encoding=UTF8'"
    )
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Categories table created successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_categories_table()