#!/usr/bin/env python3
"""
Скрипт для наповнення таблиць даними.
Вставляємо дані для таблиць status, users, tasks.
"""

import psycopg2
import sys

def populate_tables():
    # Параметри підключення до бази даних (змініть їх відповідно до вашої конфігурації)
    conn_params = {
        'dbname': 'task_management',
        'user': 'postgres',
        'password': 'len',
        'host': 'localhost',
        'port': 5432
    }

    # Дані для вставки
    users_data = [
        ('John Doe', 'john.doe@example.com'),
        ('Jane Smith', 'jane.smith@example.com'),
        ('Alice Johnson', 'alice.johnson@example.com')
    ]
    status_data = [
        ('new',),
        ('in progress',),
        ('completed',)
    ]
    # Для таблиці tasks використовуємо дані, які потім зіставимо з id статусу та користувача
    tasks_data = [
        # (title, description, status_name, user_email)
        ('Task 1', 'Description of Task 1', 'new', 'john.doe@example.com'),
        ('Task 2', 'Description of Task 2', 'in progress', 'jane.smith@example.com'),
        ('Task 3', 'Description of Task 3', 'completed', 'alice.johnson@example.com')
    ]

    conn = None
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = False
        with conn.cursor() as cur:
            # Вставка статусів
            cur.executemany(
                "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                status_data
            )
            
            # Вставка користувачів
            cur.executemany(
                "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                users_data
            )
            
            # Вставка завдань: отримуємо id статусу та користувача за допомогою SELECT
            for title, description, status_name, user_email in tasks_data:
                # Отримання status_id
                cur.execute("SELECT id FROM status WHERE name = %s", (status_name,))
                status_row = cur.fetchone()
                if not status_row:
                    raise Exception(f"Статус '{status_name}' не знайдено.")
                status_id = status_row[0]
                
                # Отримання user_id
                cur.execute("SELECT id FROM users WHERE email = %s", (user_email,))
                user_row = cur.fetchone()
                if not user_row:
                    raise Exception(f"Користувача з email '{user_email}' не знайдено.")
                user_id = user_row[0]
                
                # Вставка запису в таблицю tasks
                cur.execute(
                    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id)
                )
            
            conn.commit()
        print("Дані успішно додано до таблиць.")
    except Exception as error:
        if conn:
            conn.rollback()
        print("Помилка при додаванні даних:", error)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    populate_tables()
