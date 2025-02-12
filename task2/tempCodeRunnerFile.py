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