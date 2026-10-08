import os
import json
import uuid
from datetime import datetime, timedelta

from validation.validate import (get_fullname,get_phone_no,get_guest,get_duration)

class BookingTable:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.booking_path = os.path.join(BASE_DIR, "database", "booking.json")
        self.table_path = os.path.join(BASE_DIR, "database", "table.json")

        self.open_hour = 10         #10:00AM
        self.close_hour = 23        # 23:00 PM
        self.advance_days = 30      # 30 days

    def load_bookings(self):

        try:
            with open(self.booking_path, "r") as file:
                booking_data = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return {"booking": []}

        if "booking" not in booking_data:
            booking_data["booking"] = []

        return booking_data
    

    def save_bookings(self, booking_data):

        with open(self.booking_path, "w") as file:
            json.dump(booking_data, file, indent=4)


    def load_tables(self):

        try:
            with open(self.table_path, "r") as file:
                data = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

        tables = {}

        try:
            table_groups = data["table"][0]

            for table_type, details in table_groups.items():

                capacity = int(details["capacity"])

                for table_no in details["available_tables"]:

                    tables[str(table_no)] = {
                        "type": table_type,
                        "seats": capacity
                    }

        except:
            return {}

        return tables

#generate ID    

    def generate_booking_id(self, booking_list):

        existing_ids = {booking.get("booking_id")for booking in booking_list}

        while True:

            booking_id = "BKG" + uuid.uuid4().hex[:6].upper()

            if booking_id not in existing_ids:
                return booking_id

            
#advance booking

    def get_advance_datetime(self):

        while True:

            date_input = input("Enter Booking Date (YYYY-MM-DD): ").strip()
            time_input = input("Enter Booking Time (HH:MM, 24-hour): ").strip()

            try:
                select_time = datetime.strptime(f"{date_input} {time_input}","%Y-%m-%d %H:%M")

            except ValueError:

                print("\nInvalid date or time format!")
                continue

            current_time = datetime.now().replace(second=0)
            if select_time <= current_time:
                print("\nBooking time must be in the future.")
                continue

            latest_date = (current_time +timedelta(days=self.advance_days))

            if select_time > latest_date:
                print(f"\nAdvance booking is allowed only "f"up to {self.advance_days} days.")
                continue

            if not (self.open_hour <= select_time.hour < self.close_hour):
                print(f"\nRestaurant timing is "f"{self.open_hour}:00 to {self.close_hour}:00.")
                continue

            return select_time

#restaurant time

    def within_open_hours(self, start_time, end_time):

        opening_time = start_time.replace(hour=self.open_hour,minute=0,second=0)

        closing_time = start_time.replace(hour=self.close_hour,minute=0,second=0)

        if start_time < opening_time:
            return False

        if end_time > closing_time:
            return False

        return True

#table free

    def is_table_free(self,table_id,start_time,end_time,bookings):

        for booking in bookings:

            if str(booking.get("table_id")) != str(table_id):
                continue

            if booking.get("status") == "cancelled":
                continue

            existing_start = self.booking_start(booking)

            if existing_start is None:
                continue

            try:
                existing_duration = float(booking.get("duration", 0))

            except :
                continue


            existing_end = (
                existing_start +
                timedelta(hours=existing_duration)
            )


            # Time overlap check

            if (
                start_time < existing_end
                and end_time > existing_start
            ):

                return False


        return True


    # -------------------------------------------------
    # GET BOOKING START TIME
    # -------------------------------------------------

    def booking_start(self, booking):

        try:

            return datetime.strptime(
                f'{booking["booking_date"]} '
                f'{booking["booking_time"]}',
                "%Y-%m-%d %H:%M"
            )

        except (KeyError, ValueError):

            return None


    # -------------------------------------------------
    # CREATE BOOKING
    # -------------------------------------------------

    def book_table(self):

        tables = self.load_tables()

        if not tables:
            print("\nNo tables found.")
            return

        data = self.load_bookings()
        bookings = data["booking"]


#booking type

        print("\n" + "." * 45)
        print("              TABLE BOOKING")
        print("." * 45)

        print("\n           1. Walk-in Booking")
        print("             2. Advance Booking")

        type_choice = input("\nEnter Booking Type: ").strip()

        if type_choice == "1":

            booking_type = "walk-in"

        elif type_choice == "2":

            booking_type = "advance"

        else:

            print("\nInvalid booking type!")
            return

        customer_name = get_fullname()
        phone_no = get_phone_no()
        numofguests = get_guest()

        if booking_type == "walk-in":
            start_time = datetime.now().replace(second=0)
        else:
            start_time = self.get_advance_datetime()

        duration = get_duration()

        try:
            duration = float(duration)

        except :

            print("\nInvalid duration!")
            return

        end_time = (start_time +timedelta(hours=duration))

#restaurant timing
        if not self.within_open_hours(start_time,end_time):

            print(f"\nRestaurant timing is "f"{self.open_hour}:00 to "f"{self.close_hour}:00.")
            print("\nPlease select a valid booking duration.")

            return

#avail-table

        available = {}

        for table_id, details in tables.items():

            seats = details["seats"]

            if (seats >= numofguests and self.is_table_free(table_id,start_time,end_time,bookings)):
                available[table_id] = details

        if not available:
            print("\nNo suitable table is available for the selected time.")
            return


        print("\n" + "-" * 55)
        print("                AVAILABLE TABLES")
        print("-" * 55)

        print(
            f"{'Table':<10}"
            f"{'Type':<15}"
            f"{'Seats':<10}"
        )

        print("-" * 55)


        for table_id, details in available.items():

            print(
                f"{table_id:<10}"
                f"{details['type']:<15}"
                f"{details['seats']:<10}"
            )


        print("-" * 55)


        while True:

            table_id = input("Enter Table ID: ").strip().upper()
            if table_id in available:
                break

            print("Invalid Table ID. Please select from available tables.")

        if booking_type == "walk-in":
            status = "occupied"
        else:
            status = "booked"

#Booking
        new_booking = {
            "booking_id": self.generate_booking_id(bookings),
            "customer_name": customer_name,
            "phone_no": phone_no,
            "table_id": table_id,
            "number_of_guests": numofguests,
            "booking_type": booking_type,
            "booking_date": start_time.strftime("%Y-%m-%d"),
            "booking_time": start_time.strftime("%H:%M"),
            "duration": duration,
            "status": status
        }

        bookings.append(new_booking)
        self.save_bookings(data)
#msg

        print("\n" + "." * 50)
        print("             BOOKING CONFIRMED")
        print("." * 50)

        print(f"Booking ID : {new_booking['booking_id']}")
        print(f"Customer Name   : {customer_name}")
        print(f"Table NO.      : {table_id}")
        print(f"Guests     : {numofguests}")
        print(f"Date       : {new_booking['booking_date']}")
        print(f"Time       : {new_booking['booking_time']}")
        print(f"Duration   : {duration} hours")
        print(f"Status     : {status}")

        print("\nTable booking completed successfully!")

#booking menu

    def booking_menu(self):

        while True:

            print("\n" + "=" * 40)
            print("          TABLE BOOKING")
            print("=" * 40)

            print("\n1. Create Booking")
            print("2. View Bookings")
            print("3. Cancel Booking")
            print("4. Back")

            choice = input("\nEnter Your Choice: ").strip()

            if choice == "1":
                self.book_table()

            elif choice == "2":
                self.view_booking()

            elif choice == "3":
               self.cancel_booking()

            elif choice == "4":
                return
            else:
                print("\nInvalid Choice!")



    def view_booking(self):

        data = self.load_bookings()
        bookings = data["booking"]

        if not bookings:
            print("Booking not found")
            return

        print("\n")
        print("                                          ***************** ALL BOOKING *********************")
        print("."*130)

        print(f"{'Booking ID' :<15}"f"{'Customer Name' :<20}"f"{'Table ID' :<15}"f"{'Guests' :<10}"f"{'Booking Type' :<20}"f"{'Date' :<13}"f"{'Time' :<15}"f"{'Duration' :<15}"f"{'Status' :<15}")

        print("."*130)

        for booking in bookings:
            booking_id = booking.get("booking_id")
            customer_name = booking.get("customer_name")
            table_id = booking.get("table_id")
            guests = booking.get("number_of_guests")
            booking_type = booking.get("booking_type")
            booking_date = booking.get("booking_date")
            booking_time = booking.get("booking_time")
            duration = booking.get("duration")
            status = booking.get("status")

            print(
                f"{booking_id:<15}"
                f"{customer_name:<20}"
                f"{table_id:<15}"
                f"{guests:<10}"
                f"{booking_type:<20}"
                f"{booking_date:<13}"
                f"{booking_time:<15}"
                f"{duration :<15}"
                f"{status :<15}")

        print("=" * 130)

        return bookings



    def cancel_booking(self):
        
        data = self.load_bookings()
        bookings = data["booking"]

        if not bookings:
            print("Booking Not found")
            return
        
        self.view_booking()
        booking_id = input("\nEnter Booking ID to Cancel : ").strip().upper()
       
        for booking in bookings:
            if booking.get("booking_id") == booking_id:
                status = booking.get("status")

                if status == "cancelled":
                    print("\nBooking is already cancelled")
                    return 
                if status != "booked":
                    print("\nBooking Can't be Cancelled")
                    return
               
                booking["status"] = "cancelled"
                booking["cancelled_at"] = str(datetime.now())
                self.save_bookings(data)

                print("\nBooking Cancelled Successfully!...\n")
                print(f"Booking ID : {booking_id} ")
                print(f"Table No. : {booking.get('table_id')}")
                return

        print("Booking ID not found")        



            

        






