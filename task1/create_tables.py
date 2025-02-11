import psycopg2
import sys

def create_tables():
    # Параметри підключення до бази даних (змініть їх відповідно до вашої конфігурації)
    conn_params = {
        'dbname': 'task_management',
        'user': 'postgres',
        'password': 'len',
        'host': 'localhost',
        'port': 5432
    }

    # SQL-команди для створення таблиць із необхідними обмеженнями
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            CONSTRAINT fk_status
                FOREIGN KEY(status_id)
                    REFERENCES status(id)
                    ON DELETE CASCADE,
            CONSTRAINT fk_user
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
        )
        """
    ]

    # Дані для вставки в таблицю status
    status_data = [
        ('new',),
        ('in progress',),
        ('completed',)
    ]


    conn = None
    try:
        # Встановлюємо з'єднання з PostgreSQL
        conn = psycopg2.connect(**conn_params)
        if conn:
            print("Database connected successfully")
        conn.autocommit = False  # використання транзакцій
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
            conn.commit()
        print("Таблиці успішно створено.")
    except Exception as error:
        if conn:
            conn.rollback()
        print("Помилка при створенні таблиць:", error)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_tables()