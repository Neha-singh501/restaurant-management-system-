

import os
import json
import uuid
from validation.validate import get_foodname, get_price , get_category

class Menu_manage:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(BASE_DIR,"database","menu_items.json")

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"menu_item": []}

    # SAVE DATA 
    def save_data(self, data):

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    # NEXT ID

    def next_id(self, data):
        items = data["menu_item"]
        if not items:
            return "FD001"
        last_id = max(
        int(item["item_id"][2:])
        for item in items)

        return "FD" + str(last_id + 1).zfill(3)
        
    #  DISPLAY MENU

    def display_menu(self):
        while True:
            print("\n")
            print("-" * 30)
            print("        MENU MANAGEMENT")
            print("-" * 30)

            print("1. View All Items")
            print("2. Add New Items")
            print("3. Update Food Items")
            print("4. Delete Food Items")
            print("5. Exit")

            choice = input("\nEnter Your Choice: ").strip()

            if choice == "1":
                self.view_menu()
            elif choice == "2":
                self.add_item()
            elif choice == "3":
                self.update_menu_item()
            elif choice == "4":
                self.delete_menu_item()
            elif choice == "5":
                print("Exiting Menu Management...")
                return
            else:
                print("Invalid Choice!")

    # ---------------- ADD ITEM ----------------

    def add_item(self):

        data = self.load_data()
        food_name = get_foodname()
        for item in data["menu_item"]:
            if item["food_name"].strip().lower() == food_name.strip().lower():
                print("This Item is already added..")
                continue
        half_price = get_price()
        full_price = get_price()
        category = get_category()
        
        available_input = input("Is item available? (yes/no): ").strip().lower()

        if available_input == "yes":
            available = True

        elif available_input == "no":
            available = False

        else:
            print("Please enter yes or no.")
            return
        
        item = {
            "item_id": self.next_id(data),
            "food_name": food_name,
            "category" : category,
            "half_price": half_price,
            "full_price": full_price,
            "availability": available
        }

        data["menu_item"].append(item)

        self.save_data(data)

        print(f"'{food_name}' added to the menu at {full_price:.2f}.")

    # ---------------- VIEW MENU ----------------

    def view_menu(self, only_available=False):
        data = self.load_data()
        items = data["menu_item"]
        if only_available:
            items = [
                item
                for item in items
                if item["availability"]]
        if not items:
            print("\nMenu is empty.")
            return []

        
        print("                 ********************** ITEM'S VIEW *********************                    ")
        print("                               .............................                                ")

        print(f"{'ID':<10}{'Name':<25}{'Category':<25}{'half_price':<20}{'full_price':<20}{'Available':<10}")

        print("*" * 110)
        for item in items:
            status = "Yes" if item["availability"] else "No"
            print(
                f"{item['item_id']:<10}"
                f"{item['food_name']:<25}"
                f"{item['category']:<25}"
                f"{float(item['half_price']):<20.2f}"
                f"{float(item['full_price']):<20.2f}"
                f"{status:<20}"
            )
        print("-" * 110)
        return items


    # ---------------- UPDATE ITEM ----------------

    def update_menu_item(self):

        data = self.load_data()
        self.view_menu()
        while True:
            try:
                item_id = int(input("Enter Item ID: "))
            except ValueError:
                print("Invalid ID.")
                continue

            if item_id == 0 :
                return

            for item in data["menu_item"]:
                if item["item_id"] == item_id:
                    print("\nWhat do you want to change?")
                    print("1.Food Name")
                    print("2.Category")
                    print("3.Half Price")
                    print("4.Full Price")
                    print("5.Half & Full price")
                    print("6.Availability")
                    print("7.back")

                    choice = input("\nEnter your choice : ")

                    if choice == "1":
                        food_name = get_foodname()
                        if food_name:
                            item["food_name"] = food_name
                            print("Food Name update Successfully")

                    elif choice == "2":

                        category = get_category()
                        item["category"] = category
                        print("Category Updated Successfully")

                    elif choice == "3":

                        half_price = get_price()
                        item["half_price"] = half_price
                        print("Half Price updated successfully")

                    elif choice == "4":

                        full_price = get_price()
                        item["full_price"] = full_price
                        print("\nFull Price update successfully")

                    elif choice == "5":

                        half_price = get_price()
                        full_price = get_price()
                        item["half_price"] = half_price
                        item["full_price"] = full_price

                        print("\nHalf & Full Price update successfully")

                    elif choice == "6":
                        available_input = input("Is item available? (yes/no): ").strip().lower()
                        
                        if available_input == "yes":
                            item["availability"] = True
                        
                        elif available_input == "no":
                            item["availability"] = False
                        
                        else:
                            print("Please enter yes or no.")
                            return
                        print("\nAvailability update successfully")

                    elif choice == "7":
                        return

                    else:
                        print("Invalid Choice!...")
                        return

                    self.save_data(data)
                    print(f"Menu item {item_id} updated.")
                    return
            print("Menu item not found.")

    # ---------------- DELETE ITEM ----------------

    def delete_menu_item(self):

        data = self.load_data()
        self.view_menu()
        while True:
            try:
                item_id = int(input("Enter Item ID to delete: "))
            except ValueError:
                print("Invalid ID.")
                continue
            if item_id == 0:
                return
            for item in data["menu_item"] :
                if item["item_id"] == item_id:
                    confirm_id = input(f"delete '{item['food_name']} (yes/no) : ").strip().lower()
                    if confirm_id != "yes":
                        print("Deletion Cancelled.")
                        return
                    data["menu_item"].remove(item)
                    self.save_data(data)
                    print(f"Menu item {item_id} deleted.")
                    return

            print("Menu item not found.")

  