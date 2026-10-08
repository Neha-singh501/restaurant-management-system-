
import os
import json
import uuid
from datetime import datetime
from validation.validate import get_fullname
from logs.logger import log_info, log_warning, log_error


class OrderManagement:

    def __init__(self):

        BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(BASE_DIR,"database" , "orders.json")
        self.menu_path= os.path.join(BASE_DIR, "database" , "menu_items.json")
        self.booking_path = os.path.join(BASE_DIR, "database", "booking.json")

    def load_order(self):
        try:
            log_info("Loading order data")
            with open(self.file_path , "r") as file:
                data = json.load(file)
            log_info("Order Data loaded successfully")

        except (FileNotFoundError , json.JSONDecodeError):
            log_warning("File not found")
            return{"order" : []}

        if "order" not in data:
            log_warning("Order key not found in order")
            data["order"] = []

        return data

    def save_order(self, data):
            log_info("Saving order data")
            with open(self.file_path , "w") as file:
                json.dump(data,file, indent = 4)
            log_info("Saved order Successfully")

    def load_booking(self):
        try:
            log_info("Loading booking data")

            with open(self.booking_path, "r") as file:
                data = json.load(file)

            log_info("Booking data loading Successfully")

        except (FileNotFoundError , json.JSONDecodeError):
            log_warning("File Not Found")
            log_error("Json Data not found")
            return{"booking" :[]}
        
        if "booking" not in data:
            log_warning("Booking key not found")
            data["booking"] = []
        return data


    def load_menu(self):
        try:
            log_info("Load Menu data")
            with open(self.menu_path, "r") as file:
                return json.load(file).get("menu_item", [])
            log_info("Menu data load successfully")
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def generate_order_id(self,order):
        log_info("Generate new order Id")
        existing_id = {ord.get("order_id") for ord in order}

        while True:
            order_id = "ORD" + uuid.uuid4().hex[:6].upper()
            if order_id not in existing_id :
                log_info("unique id generate")
                return order_id
            

    def order_menu(self):
        while True:
            print("\n" + "="*30)
            print("          ORDER MANAGE ")
            print("="*30)
            print("\n1. Create New Order")
            print("2. View All Orders")
            print("3. Update Orders")
            print("4. Cancel Orders")
            print("5. Back")


            choice = input("Enter Choice : ").strip()

            if choice =="1":
                log_info("User selected create new order")
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

            booking_id = None
            table_id  = None

            print("\n1. Dine in")
            print("2. Takeway")

            choice = input("Enter Choice : ").strip()

            if choice == "1":
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

            elif choice == "2":
                customer_name =  get_fullname()
            else :
                print("Invalid Choice!..")
                return

#menu show
            menu = self.load_menu()

            if not menu :
                print("\n Menu is not available.")
                return

            print("\n" + "-"*90)

            print(f"{'item_id' : <10}{'name':<25}{'category': <20}{'half_price':<20}{'full_price':<20}")

            print("."*90)

            for item in menu:
                if item.get("availability"):
                    print(f"{item.get('item_id'):<10}{item.get('food_name'):<25}{item.get('category'):<20}{item.get('half_price'):<20}{item.get('full_price'):<20}")

            print("="*90)
            while True:
                try:
                    item_id = int(input("Enter Item ID : ").strip())
                except:
                    print("Please Enter Number")
                    continue

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
                try:
                    
                    quantity = int(input("Enter Quantity : ").strip())
                except:
                    print("Enter Number")
                    continue

                if quantity <=0:
                    print("Quantity must be 1")
                    continue

                print("\n -----select Size---- ")
                print("1.Half Size")
                print("2.Full Size")

                choice = input("Enter Size : ").strip()
                if choice == "1":
                    price = float(selected_item.get("half_price"))
                elif choice == "2":
                    price = float(selected_item.get("full_price"))
                else:
                    print("Invalid Choice")
                    return

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
            log_warning("Order not found")
            print("\nOrder not found")
            return

        print("\n" + "="*105)
        print("                                                   ORDER LIST")
        print("" + "="*105)
        print(f"{'Order ID' :<14}{'booking_id' :<15}{'Customer Name' :<20}{'Table No' :<10}{'Total Amount' :<20}{'Status' :<15}{'Created At' :<20}")

        print("="*105)

        for order in orders:
            booking_id = order.get("booking_id") or "-"
            table_id = order.get("table_id") or "Takeway"
            print(f"{order.get('order_id') :<14}"
                  f"{booking_id :<15}"
                  f"{order.get('customer_name') :<20}"
                  f"{table_id:<10}"
                  f"{order.get('total_amount') :<15}"
                  f"{order.get('order_status') :<15}"
                  f"{order.get('created_at') :<20}")
        print("."*105)

    def update_order(self):
        data = self.load_order()
        orders = data["order"]
        if not orders:
            log_warning("Order Not found")
            print("Order not found")
            return
        
        self.view_orders()

        while True:
            order_id = input("\nEnter Order ID to Update : ").strip().upper()
            if order_id == "0":
                return

            found_order = None
            for order in orders:
                if order.get("order_id") == order_id:
                    found_order  = order
                    break
            if found_order is None:
                    print("\nOrder ID not found")
                    continue
            break
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
            return

        found_order["order_status"] = new_status
        self.save_order(data)
        print(f"Order : {order_id} updated : {current_status} {new_status}")


    def cancel_order(self):

        data = self.load_order()
        orders = data["order"]
        if not orders:
            print("Order not found")
            return
        self.view_orders()
        while True:
            order_id = input("Enter Order ID to cancel : ").strip().upper()
            if order_id == "0":
                return

            found_order = None
            for order in orders:
                if order.get("order_id") == order_id:
                    found_order = order
                    break
            if found_order is None:
                print("\nOrder ID not found")
                continue
            break

        current_status = found_order.get("order_status")

        if current_status == "cancelled":
            print("This order is already cancelled")
            return
        if current_status == "completed":
            print("Order can't be cancelled it is already complete.")
            return
        if current_status == "served":
            print("Order can't be cancelled it's already served.") 
            return

        confirm_cancel = input("Are you sure you want to cancel?(yes/no) ").strip().lower()
        if confirm_cancel != "yes":
            print("Can't be cancel")
            return

        found_order["order_status"] = "cancelled"
        self.save_order(data)

        print("Order Cancelled Successful!...")








    
            
            
            

        
            

