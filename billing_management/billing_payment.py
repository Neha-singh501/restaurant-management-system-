
import os
import json
import uuid
from datetime import datetime


class BillManagement:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bill_path = os.path.join(BASE_DIR, "database", "bill.json")
        self.order_path = os.path.join(BASE_DIR, "database", "orders.json")
        self.payment_path = os.path.join(BASE_DIR,"database","payment.json")


    def load_bill(self):
        try:
            with open(self.bill_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"bill": []}

        if "bill" not in data:
            data["bill"] = []

        return data

    def save_bill(self, data):
        with open(self.bill_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_order(self):
        try:
            with open(self.order_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"order": []}

        if "order" not in data:
            data["order"] = []

        return data

    def save_order(self, data):
        with open(self.order_path, "w") as file:
            json.dump(data, file, indent=4)


    def generate_bill_id(self, bills):
        existing_ids = [b.get("bill_id") for b in bills]

        while True:
            bill_id = "BILL" + uuid.uuid4().hex[:6].upper()
            if bill_id not in existing_ids:
                return bill_id


    def billing_menu(self):
        while True:
            print("\n" + "=" * 30)
            print("          BILLING")
            print("=" * 30)
            print("\n1. Generate Bill")
            print("2. View Bill")
            print("3. process payment")
            print("4. Back")

            choice = input("Enter Choice : ").strip()

            if choice == "1":
                self.generate_bill()
            elif choice == "2":
                self.view_bill()
            elif choice == "3":
                pass
            elif choice == "4":
                return
            else:
                print("Invalid Choice!...")

    def generate_bill(self):

        order_data = self.load_order()
        orders = order_data["order"]

        if not orders:
            print("\nOrder not found")
            return
        
        while True:
            order_id = input("\nEnter Order ID : ").strip().upper()

            if not order_id:
                print("Order ID can't be empty")
            else:
                break 

        found_order = None

        for order in orders:
            if order.get("order_id") == order_id:
                found_order = order
                break

        if found_order is None:
            print("\nOrder ID not found.")
            return

        status = found_order.get("order_status")

        if status == "cancelled":
            print("Bill cannot be generated bcz the order has been cancelled..")
            return
        
        if status != "served":
            print("Bill can't be generate bcz the order hasn't been served yet.")
            return

        bill_data = self.load_bill()
        bills = bill_data["bill"]

        for b in bills:
            if b.get("order_id") == order_id:
                print(f"Bill already generated.: {b.get('bill_id')}")
                return

        menu_items = found_order.get("menu_items",[])
        if not menu_items:
            print("\nCan't generate bill bcz no menu item were found.")
            return

        subtotal = 0

        for item in menu_items:
            try:
                item_subtotal = float(item.get("subtotal"))
            except:
                print("Invalid subtotal found in order")
                return

            if item_subtotal < 0:
                print("\nInvalid subtotal found in order")
                return

            subtotal += item_subtotal 

        while True:
                try:
                    discount_percent = float(input("\nEnter Discount : ").strip())
                    if discount_percent < 0 :
                        print("Discount Must be btwn 1 to 100 ")
                        continue
                    if discount_percent > 100:
                        print("Discount must be btwn 1 to 100")
                        continue
                    break
                except:
                    print("Invalid Discount")
                
        discount = subtotal * discount_percent /100
        after_discount = subtotal - discount

        tax_percent = 5
        tax = after_discount * tax_percent/100

        grand_total = after_discount + tax


        bill_id = self.generate_bill_id(bills)
        bill = {
                "bill_id" : bill_id,
                "order_id" : order_id,
                "booking_id" : found_order.get("booking_id"),
                "customer_name" :found_order.get("customer_name"),
                "table_id": found_order.get("table_id"),
                "menu_items" : menu_items,
                "subtotal": subtotal,
                "discount_percent": discount_percent,
                "discount" : discount,
                "tax_percent" : tax_percent,
                "tax" : tax,
                "grand_total" : grand_total,
                "payment_status" : "pending",
                "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M ")
             }

        bills.append(bill)
        self.save_bill(bill_data)

        print("\nBill Generated Successfully")

        print("*"*50)
        print("\n")
        print(f"BILL ID : {bill_id}")
        print(f"customer_name : {found_order.get("customer_name")}")
        print(f"SubTotal : {subtotal:.2f}")
        print(f"Discount : {discount:.2f}")
        print(f"Tax ({tax_percent}%) : {tax:.2f}")
        print(f"Grand Total : {grand_total:.2f}")
        # print(f"Payment Status" : "pending")


    def view_bill(self):
        bill_data = self.load_bill()
        bills = bill_data.get("bill")

        if not bills:
            print("No Bill Found")
            return

        bill_id = input("Enter Bill ID : ").strip()

        found_bill = None

        for bill in bills:
            if bill.get("bill_id") == bill_id:
                found_bill = bill
                break
        if found_bill is None:
            print("Bill ID not Found")
            return
        table = found_bill.get("table_id")
        if table is None:
            table = "Takeaway"

        print("\n" + "*" * 50)
        print("                 DISPLAY BILL ")
        print("*" * 50)

        print(f"Bill ID   : {found_bill.get('bill_id')}")
        print(f"Order ID  : {found_bill.get('order_id')}")
        print(f"Customer  : {found_bill.get('customer_name')}")
        print(f"Table     : {table}")
        print(f"Date      : {found_bill.get('created_at')}")

        print("-" * 50)
        print(f"{'Item':<22}{'Qty':<6}{'Price':<10}{'Subtotal':<10}")
        print("-" * 50)

        for item in found_bill.get("menu_items", []):
            print(f"{item.get('food_name'):<22}"
                  f"{item.get('quantity'):<6}"
                  f"{item.get('price'):<10}"
                  f"{item.get('subtotal'):<10}")

        print("-" * 50)
        print(f"SubTotal          : {found_bill.get('subtotal'):.2f}")
        print(f"Discount ({found_bill.get('discount_percent')}%)     : {found_bill.get('discount'):.2f}")
        print(f"Tax ({found_bill.get('tax_percent')}%)          : {found_bill.get('tax'):.2f}")
        print(f"Grand Total       : {found_bill.get('grand_total'):.2f}")
        print("*" * 50)


    def load_payment(self):
        try:
            with open(self.payment_path,"r") as file:
                data = json.load(file)
        except:
            return{"payment" : []}
        if "payment" not in data:
            data["payment"] =[]

        return data

    def save_payment(self,data):
            with open(self.payment_path,"w") as file:
                json.dump(data,file,indent = 4)

    def process_payment(self):

        bill_data = self.load_bill()
        bills = bill_data["bill"]

        if not bills:
            print("\nNo Bill Found")
            return
        
        pending_bill = []

        for bill in bills:
            if bill.get("payment_status") =="pending":
                pending_bill.append(bill)

        if not pending_bill:
            print("There are currently no pending bills.")
            return

        print("\n------ Pending Bills------\n")
        print(f"{'Bill_id':<12}{'customer_name' :<20}{'subtotal':<10}")
        print("-"*50)

        for bill in pending_bill:
            print(f"{bill.get('bill_id'):<12}"
                  f"{bill.get('customer_name') :<20}"
                  f"{bill.get('grand_total') :<10.2f}")

        found_bill = None

        while True:
            bill_id = input("Enter Bill ID : ").strip().upper()

            for bill in pending_bill:
                if bill.get("bill_id") == bill_id:
                    found_bill = bill
                    break

            if not found_bill:
                break
            print("\nInvalid Bill ID ")

        total = found_bill.get("grand_total")
        print(f"\nAmount to Pay : {total:.2f}")
        while True:
                    
            print("\n1. Cash")
            print("2. UPI")
            print("3. Card")

            choice = input("Enter Your Choice : ").strip()

            if choice == "1":
                method = "cash"
                


        



            

    
    





