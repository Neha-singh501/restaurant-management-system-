
from logs.logger import log_info, log_warning, log_error
import stdiomask

# -------------authentication
# ------------------------------------------ 

def get_username():
    
    while True:
        username = input("Enter username : ").strip()
        if not username :
            log_warning("user Validation failed : user is empty ")
            print("Username Can't Be Empty!...")
        elif " " in username  :
            log_warning("user Validation failed : space is not allow ")
            print("NOt Allow Space In Username. ")
        elif len(username) < 3 :
            log_warning("user Validation failed : less than 3 character ")
            print("username must be 3 character. ")
        elif not username[0].isalpha():
            log_warning("user Validation failed : username not start letter")
            print("Username Start with letter.")
        elif not username.isalnum() :
            print("Please Use only letter and number.")
        else :
            log_info("Username validation successful")
            return username

def get_fullname():
    while True:
        full_name = input("Enter Full Name : ").strip().title()
        if  not full_name :
            log_warning("Full name validation failed : full name is empty")
            print("Name is required..")
        elif not full_name.replace(" ","").isalpha():
            log_warning("full name validation failed : full name isn't alphabet")
            print("Name should contain only alphabet and space")
        elif len(full_name) < 3 :
            log_warning("Full name validation failed : less then 3 character")
            print("Name must contain at least 3 character")
        elif len(full_name) > 20:
            log_warning("Full name validation failed : greater then 20 character")
            print("Name can't excced 20 character")
        elif "  " in full_name:
            log_warning("Full name validation failed : use multiple space")
            print("Multiple Space not allow.")

        else :
            log_info("Full name validation successful")
            return full_name

def get_phone_no():
    while True:
        phone_no = input("Enter Your Phone No. : ").strip()
        if not phone_no :
            log_warning("Phone No  validation failed : phone no is empty")
            print("Phone Number is required..")
        elif not phone_no.isdigit():
            log_warning("phone no validation failed : phone no is character")
            print("Phone No.. should contain Only Digit ")
        elif len(phone_no) !=10:
            log_warning("phone no validation failed : less 10 digit phone no")
            print("Please Enter Valid Phone Number")
        elif phone_no[0] not in "6789":
            log_warning("phone no validation failed : start with 1,2,3,4,5")
            print("Phone number must start with 6, 7, 8 or 9")
       
        else:
            log_info("Phone no validation successful")
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
            log_warning("Email validation failed : not entered email")
            print("Email is required")
        elif " " in email:
            log_warning("Email validation failed :using sapce")
            print("Email should not contain space")
        elif not email.endswith("@gmail.com"):
            log_warning("Email validation failed : email address wrong")
            print("Enter Valid email address")
        elif email.count("@") != 1:
            log_warning("Email validation failed : email address wrong")
            print("Enter Valid Email ")
        elif ".." in email :
            log_warning("Email validation failed : email address wrong")
            print("Eamil can't consective dots")
        elif  not email[0].isalpha():
            log_warning("Email validation failed : using special character")
            print("Please start with alphabet")

        else:
            log_info("Email Validation Successful")
            return email

#------------------------------------------------
# --------------------menu validation
#-------------------------------------------------


def get_foodname():

    while True:

        food_name = input("Enter Food Name : ").strip().title()

        if not food_name:
            log_warning("Food Name validation failed : empty food name")
            print("Food Name Can't be Empty.")

        elif len(food_name) < 3 :
            log_warning("Food Name validation failed : less then 3 character")
            print("Food Name must be 3 character.")

        elif len(food_name) > 50:
            log_warning("Food Name validation failed : greater then 50 character")
            print("Food Name can't exceed 50 character")

        elif not any(char.isalpha() for char in food_name):
            log_warning("Food Name validation failed : using special character")
            print("Food Name must contain only letter & number.")

        else:
            log_info("Food Name validation successful")
            return food_name

    #catagory
def get_category():

    while True:
        category = input("Enter Category : ").strip().title()

        if not category:
            log_warning("Category Validation failed : enterd empty")
            print("Category Can't be empty.")

        elif not category.replace(" ","").isalpha():
            log_warning("Category validation failed : using digit")
            print("Category must be Contain Letters.")

        else:
            log_info("Category Validation Successful")
            return category

def get_price():

    while True:
        price = input("Enter Food Price : ")

        if not price :
            log_warning("Price Validation Falied : Entered Empty")
            print("Price can't be empty")
            continue

        try :
            price = float(price)

            if price <=0:
                log_warning("Price validation Failed : less then 0 entered")
                print("Price must be greater then Zero")
                continue

            return price

        except ValueError:
            log_warning("Price Validation Failed : invalid number")
            print("Please Enter valid number")

def get_full_price():

    while True:
        price = input("Enter Full Price : ")

        if not price :
            log_warning("Price Validation Falied : Entered Empty")
            print("Price can't be empty")
            continue

        try :
            price = float(price)

            if price <=0:
                log_warning("Price validation Failed : less then 0 entered")
                print("Price must be greater then Zero")
                continue

            return price

        except ValueError:
            log_warning("Price Validation Failed : invalid number")
            print("Please Enter valid number")
#====================================
#       Booking
#======================================

def get_guest():

    while True:
        try:
            numofguest = int(input("Enter Number of Guest : ").strip())
        except ValueError:
            log_error
            print("Please Enter Valid Number")
            continue

        if  not numofguest :
            log_warning("Guest Validation failed : enter empty")
            print("Number of Guests is required")

        elif numofguest < 1:
            log_warning("Guest validation failed : less then 1 guest")
            print("Number of guests must be at least 1")

        else:
            log_info("Guest validation successful")
            return numofguest
def get_duration():

    while True:

        try:
            duration = int(input("Enter Duration(in hour) : ").strip())
        except ValueError:
            log_warning("Duration Validation Failed : enter character")
            print("Please Enter a Number")
            continue
            
        if not duration:
            log_warning("Duration Validation Failed : empty duration")
            print("Booking Duration is required")


        elif duration <=0 :
            log_warning("Duration Validation Failed : less then 1 hour")
            print("Duration Must be at least 1 hour")

        elif duration > 12 :
            log_warning("Duration Validation Failed : greater then 12 hour")
            print("Duration can't be more 12 hours")

        else :
            log_info("Duration Validation Successful")
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
            log_info("Booking ID Cancel Successful : Use 0 ")
            return None
        if not booking_id:
            log_warning("Booking ID validation Failed : enter empty")
            print("Booking ID can't be empty.")
        elif not booking_id.startswith("BKG") or len(booking_id) != 9:
            print("Invalid ID")
        elif not booking_id.isalnum():
            log_warning("Booking ID validation failed : invalid enter")
            print("Booking ID can contain only letters and numbers.")
        else:
            log_info("Booking ID validation Successful")
            return booking_id


