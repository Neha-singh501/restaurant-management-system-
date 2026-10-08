
from user_authentication.auth import Auth
from logs.logger import log_info,log_warning

auth = Auth()

def register_admin():
    while True:
        print("*"*45)
        log_info("Open Admin setup screen")
        print("     ADMIN INITIAL SETUP")
        print("*"*45)
        print("\n 1. SIGN UP")
        print("2. EXIT")

        choice = input("Enter Your Choice : ")

        if choice == "1":
            log_info("Admin Selected Setup")
            auth.admin_sign_up()
           
        elif choice == "2":
            log_info("Admin Exited from setup")
            return
        else :
            log_warning("Invalid choice enterd in admin setup")
            print("Invalid Choice !...")

def main():

    log_info("Program Start")
    if not auth.admin_exist():
        log_info("Admin doesn't exist. Admin setup start")
        register_admin()
        
    while True:
        print("*" * 45)
        print("     RESTAURANT MANAGEMENT SYSTEM ")
        print("*" * 45)
        print("\n1. SIGN_IN")
        print("2. EXIT")

        choice = input("\nEnter Your Choice : ")
        
        if choice == "1":
           log_info("User selected sign up")
           role_menu(auth)

        elif choice == "2":
            log_info("Program exited")
            print("Thanks..! For Visiting Our Restaurant Management .")
            break
        else :
            log_warning(f"Invalid choice entered in main menu : {choice}")
            print("\nInvalid Choice !....")

def role_menu(auth):
    while True:
       
        print("\n.........SIGN IN AS..........\n")
        
        print("1. ADMIN SIGN IN ")
        print("2. STAFF SIGN IN")
        print("3. BACK")

        role_choice = input("\nEnter choice :  ").strip()

        if role_choice == "1":
            log_info("Admin sign in selected")
            auth.admin_sign_in()

        elif role_choice == "2":
            log_info("Staff sign in selected")
            auth.staff_sign_in()

        elif role_choice =="3":
            log_info("user returned from role menu")
            break
        else :
            log_warning(f"Invalid choice entered in role menu : {role_choice}")
            print("Invalid Choice!....")




