#!/usr/bin/env python3
"""
Скрипт seed.py заповнює таблиці users, status та tasks випадковими даними за допомогою Faker.

- В таблицю status вставляються стандартні статуси: 'new', 'in progress', 'completed'.
- В таблицю users вставляється певна кількість випадкових користувачів із унікальними email.
- В таблицю tasks вставляються завдання з випадковими заголовками та описами, 
  де кожне завдання прив'язане до випадкового користувача та має статус із переліку.
"""

import psycopg2
import sys
import random
from faker import Faker

def seed_data():
    # Параметри підключення до PostgreSQL (змініть відповідно до вашої конфігурації)
    conn_params = {
        'dbname': 'task_management',
        'user': 'postgres',
        'password': 'len',
        'host': 'localhost',
        'port': 5432
    }
    
    fake = Faker()
    # Для забезпечення унікальності email, використовуємо властивість unique
    # Faker.seed(0)  # (опційно) для відтворюваності результатів

    # Налаштування кількості записів
    num_users = 10
    num_tasks = 20
    statuses = ['new', 'in progress', 'completed']

    conn = None
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = False
        with conn.cursor() as cur:
            # Вставка статусів (якщо такий запис вже існує, пропускаємо)
            for status in statuses:
                cur.execute(
                    "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (status,)
                )
            
            # Вставка користувачів із унікальними даними
            for _ in range(num_users):
                name = fake.name()
                email = fake.unique.email()
                cur.execute(
                    "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                    (name, email)
                )
            
            # Отримання списку user_id після вставки
            cur.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cur.fetchall()]
            if not user_ids:
                raise Exception("Не знайдено жодного користувача після вставки.")
            
            # Отримання статусів (мапа: status name -> id)
            cur.execute("SELECT id, name FROM status")
            status_rows = cur.fetchall()
            status_dict = {name: id for id, name in status_rows}
            
            # Вставка завдань із випадковими даними
            for _ in range(num_tasks):
                title = fake.sentence(nb_words=6)[:100]  # обмеження довжини до 100 символів
                description = fake.text(max_nb_chars=200)
                # Випадковий вибір користувача та статусу
                user_id = random.choice(user_ids)
                status_name = random.choice(statuses)
                status_id = status_dict[status_name]
                
                cur.execute(
                    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id)
                )
            
            conn.commit()
            print("Випадкові дані успішно додано до таблиць.")
    except Exception as error:
        if conn:
            conn.rollback()
        print("Помилка при наповненні таблиць даними:", error)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    seed_data()
