
from menu_management.menu_manage import Menu_manage
from staff_management.staff_manage import register_staff
from booking_management.booking_table import BookingTable
from order_management.order_manage import OrderManagement
from billing_management.billing_payment import BillManagement
from inventory_management.inventory import Inventory_Manage
from logs.logger import log_info , log_warning 

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
               log_info("Admin Selected Staff management")
               register_staff()
               log_info("Staff Management Complete")

            elif choice == "2":
                log_info("Admin Selecter Menu Management")
                menu_obj = Menu_manage()
                menu_obj.display_menu()
                log_info("Menu Management Completed")

            elif choice == "3":
                log_info("Admin Selected Inventory Management")
                inv_obj = Inventory_Manage()
                inv_obj.inventory_menu()
                log_info("Inventory management Complete")

            elif choice == "4":
                log_info("Admin Selected Booking Management")
                t1 = BookingTable()
                t1.booking_menu()
                log_info("Booking Management Complete")

            elif choice == "5":
                log_info("Admin Selected order management")
                ord_obj = OrderManagement()
                ord_obj.order_menu()
                log_info("Order Management Complete")
                
            elif choice == "6":
                log_info("Admin Selected Bill Management ")
                bill_obj = BillManagement()
                bill_obj.billing_menu()
                log_info("Bill management Complete")
               
            elif choice == "7":
                log_info("Admin Returned From Dashboard")
                return
            
            else :
                log_warning("Invalid Choice in Admin Dashboard")
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
                log_info("Staff Selected View Menu")
                dis = Menu_manage()
                dis.view_menu()
                log_info("View Menu Complete")
               
            elif choice == "2":
                log_info("Staff Selected Booking Management")
                t1 = BookingTable()
                t1.booking_menu()
                log_info("Complete Booking mnaagement")
                
            elif choice == "3":
                log_info("Staff Started Order management")
                ord_obj = OrderManagement()
                ord_obj.order_menu()
                log_info("Complete Booking Management")
       
            elif choice == "4":
                log_info("Staff Selected Bill Management")
                bill_obj = BillManagement()
                bill_obj.billing_menu()
                log_info("Complete Billing Management")

            elif choice == "5":
                log_info("Staff Returned From Dashboard")
                print("Logging out !....")
                return
            else :
                log_warning("Invalid Choice in Staff Dashboard :")
                print("Invalid Choice!....")


