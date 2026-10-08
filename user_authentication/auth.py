
import json
import os
import uuid
from logs.logger import log_info, log_warning, log_error
from validation.validate import get_fullname,get_username , get_password , get_email , get_phone_no
from dashboard.dashboards import Dashboard

class Auth :

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(BASE_DIR,"database","user.json")

   
    def load_users(self):
        try:
             with open(self.file_path, "r") as file:
                 data = json.load(file)
                 log_info("User Data load Successfully")
                 return data
        except(FileNotFoundError,json.JSONDecodeError):
             log_warning("User File not found.empty user")
             log_error("invalid json data")
             return{"users" : []}
        
    def admin_exist(self):

        data = self.load_users()
        for user in data["users"]:
            if user.get("role") == "admin":
                log_info("Admin already exist")
                return True
        log_info("No admin account found")
        return False
        
    def admin_sign_up(self):

        data = self.load_users()

        for user in data["users"]:
            if user.get("role") == "admin":
                log_warning("Admin Already Exist. But again try")
                print("\nAdmin already register...")
                return

        print("*"*45)
        print("         ADMIN SETUP")
        print("*"*45)

        full_name = get_fullname()
        username = get_username()
        email = get_email()
        phone_no = get_phone_no()
        password = get_password()

        for user in data["users"]:
             if user.get("username")== username :
                  log_warning("Admin registration failed : user name already exist ")
                  print("Username already Taken")
                  return
             if user.get("email") == email:
                  log_warning("Admin registration failed : email already exist")
                  print("Email Already create")
                  return

        admin_id = "ADM" + uuid.uuid4().hex[:6].upper()

        new_admin = {
            "id": admin_id,
            "full_name": full_name,
            "username": username,
            "phone_no": phone_no,
            "role": "admin",
            "email": email,
            "password": password
        }

        data["users"].append(new_admin)

        with open(self.file_path, "w") as file:
           json.dump(data,file,indent =4)
        print("\n")
        log_info("Admin Registeration Successfully")
        print("Admin registered successfully!")
        print(f"Admin ID : {admin_id}")
    
  
    def sign_in(self , selected_role):
        
        email = get_email()
        password = get_password()

        try : 
            with open(self.file_path,"r") as file:
                data = json.load(file)
        
        except (FileNotFoundError, json.JSONDecodeError) :
            log_error("Login Failed : user file not found")
            log_error("Login Failed : invalid json data")
            data = {"users" : []}
            return
        
        user_found = False

        for user in data["users"]:
            if user["email"] == email and user["password"] ==password:
                user_found = True 
                role = user.get("role")
                if role != selected_role:
                    log_warning("Access Denied : correct credentials but wrong role selected ")
                    print(f"\n Access Denied ! ..")
                    print("                 Your login credentials are correct.")
                    print(f"            Registered Role : {role.title()}")
                    print(f"            Selected Role   : {selected_role.title()}")
                    print("                 You are not authorized to access this dashboard.")
                    print("                 Please select the correct role and try again.")
                    return
                print("\nLogin Successful!....")

                if role == "staff":
                    print(f"Staff ID :  {user.get('id')}")
                    print(f"Staff Name :  {user.get('full_name')}")

                dash_obj = Dashboard()

                if role == "admin":
                        log_info("Admin Dashboard opened")
                        dash_obj.admin_dashboard()
                        return
                
                elif role == "staff":
                        log_info("Staff Dashboard opened")
                        dash_obj.staff_dashboard()
                        return
        if not user_found:
            log_warning("Login Failed : invalid email or password")
            print("Login Failed!...")

    def admin_sign_in(self):
        log_info("Admin Sign in process Started")
        self.sign_in("admin")

    def staff_sign_in(self):
        log_info("Staff Sign in Process Started")
        self.sign_in("staff")






           

    










    
    

        
