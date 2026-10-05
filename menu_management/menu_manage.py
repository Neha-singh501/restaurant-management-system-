

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
            return 1
        return max(item["item_id"] for item in items) + 1

    #  DISPLAY MENU

    def display_menu(self):
        while True:
            print("\n")
            print("-" * 30)
            print("        MENU MANAGEMENT")
            print("-" * 30)

            print("1. View All Items")
            print("2. Add New Items")
            print("3. Search Food Items")
            print("4. Update Food Items")
            print("5. Delete Food Items")
            print("6. Update Availability")
            print("7. Exit")

            choice = input("\nEnter Your Choice: ").strip()

            if choice == "1":
                self.view_menu()
            elif choice == "2":
                self.add_item()
            elif choice == "3":
                self.search_item()
            elif choice == "4":
                self.update_menu_item()
            elif choice == "5":
                self.delete_menu_item()
            elif choice == "6":
                self.update_availability()
            elif choice == "7":
                print("Exiting Menu Management...")
                return
            else:
                print("Invalid Choice!")

    # ---------------- ADD ITEM ----------------

    def add_item(self):

        data = self.load_data()
        food_name = get_foodname()
        price = get_price()
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
            "price": price,
            "availability": available
        }

        data["menu_item"].append(item)

        self.save_data(data)

        print(f"'{food_name}' added to the menu at {price:.2f}.")

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

        print("\n" + "-" * 82)
        print("                         MENU")
        print("-" * 82)

        print(f"{'ID':<5}{'Name':<25}{'Category':<30}{'Price':<12}{'Available':<10}")

        print("-" * 90)
        for item in items:
            status = "Yes" if item["availability"] else "No"
            print(
                f"{item['item_id']:<5}"
                f"{item['food_name']:<25}"
                f"{item['category']:<25}"
                f"{float(item['price']):<11.2f}"
                f"{status:<10}"
            )
        print("-" * 65)
        return items

    # ---------------- SEARCH ITEM ----------------

    def search_item(self):
        data = self.load_data()
        search = input("Enter food name to search: ").strip().lower()
        found = []
        for item in data["menu_item"]:
            if search in item["food_name"].lower():
                found.append(item)
        if not found:
            print("Menu item not found.")
            return
        print("\nSearch Result:")
        for item in found:
            status = ("Available"if item["availability"]else "Not Available")
            print(
                f"ID: {item['item_id']} | "
                f"Name: {item['food_name']} | "
                f"Price: ₹{item['price']:.2f} | "
                f"Status: {status}"
            )

    # ---------------- UPDATE ITEM ----------------

    def update_menu_item(self):
        data = self.load_data()
        try:
            item_id = int(input("Enter Item ID: "))
        except ValueError:
            print("Invalid ID.")
            return
        for item in data["menu_item"]:
            if item["item_id"] == item_id:
                print("\nLeave input empty if you don't want to change it.")
                food_name = input("Enter New Name: ").strip()
                price = input("Enter New Price: ").strip()
                if food_name:
                    item["food_name"] = food_name.title()
                if price:
                    try:
                        price = float(price)
                        if price <= 0:
                            print("Price must be greater than 0.")
                            return
                        item["price"] = price
                    except ValueError:
                        print("Invalid price.")
                        return
                self.save_data(data)
                print(f"Menu item {item_id} updated.")
                return
        print("Menu item not found.")

    # ---------------- DELETE ITEM ----------------

    def delete_menu_item(self):
        data = self.load_data()
        try:
            item_id = int(input("Enter Item ID to delete: "))
        except ValueError:
            print("Invalid ID.")
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

    # ---------------- UPDATE AVAILABILITY ----------------

    def update_availability(self):
        data = self.load_data()
        try:
            item_id = int(input("Enter Item ID: "))
        except ValueError:
            print("Invalid ID.")
            return
        for item in data["menu_item"]:
            if item["item_id"] == item_id:
                choice = input("Available? (yes/no): ").strip().lower()
                if choice == "yes":
                    item["availability"] = True
                elif choice == "no":
                    item["availability"] = False
                else:
                    print("Please enter yes or no.")
                    return
                self.save_data(data)
                print(f"Availability of "f"{item['food_name']} updated.")
                return
        print("Menu item not found.")