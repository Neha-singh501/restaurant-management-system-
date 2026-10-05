
from menu_management.menu_manage import Menu_manage
from staff_management.staff_manage import register_staff
from booking_management.booking_table import BookingTable
from order_management.order_manage import OrderManagement
# from billing_management.billing_payment import BillManagement
# from inventory_management.inventory import Inventory_Manage

class Dashboard:

    def __init__(self):
       pass

    def admin_dashboard(self):
        while True:
            print("="*30)
            print("   Welcome! To Admin's Dashboard ")
            print("="*30)
            print("\n1. Staff Management")
            print("2. Menu Management")
            print("3. Inventory Management")
            print("4. Manage Booking")
            print("5. Order Manage ")
            print("6. Billing ")
            print("7. Back")

            choice = input("\nEnter Your Selection to Continue - ").strip()

            if choice == "1":
               register_staff()

            elif choice == "2":
                dis = Menu_manage()
                dis.display_menu()

            elif choice == "3":
                # inv = Inventory_Manage()
                # inv.inventory_menu()
                pass

            elif choice == "4":
                t1 = BookingTable()
                t1.booking_menu()

            elif choice == "5":
                ord = OrderManagement()
                ord.order_menu()
                
            elif choice == "6":
                # bil = BillManagement()
                # bil.billing_menu()
                pass
                
            elif choice == "7":
                return
            
            else :
                print("Invalid Choice!")
       
    def staff_dashboard(self):
        while True:
            print("\n" + "="*50)
            print("Welcome! To Staff's Dashboard ")
            print("=" * 50)
            print("\n1.View Menu")
            print("2.Manage Booking")
            print("3.Order Manange")
            print("4.Billing")
            print("5.Logout")

            choice = input("Enter Your choice : ")

            if choice == "1":
                dis = Menu_manage()
                dis.view_menu()
               
            elif choice == "2":
                t1 = BookingTable()
                t1.booking_menu()
                
            elif choice == "3":
                ord = OrderManagement()
                ord.order_menu()
       
            elif choice == "4":
                # bil = BillManagement()
                # bil.billing_menu()
                pass

            elif choice == "5":
                print("Logging out !....")
                return
            else :
                print("Invalid Choice!....")


