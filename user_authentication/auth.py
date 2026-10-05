
import json
import os
import uuid
from validation.validate import get_fullname,get_username , get_password , get_email 
from dashboard.dashboards import Dashboard

class Auth :

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(BASE_DIR,"database","user.json")


    
    def admin_sign_up(self):
        if self.count_admins() >= self.MAX_ADMINS:
            print(f"Admin limit reached. Only {self.MAX_ADMINS} admins are allowed.")
            return

        data = self.load_users()

        print("\n" + "." * 30)
        print("        ADMIN SIGN UP")
        print("." * 30)
        print(f"Admins registered: {self.count_admins()} of {self.MAX_ADMINS}")

        full_Name = get_fullname()
        username = get_username()
        email = get_email()
        password = get_password()

        for user in data["users"]:
            if user.get("username") == username:
                print("Username already registered.")
                return
            if user.get("email") == email:
                print("Email already registered.")
                return

        admin_id = "ADM" + uuid.uuid4().hex[:6].upper()

        new_admin = {
            "id": admin_id,
            "full_Name": full_Name,
            "username": username,
            "role": "admin",
            "email": email,
            "password": password
        }

        data["users"].append(new_admin)

        json_text = json.dumps(data, indent=4)
        with open(self.file_path, "w") as file:
            file.write(json_text)

        print("\nAdmin registered successfully!")
        print(f"Admin ID : {admin_id}")
        pass
  
    def sign_in(self , selected_role):
        
        username = get_username()
        password = get_password()

        try : 
            with open(self.file_path,"r") as file:
                data = json.load(file)
        
        except FileNotFoundError, json.JSONDecodeError :
            data = {"users" : []}
            return
        user_found = False
        for user in data["users"]:
            if user["username"] == username and user["password"] ==password:
                user_found = True 
                role = user.get("role")
                if role != selected_role:
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
                    print(f"Staff Name :  {user.get('full_Name')}")
                dash_obj = Dashboard()
                if role == "admin":
                        dash_obj.admin_dashboard()
                        return
                elif role == "staff":
                        dash_obj.staff_dashboard()
                        return
        if not user_found:
            print("Login Failed!...")

    def admin_sign_in(self):
         self.sign_in("admin")

    def staff_sign_in(self):
         self.sign_in("staff")






           

    










    
    

        
