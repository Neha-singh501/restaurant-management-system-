

import stdiomask

# -------------authentication
# ------------------------------------------ 

def get_username():
    
    while True:
        username = input("Enter username : ").strip()
        if not username :
            print("Username Can't Be Empty!...")
        elif " " in username  :
            print("NOt Allow Space In Username. ")
        elif len(username) < 3 :
             print("username must be 3 character. ")
        elif not username[0].isalpha():
            print("Username Start with letter.")
        elif not username.isalnum() :
            print("Please Use only letter and number.")
        else :
            return username

def get_fullname():
    while True:
        full_name = input("Enter Full Name : ").strip().title()
        if  not full_name :
            print("Name is required..")
        elif not full_name.replace(" ","").isalpha():
            print("Name should contain only alphabet and space")
        elif len(full_name) < 3 :
            print("Name must contain at least 3 character")
        elif len(full_name) > 50:
            print("Name can't excced 50 character")
        elif "  " in full_name:
            print("Multiple Space not allow.")

        else :
            return full_name

def get_phone_no():
    while True:
        phone_no = input("Enter Your Phone No. : ").strip()
        if not phone_no :
            print("Phone Number is required..")
        elif not phone_no.isdigit():
            print("Phone No.. should contain Only Digit ")
        elif len(phone_no) !=10:
            print("Please Enter Valid Phone Number")
        elif phone_no[0] not in "6789":
            print("Phone number must start with 6, 7, 8 or 9")
        elif len(set(phone_no)) == 1:
            print("Enter a valid phone number")
        else:
            return phone_no

def get_password():
    while True:
        password = stdiomask.getpass(prompt = "Enter Password : ", mask = "*").strip()
        if password == "" :
            print("Password is required.")
        elif len(password) < 8:
            print("Password Must Be 8 Character.")
        else:
          return password

def get_email():
    while True : 
        email = input("Enter your email: ").strip().lower()

        if  not email :
            print("Email is required")
        elif " " in email:
            print("Email should not contain space")
        elif not email.endswith("@gmail.com"):
            print("Enter Valid email address")
        elif email.count("@") != 1:
            print("Enter Valid Email ")
        elif ".." in email :
            print("Eamil can't consective dots")
        elif  not email[0].isalpha():
            print("Please start with alphabet")

        else:
            return email

#------------------------------------------------
# --------------------menu validation
#-------------------------------------------------


def get_foodname():

    while True:

        food_name = input("Enter Food Name : ").strip().title()

        if not food_name:
            print("Food Name Can't be Empty.")

        elif len(food_name) < 3 :
            print("Food Name must be 3 character.")

        elif len(food_name) > 50:
            print("Food Name can't exceed 50 character")

        elif not any(char.isalpha() for char in food_name):
            print("Food Name must contain only letter & number.")

        else:
            return food_name

    #catagory
def get_category():

    while True:
        category = input("Enter Category : ").strip().title()

        if not category:
            print("Category Can't be empty.")

        elif not category.replace(" ","").isalpha():
            print("Category must be Contain Letters.")

        else:
            return category

def get_price():

    while True:
        price = input("Enter Food Price : ")

        if not price :
            print("Price can't be empty")
            continue

        try :
            price = float(price)

            if price <=0:
                print("Price must be greater then Zero")
                continue

            return price

        except ValueError:
            print("Please Enter valid number")

#====================================
#       Booking
#======================================

def get_guest():

    while True:
        try:
            numofguest = int(input("Enter Number of Guest : ").strip())
        except ValueError:
            print("Please Enter Valid Number")
            continue

        if  not numofguest :
            print("Number of Guests is required")

        elif numofguest < 1:
            print("Number of guests must be at least 1")

        else:
            return numofguest
def get_duration():

    while True:

        try:
            duration = int(input("Enter Duration(in hour) : ").strip())
        except ValueError:
            print("Please Enter a Number")
            continue
            
        if not duration:
            print("Booking Duration is required")


        elif duration <=0 :
            print("Duration Must be at least 1 hour")

        elif duration > 12 :
            print("Duration can't be more 12 hours")

        else :
            return duration

def get_booking_type():
    while True:
        print("\n1. Walk-in Booking")
        print("2. Advance Booking")
        choice = input("Booking type: ").strip()

        if choice == "1":
            return "walk-in"
        if choice == "2":
            return "advance"
        print("Invalid choice. Enter 1 or 2.")


def get_booking_id():
    while True:
        booking_id = input("Enter Booking ID (to cancel): ").strip().upper()

        if booking_id == "0":
            return None
        if not booking_id:
            print("Booking ID can't be empty.")
        elif not booking_id.startswith("BKG") or len(booking_id) != 9:
            print("Invalid ID")
        elif not booking_id.isalnum():
            print("Booking ID can contain only letters and numbers.")
        else:
            return booking_id


def get_yes_no(question):
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()

        if answer in ("y", "n"):
            return answer == "y"
        print("Please enter y or n.")

#========================================
#           order
# ==========================================
          
def get_order_id():
    pass
def get_food_quantity():
    pass
def order_status():
    pass


       



