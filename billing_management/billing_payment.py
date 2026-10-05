
import os
import json
import uuid
from datetime import datetime


class BillManagement:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bill_path = os.path.join(BASE_DIR, "database", "bill.json")
        self.order_path = os.path.join(BASE_DIR, "database", "orders.json")


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
            print("." * 30)
            print("\n1. Generate Bill")
            print("2. Back")

            choice = input("Enter Choice : ").strip()

            if choice == "1":
                self.generate_bill()
            elif choice == "2":
                return
            else:
                print("Invalid Choice!...")


    def generate_bill(self):

        order_data = self.load_order()
        orders = order_data["order"]

        if not orders:
            print("\nOrder not found")
            return

        order_id = input("\nEnter Order ID : ").strip().upper()

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
            print("Cancelled order ka bill nahi ban sakta.")
            return

        if status not in ["served", "completed"]:
            print(f"Bill abhi nahi ban sakta, order status : {status}")
            return

        # Step 3: pehle se bill to nahi bana
        bill_data = self.load_bill()
        bills = bill_data["bill"]

        for b in bills:
            if b.get("order_id") == order_id:
                print(f"Is order ka bill pehle se ban chuka hai : {b.get('bill_id')}")
                return

        # Step 4: hisaab
        subtotal = found_order.get("total_amount")
        gst = round(subtotal * 0.05, 2)       # 5% GST
        grand_total = round(subtotal + gst, 2)

        # Step 5: payment method
        print("\n1. Cash")
        print("2. UPI")
        print("3. Card")

        pay_choice = input("Select Payment Method : ").strip()

        if pay_choice == "1":
            payment_method = "cash"
        elif pay_choice == "2":
            payment_method = "upi"
        elif pay_choice == "3":
            payment_method = "card"
        else:
            print("Invalid Choice!...")
            return

        # Step 6: bill save
        new_bill = {
            "bill_id": self.generate_bill_id(bills),
            "order_id": order_id,
            "customer_name": found_order.get("customer_name"),
            "table_id": found_order.get("table_id"),
            "subtotal": subtotal,
            "gst": gst,
            "grand_total": grand_total,
            "payment_method": payment_method,
            "payment_status": "paid",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        bills.append(new_bill)
        self.save_bill(bill_data)

        # Step 7: order ko completed karo
        found_order["order_status"] = "completed"
        self.save_order(order_data)

        # Step 8: print
        self.print_bill(new_bill, found_order)

    # ---------------- PRINT BILL ----------------

    def print_bill(self, bill, order):

        print("\n" + "=" * 50)
        print("                  RESTAURANT BILL")
        print("=" * 50)

        print(f"Bill ID  : {bill['bill_id']}")
        print(f"Order ID : {bill['order_id']}")
        print(f"Customer Name: {bill['customer_name']}")
        print(f"Table No : {bill['table_id']}")
        print(f"Date     : {bill['created_at']}")

        print("-" * 50)
        print(f"{'Item':<22}{'Quantity':<6}{'Price':<10}{'Total':<10}")
        print("-" * 50)

        for item in order["menu_items"]:
            print(f"{item['food_name']:<22}{item['quantity']:<6}{item['price']:<10}{item['subtotal']:<10}")

        print("-" * 50)
        print(f"{'Subtotal':<38}{bill['subtotal']:>10.2f}")
        print(f"{'GST (5%)':<38}{bill['gst']:>10.2f}")
        print(f"{'Grand Total':<38}{bill['grand_total']:>10.2f}")
        print("-" * 50)
        print(f"Payment : {bill['payment_method']} ({bill['payment_status']})")
        print("=" * 50)
        print("          Thank You! Visit Again")
        print("=" * 50) 




