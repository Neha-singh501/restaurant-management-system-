
from user_authentication.auth import Auth

auth = Auth()

def register_admin():
    while True:
        print("*"*45)
        print("     ADMIN INITIAL SETUP")
        print("*"*45)
        print("\n 1. SIGN UP")
        print("2. EXIT")

        choice = input("Enter Your Choice : ")

        if choice == "1":
            auth.admin_sign_up()
           
        elif choice == "2":
            return
        else :
            print("Invalid Choice !...")

def main():

    if not auth.admin_exist():
        register_admin()
        
    while True:
        print("*" * 45)
        print("     RESTAURANT MANAGEMENT SYSTEM ")
        print("*" * 45)
        print("\n1. SIGN_IN")
        print("2. EXIT")

        choice = input("\nEnter Your Choice : ")
        
        if choice == "1":
           role_menu(auth)

        elif choice == "2":
            print("Thanks..! For Visiting Our Restaurant Management .")
            break
        else :
            print("\nInvalid Choice !....")

def role_menu(auth):
    while True:
       
        print("\n.........SIGN IN AS..........\n")
        
        print("1. ADMIN SIGN IN ")
        print("2. STAFF SIGN IN")
        print("3. BACK")

        role_choice = input("\nEnter choice :  ").strip()

        if role_choice == "1":
          
            auth.admin_sign_in()

        elif role_choice == "2":
            auth.staff_sign_in()

        elif role_choice =="3":
            break
        else :
            print("Invalid Choice!....")




