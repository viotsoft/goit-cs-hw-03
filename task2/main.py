import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

def connect_to_mongodb(uri="mongodb://localhost:27017/", db_name="catsdb", collection_name="cats"):
    """
    Подключается к MongoDB и возвращает объект коллекции.
    """
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        print("Підключення до MongoDB встановлено.")
        return collection
    except Exception as e:
        print("Помилка підключення до MongoDB:", e)
        return None

def create_cat(collection, name, age, features):
    """
    Добавляет нового кота в коллекцию.
    """
    try:
        # Проверим, чтобы возраст не был отрицательным
        if age < 0:
            print("Вік кота не може бути від'ємним.")
            return
        
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Додано кота з id: {result.inserted_id}")
    except Exception as e:
        print("Помилка створення кота:", e)

def get_all_records(collection):
    """
    Выводит все записи из коллекции.
    """
    try:
        cats = collection.find()
        print("\nВсі записи:")
        empty = True
        for cat in cats:
            print(cat)
            empty = False
        if empty:
            print("Колекція порожня.")
    except Exception as e:
        print("Помилка читання записів:", e)

def get_cat_by_name(collection, name):
    """
    Находит и выводит информацию о коте по имени.
    """
    if not name.strip():
        print("Ім'я кота не може бути порожнім.")
        return

    try:
        cat = collection.find_one({"name": name})
        if cat:
            print("\nІнформація про кота:")
            print(cat)
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print("Помилка пошуку кота:", e)

def update_cat_age(collection, name, new_age):
    """
    Обновляет возраст кота по имени.
    """
    if not name.strip():
        print("Ім'я кота не може бути порожнім.")
        return
    
    # Проверка возраста
    if new_age < 0:
        print("Вік кота не може бути від'ємним.")
        return

    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Оновлено вік кота з ім'ям '{name}'.")
        else:
            # Если кот не найден или возраст совпал с предыдущим
            cat_exists = collection.find_one({"name": name})
            if not cat_exists:
                print("Кота з таким ім'ям не знайдено.")
            else:
                print("Дані не змінено (вік залишився таким самим).")
    except Exception as e:
        print("Помилка оновлення віку кота:", e)

def add_feature_to_cat(collection, name, feature):
    """
    Добавляет новую характеристику в список features кота по имени.
    """
    if not name.strip():
        print("Ім'я кота не може бути порожнім.")
        return

    if not feature.strip():
        print("Характеристика не може бути порожньою.")
        return

    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print(f"Додано нову характеристику для кота '{name}'.")
        else:
            # Либо кот не найден, либо такая характеристика уже есть
            cat_exists = collection.find_one({"name": name})
            if not cat_exists:
                print("Кота з таким ім'ям не знайдено.")
            else:
                print("Характеристика не додана (можливо, вона вже існує).")
    except Exception as e:
        print("Помилка додавання характеристики:", e)

def delete_cat_by_name(collection, name):
    """
    Удаляет запись кота по имени.
    """
    if not name.strip():
        print("Ім'я кота не може бути порожнім.")
        return

    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Видалено кота з ім'ям '{name}'.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print("Помилка видалення кота:", e)

def delete_all_records(collection):
    """
    Удаляет все записи из коллекции.
    """
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except Exception as e:
        print("Помилка видалення всіх записів:", e)

def menu():
    """
    Выводит меню операций.
    """
    print("\nВиберіть операцію:")
    print("1. Вивести всі записи")
    print("2. Знайти кота за ім'ям")
    print("3. Додати нового кота")
    print("4. Оновити вік кота за ім'ям")
    print("5. Додати характеристику кота за ім'ям")
    print("6. Видалити кота за ім'ям")
    print("7. Видалити всі записи")
    print("0. Вийти")

def main():
    # Подключение к MongoDB
    collection = connect_to_mongodb()
    if collection is None:
        return  # Если не удалось подключиться, завершаем программу
    
    while True:
        menu()
        choice = input("Ваш вибір: ")
        
        if choice == "1":
            get_all_records(collection)

        elif choice == "2":
            name = input("Введіть ім'я кота: ").strip()
            if not name:
                print("Ім'я кота не може бути порожнім.")
                continue
            get_cat_by_name(collection, name)

        elif choice == "3":
            name = input("Введіть ім'я кота: ").strip()
            if not name:
                print("Ім'я кота не може бути порожнім.")
                continue
            try:
                age = int(input("Введіть вік кота: "))
            except ValueError:
                print("Вік має бути числом!")
                continue
            features_input = input("Введіть характеристики (через кому): ")
            features = [feat.strip() for feat in features_input.split(',') if feat.strip()]
            create_cat(collection, name, age, features)

        elif choice == "4":
            name = input("Введіть ім'я кота: ").strip()
            if not name:
                print("Ім'я кота не може бути порожнім.")
                continue
            cat_exists = collection.find_one({"name": name})
            if not cat_exists:
                print("Кота з таким ім'ям не знайдено.")
                continue
            try:
                new_age = int(input("Введіть новий вік: "))
            except ValueError:
                print("Вік має бути числом!")
                continue
            update_cat_age(collection, name, new_age)

        elif choice == "5":
            name = input("Введіть ім'я кота: ").strip()
            if not name:
                print("Ім'я кота не може бути порожнім.")
                continue
            feature = input("Введіть нову характеристику: ").strip()
            if not feature:
                print("Характеристика не може бути порожньою.")
                continue
            add_feature_to_cat(collection, name, feature)

        elif choice == "6":
            name = input("Введіть ім'я кота для видалення: ").strip()
            if not name:
                print("Ім'я кота не може бути порожнім.")
                continue
            delete_cat_by_name(collection, name)

        elif choice == "7":
            confirm = input("Ви впевнені, що хочете видалити всі записи? (так/ні): ")
            if confirm.lower() == "так":
                delete_all_records(collection)
            else:
                print("Відміна видалення.")

        elif choice == "0":
            print("Вихід із програми.")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
