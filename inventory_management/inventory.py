import json
import os


class Inventory_Manage:

    def __init__(self):
        self.inventory_file = "database/inventory.json"
        self.reorder_level = 10 

    def load_inventory(self):
    
        if not os.path.exists(self.inventory_file):
            return []
        try:
            with open(self.inventory_file, "r") as file:
                data = json.load(file)
            return data["inventory"]
        except:
            return []

    def save_inventory(self, items):
        with open(self.inventory_file, "w") as file:
            json.dump({"inventory": items}, file, indent=4)

 
    def get_quantity(self, message):
    
        while True:
            qty = input(message)
            if qty.isdigit() and int(qty) > 0:
                return int(qty)
            print("Invalid quantity ")

    def get_price(self):
        while True:
            price = input("Price: ")
            if price.replace(".", "", 1).isdigit() and float(price) > 0:
                return float(price)
            print(" Invalid price ")

    def get_text(self, message):
    
        while True:
            text = input(message).strip()
            if text.replace(" ", "").isalpha():
                return text
            print("Enter only letter")

   
    def show_items(self, items):
        print("\nID      | Name        | Category      | Quantity | Unit | Price")
        print("-------------------------------------------------------------")
        for item in items:
            print(item["id"], "|", item["name"], "|", item["category"], "|",
                  item["quantity"], "|", item["unit"], "|", item["price"])

    def select_item(self, items):
      
        if len(items) == 0:
            print("Inventory is empty")
            return None

        self.show_items(items)
        item_id = input("\nEnter Item ID: ").upper()

        for item in items:
            if item["id"] == item_id:
                return item

        print("Error: Item nahi mila")
        return None

    # ---------- 1. View Inventory ----------
    def view_inventory(self):
        items = self.load_inventory()
        if len(items) == 0:
            print("Inventory khaali hai")
        else:
            self.show_items(items)

    # ---------- 2. Add Stock ----------
    def add_stock(self):
        items = self.load_inventory()
        item = self.select_item(items)
        if item == None:
            return

        qty = self.get_quantity("Enter quantity to add: ")

        item["quantity"] = item["quantity"] + qty
        self.save_inventory(items)
        print("Success: Stock updated. Naya stock:", item["quantity"], item["unit"])

    # ---------- 3. Remove Stock ----------
    def remove_stock(self):
        items = self.load_inventory()
        item = self.select_item(items)
        if item == None:
            return

        while True:
            qty = self.get_quantity("Enter quantity to remove: ")
            if qty <= item["quantity"]:
                break
            print("Error: Not enough stock. Available:", item["quantity"])

        item["quantity"] = item["quantity"] - qty
        self.save_inventory(items)
        print("Success: Stock removed. Bacha hua stock:", item["quantity"], item["unit"])

    # ---------- 4. Manage Inventory ----------
    def new_item_id(self, items):
        # sabse bada number dhoondho, usme 1 jodo -> FD001, FD002 ...
        biggest = 0
        for item in items:
            number = int(item["id"][2:])
            if number > biggest:
                biggest = number
        return "FD" + str(biggest + 1).zfill(3)

    def manage_inventory(self):
        items = self.load_inventory()

        # Select Category: pehle se maujood categories dikhao
        categories = []
        for item in items:
            if item["category"] not in categories:
                categories.append(item["category"])

        print("\nAvailable Categories:", categories)
        category = input("Enter Category: ").strip()
        if category == "":
            print("Error: Category khaali nahi ho sakti")
            return

        # Choose Action
        print("\n1. Add Item")
        print("2. Update Item")
        print("3. Delete Item")
        action = input("Choose action: ")

        # is category ke items nikalo
        category_items = []
        for item in items:
            if item["category"] == category:
                category_items.append(item)

        if action == "1":
            name = self.get_text("Item name: ")
            quantity = self.get_quantity("Quantity: ")
            unit = self.get_text("Unit (Kg/Ltr/Pcs): ")
            price = self.get_price()

            new_item = {
                "id": self.new_item_id(items),
                "name": name,
                "category": category,
                "quantity": quantity,
                "unit": unit,
                "price": price
            }
            items.append(new_item)
            self.save_inventory(items)
            print("Success: Item added. ID:", new_item["id"])

        elif action == "2":
            item = self.select_item(category_items)
            if item == None:
                return

            print("Naye details daalo:")
            item["name"] = self.get_text("Item name: ")
            item["quantity"] = self.get_quantity("Quantity: ")
            item["unit"] = self.get_text("Unit (Kg/Ltr/Pcs): ")
            item["price"] = self.get_price()

            self.save_inventory(items)
            print("Success: Item updated")

        elif action == "3":
            item = self.select_item(category_items)
            if item == None:
                return

            confirm = input("Kya aap sach me delete karna chahte ho? (y/n): ").lower()
            if confirm == "y":
                items.remove(item)
                self.save_inventory(items)
                print("Success: Item deleted")
            else:
                print("Delete cancel ho gaya")

        else:
            print("Error: Galat option")

    # ---------- 5. Low Stock Alert ----------
    def low_stock_alert(self):
        items = self.load_inventory()
        found = False

        print("\n---------- LOW STOCK ALERT ----------")
        for item in items:
            if item["quantity"] <= self.reorder_level:
                print(item["name"], "- sirf", item["quantity"], item["unit"], "bacha hai")
                found = True

        if found == False:
            print("Sab items ka stock theek hai")

    # ---------- Inventory Menu ----------
    def inventory_menu(self):
        while True:
            print("\n===== INVENTORY MENU =====")
            print("1. View Inventory")
            print("2. Add Stock")
            print("3. Remove Stock")
            print("4. Manage Inventory")
            print("5. Low Stock Alert")
            print("6. Back")
            choice = input("Choose an option: ")

            if choice == "1":
                self.view_inventory()
            elif choice == "2":
                self.add_stock()
            elif choice == "3":
                self.remove_stock()
            elif choice == "4":
                self.manage_inventory()
            elif choice == "5":
                self.low_stock_alert()
            elif choice == "6":
                break
            else:
                print("Galat option, dobara try karo")


# Ye file seedha run karo to menu chalega.
# Dashboard se import karoge to apne aap nahi chalega.
if __name__ == "__main__":
    inventory = Inventory_Manage()
    inventory.inventory_menu()