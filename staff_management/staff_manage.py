
import os 
import json
import uuid
from validation.validate import get_fullname , get_username, get_phone_no, get_password, get_email

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR,"database","user.json")
    
def register_staff():

    while True:
        print("*"*25)
        print("     STAFF MANAGE  ")
        print("*"*25)
        print("\n1. Add_New_Staff ")
        print("2. View Staff")
        print("3. Update Staff")
        print("4. Delete Staff")
        print("5. back")

        choice = input("Enter Your Choice : ")

        if choice == "1":
            new_staff()
        elif choice =="2":
            view_staff()
        elif choice == "3":
            update_staff() 
        elif choice == "4":
            delete_staff() 
        elif choice == "5":
            return
        else :
            print("Invalid Choice!....")

def generate_staff_id(users):
    existing_id = {user.get("id") for user in users}
    while True:
        staff_id = "STF" + uuid.uuid4().hex[:6].upper()
        if staff_id not in existing_id :
            return staff_id

def new_staff():
    try:
        with open(file_path ,"r") as file:
            data = json.load(file)
    except FileNotFoundError , json.JSONDecodeError:
        data = {"users" : []}
       

    staff_id = generate_staff_id(data["users"])
    full_Name = get_fullname()
    username = get_username()
    email = get_email()
    phone_no = get_phone_no()
    password = get_password()
    
    
    for user in data["users"] :
        if user.get("username") == username:
            print("Username Already Registered")
            return
        if user.get("email") == email:
            print("Email Already Taken ")
            return

    new_user = {

        "id" : staff_id,
        "full_Name" : full_Name,
        "username" : username,
        "phone_no" : phone_no,
        "email" : email,
        "password" : password,
        "role" : "staff"
    }

    data["users"].append(new_user)

    with open(file_path, "w") as file :
        json.dump(data,file, indent = 4)


    print("\nStaff Registered Successfully !\n")
    print(f"Your Staff ID Is: {staff_id}")
    print(f"Role : staff")
    

def view_staff():
    try :
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError , json.JSONDecodeError:
        print("File Not Found")
        return

    staff_list = [user for user in data["users"] if user.get("role") == "staff"]

    if not staff_list:
        print("Not Registered Staff")
        return

    print("\n")
    print("                         ************** All Staff ******************")
    print("                                  ...................               ")
    print("\n")

    print(f"{'**ID**':<18}{'**Name**':<20}{'**Username**':<15}{'**Email**':<28}{'**Phone No.**':<18}{'**Role**':<8}")
    print("."*110)
   

    for user in staff_list :
        print(
            f"{user.get('id', ''):<18}"
            f"{user.get('full_Name', ''):<20}"
            f"{user.get('username', ''):<15}"
            f"{user.get('email', ''):<28}"
            f"{user.get('phone_no', ''):<18}"
            f"{user.get('role', ''):<8}"
        )
        
        print("\n" + "-"*110)


def update_staff():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("User file not found.")
        return
    view_staff()
    while True:
        staff_id = input("Enter Staff ID to update : ").strip().upper()

        staff = None
        for user in data["users"]:
            if user.get("id") == staff_id :
                staff = user
                break

        if staff is None:
            print("Staff ID not found. Please Enter Valid Staff ID")
            continue 

        if staff.get("role") == "admin":
            print("You can't update admin..")
            return

        break

    print("\n" + "."*30)
    print("     UPDATE STAFF")
    print("."*30)

    print(f'\nSelected Staff: {staff.get("full_Name")}')
    print("1. Full Name")
    print("2. Phone No.")
    print("3. Email")
    print("4. Back")

    choice = input("Enter Your Choice : ").strip()

    if choice == "1":
        staff["full_Name"] = get_fullname()

    elif choice == "2":
        staff["phone_no"] = get_phone_no()

    elif choice == "3":
        new_email = get_email()
        for user in data["users"]:
            if user.get("email") == new_email and user.get("id") != staff_id:
                print("This Email is already registered with another user.")
                return
        staff["email"] = new_email

    elif choice == "4":
        return

    else:
        print("Invalid choice.")
        return

    json_text = json.dumps(data, indent=4)
    with open(file_path, "w") as file:
        file.write(json_text)

    print("Update Successful!....")


def delete_staff():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("User file not found .")
        return

    view_staff()
    while True:
        staff_id = input("Enter Staff ID to Delete : ").strip().upper()

        staff = None
        for user in data["users"]:
            if user.get("id") == staff_id :
                staff = user
                break

        if staff is None:
            print("Staff ID not found. Enter Valid Staff ID")
            continue

        if staff.get("role") == "admin":
            print("You can't delete admin...")
            return

        break
    

    print("\n" + "." * 30)
    print("        DELETE STAFF")
    print("." * 30)
    print(f'ID       : {staff.get("id")}')
    print(f'Name     : {staff.get("full_Name")}')
    print(f'Username : {staff.get("username")}')
    print(f'Email       : {staff.get("email")}')
    print(f'Phone    : {staff.get("phone_no")}')

    confirm = input("\nConfirm deletion..(yes/no): ").strip().lower()

    if confirm != "yes":
        print("Staff Deleting Cancelled!...")
        return

    data["users"].remove(staff)

    json_text = json.dumps(data, indent=4)
    with open(file_path, "w") as file:
        file.write(json_text)

    print("Staff Deleted Successfully!...")







