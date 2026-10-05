
import os
import json
import uuid
from datetime import datetime


class OrderManagement:

    def __init__(self):

        BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(BASE_DIR,"database" , "orders.json")
        self.menu_path= os.path.join(BASE_DIR, "database" , "menu_items.json")
        self.booking_path = os.path.join(BASE_DIR, "database", "booking.json")

    def load_order(self):
        try:
            with open(self.file_path , "r") as file:
                data = json.load(file)

        except (FileNotFoundError , json.JSONDecodeError):
            return{"order" : []}

        if "order" not in data:
            data["order"] = []

        return data

    def save_order(self, data):
            with open(self.file_path , "w") as file:
                json.dump(data,file, indent = 4)

    def load_booking(self):
        try:
            with open(self.booking_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError , json.JSONDecodeError):
            return{"booking" :[]}
        if "booking" not in data:
            data["booking"] = []
        return data


    def load_menu(self):
        try:
            with open(self.menu_path, "r") as file:
                return json.load(file).get("menu_item", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # def find_menu_item(self, menu, item_id):
    #     for item in menu:
    #         if item.get("item_id") == item_id:
    #             return item
    #     return None

    def generate_order_id(self,order):

        existing_id = {ord.get("order_id") for ord in order}

        while True:
            order_id = "ORD" + uuid.uuid4().hex[:6].upper()
            if order_id not in existing_id :
                return order_id


 
    def order_menu(self):
        while True:
            print("\n" + "="*30)
            print("          ORDER MANAGE ")
            print("."*30)
            print("\n1. Create New Order")
            print("2. View All Orders")
            print("3. Update Orders")
            print("4. Cancel Orders")
            print("5. Back")


            choice = input("Enter Choice : ").strip()

            if choice =="1":
                self.create_order()
            elif choice == "2":
              self.view_orders()
            elif choice == "3":
                self.update_order()
            elif choice == "4":
                self.cancel_order()
            elif choice == "5":
                return
            else:
                print("Invalid Choice!...")

    def create_order(self):
            order_items = []
           
            booking_data = self.load_booking()
           
            bookings = booking_data["booking"]

            if not bookings:
                print("\n Booking Not Found.")
                return

            booking_id = input("Enter Booking ID : ").strip().upper()

            found_booking = None

            for booking in bookings:
                if booking.get("booking_id") == booking_id:
                    found_booking = booking
                    break
            if found_booking is None:
                print("\nBooking ID not Found.")
                return
#status check

            if found_booking.get("status") != "occupied":

                print("\n Order can't be created because the table is not currently occupied.")
                return

            customer_name = found_booking.get("customer_name")
            table_id = found_booking.get("table_id")

            # print("\n" + "."*50)
            # print("         CREATE ORDER")
            # print("."*50)

            # print(f"customer Name : {customer_name}")
            # print(f"Table No : {table_id}")
            # print(f"Booking ID : {booking_id}")
#menu show
            menu = self.load_menu()

            if not menu :
                print("\n Menu is not available.")
                return

            print("\n" + "-"*80)

            print(f"{'item_id' : <10}{'name':<25}{'category': <20}{'price':<20}")

            print("."*70)

            for item in menu:
                if item.get("availability"):
                    print(f"{item.get('item_id') : <10}{item.get('food_name') : <25}{item.get('category') : <20}{item.get('price') : <10}")

            print("="*70)
            while True:

                item_id = int(input("Enter Item ID : ").strip())
                selected_item = None
                for item in menu:
                    if item.get("item_id") == item_id:
                        selected_item = item
                        break
                if selected_item is None :
                    print("Invalid Item ID")
                    continue

                if not selected_item.get("availability"):
                    print("This Item is not available")
                    continue

                quantity = int(input("Enter Quantity : ").strip())

                price = float(selected_item.get("price"))
                subtotal = price*quantity

                order_items.append({
                    "item_id": item_id,
                    "food_name": selected_item.get("food_name"),
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal
                })

                more = input("Do you want to add another item? (yes/no): ").strip().lower()

                if more != "yes":
                    break

            total_amount = sum(item["subtotal"] for item in order_items)

            order_data = self.load_order()
            orders = order_data["order"]

            new_order = {
                "order_id": self.generate_order_id(orders),
                "booking_id" : booking_id,
                "customer_name": customer_name,
                "table_id": table_id,
                "menu_items": order_items,
                "total_amount": total_amount,
                "order_status": "pending",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            orders.append(new_order)
            self.save_order(order_data)


            print("."*50)
            print("         ORDER CREATED")
            print("."*50)

            print(f"Order ID : {new_order['order_id']}")
            print(f"Customer Name : {customer_name}")
            print(f"Table No : {table_id}")
            print(f"Total Amount : {total_amount : .2f}")
            print(f"Status : {new_order['order_status']}")

            print("="*50)


    def view_orders(self):

        data = self.load_order()
        orders = data["order"]

        if not orders:
            print("\nOrder not found")
            return

        print("\n" + "="*50)
        print("                 ORDER LIST")
        print("\n" + "="*100)
        print(f"{'Order ID' :<14}{'booking_id' :<15}{'Customer Name' :<20}{'Table No' :<10}{'Total Amount' :<12}{'Status' :<15}{'Created At' :<20}")

        print("."*100)

        for order in orders:
            print(f"{order.get('order_id') :<14}"
                  f"{order.get('booking_id') :<15}"
                  f"{order.get('customer_name') :<20}"
                  f"{order.get('table_id') :<10}"
                  f"{order.get('total_amount') :<12}"
                  f"{order.get('order_status') :<15}"
                  f"{order.get('created_at') :<20}")
            print("="*100)


    def update_order(self):
        data = self.load_order()
        orders = data["order"]

        if not orders:
            print("Order not found")
            return

        order_id = input("\nEnter Order ID to Update : ").strip().upper()

        found_order = None
        for order in orders:
            if order.get("order_id") == order_id:
                found_order  = order
                break
        if found_order is None:
                print("\nOrder ID not found")
                return
        current_status = found_order.get("order_status")

        if current_status in ["completed","cancelled"]:
            print("This order can't be update.")
            return
        print("\n1. Preparing")
        print("2. Served")
        print("3. Completed")
        print("4. Back")

        choice = input("Select New Status : ").strip()

        if choice == "1":
            new_status = "preparing"
        elif choice == "2":
            new_status = "served"
        elif choice == "3":
            new_status = "completed"
        elif choice == "4":
            return
        else :
            print("Invalid Choice!..\n")

        found_order["order_status"] = new_status
        self.save_order(data)
        print(f"Order : {order_id} updated : {current_status} {new_status}")


    def cancel_order(self):

        data = self.load_order()
        orders = data["order"]
        if not orders:
            print("Order not found")
            return

        order_id = input("Emter Order ID to cancel : ").strip().upper()

        found_order = None

        for order in orders:
            if order.get("order_id") == order_id:
                found_order = order
                break
        if found_order is None:
            print("\nOrder ID not found")
            return

        current_status = found_order.get("order_status")

        if current_status == "cancelled":
            print("This order is already cancelled")
            return
        if current_status == "completed":
            print("Order can't be cancelled it is already complete.")
            return
        if current_status == "served":
            print("Order cant br cancelled it's already served.") 
            return

        confirm_cancel = input("Are you sure you want to cancel?(yes/no) ").strip()
        if confirm_cancel != "yes":
            print("Can't be cancel")
            return

        found_order["order_status"] = "cancelled"
        self.save_order(data)

        print("Order Cancelled Successful!...")








    
            
            
            

        
            

