import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkinter import filedialog
from PIL import Image, ImageTk  # To display images

class RoomBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Booking System")
        self.root.geometry("800x600")
        
        # Set the background image
        self.bg_image = Image.open("images/bedroom.jpg")  # Provide the correct path for your background image
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Frame for the form
        self.form_frame = tk.Frame(self.root, bg="white", bd=5)
        self.form_frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)

        # Connect to Database
        self.conn = mysql.connector.connect(
            host="localhost", port="3306", username="root", password="sidhu1234@deep", database="management"
        )
        self.cursor = self.conn.cursor()

        # Customer information variables
        self.var_name = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_aadhar = tk.StringVar()
        self.var_father_name = tk.StringVar()
        self.var_age = tk.StringVar()

        # Room & Meal choices
        self.room_type = tk.StringVar()
        self.room_price = tk.DoubleVar()
        self.meal_options = []

        # Create all input fields for the customer, room and meal info
        self.create_full_booking_form()

    def create_full_booking_form(self):
        tk.Label(self.form_frame, text="Customer Info", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        # Customer Name
        tk.Label(self.form_frame, text="Name", bg="white").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.form_frame, textvariable=self.var_name, width=30).grid(row=1, column=1, pady=5)

        # Contact
        tk.Label(self.form_frame, text="Contact", bg="white").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.form_frame, textvariable=self.var_contact, width=30).grid(row=2, column=1, pady=5)

        # Email
        tk.Label(self.form_frame, text="Email", bg="white").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(self.form_frame, textvariable=self.var_email, width=30).grid(row=3, column=1, pady=5)

        # Aadhar ID
        tk.Label(self.form_frame, text="Aadhar ID", bg="white").grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(self.form_frame, textvariable=self.var_aadhar, width=30).grid(row=4, column=1, pady=5)

        # Father's Name
        tk.Label(self.form_frame, text="Father's Name", bg="white").grid(row=5, column=0, padx=10, pady=5)
        tk.Entry(self.form_frame, textvariable=self.var_father_name, width=30).grid(row=5, column=1, pady=5)

        # Age
        tk.Label(self.form_frame, text="Age", bg="white").grid(row=6, column=0, padx=10, pady=5)
        tk.Entry(self.form_frame, textvariable=self.var_age, width=30).grid(row=6, column=1, pady=5)

        # Room Type Selection
        tk.Label(self.form_frame, text="Choose Room Type", bg="white").grid(row=7, column=0, padx=10, pady=5)
        room_options = ['Single', 'Double', 'Deluxe']
        room_dropdown = ttk.Combobox(self.form_frame, values=room_options, textvariable=self.room_type, width=27)
        room_dropdown.grid(row=7, column=1)
        room_dropdown.current(0)

        # Meal Options Selection
        tk.Label(self.form_frame, text="Meals (Select all that apply)", bg="white").grid(row=8, column=0, padx=10, pady=5)
        meal_options = ["Breakfast", "Lunch", "Dinner", "None"]
        for i, meal in enumerate(meal_options):
            tk.Checkbutton(self.form_frame, text=meal, variable=tk.IntVar(), command=lambda meal=meal: self.select_meal(meal), bg="white").grid(row=9+i, column=0, padx=10, sticky=tk.W)

        # Calculate Price Button
        tk.Button(self.form_frame, text="Calculate Price", command=self.calculate_price, width=15, bg="#FF9800", fg="white", font=("Arial", 12)).grid(row=13, column=1, pady=10)

        # Confirm Booking Button
        tk.Button(self.form_frame, text="Confirm Booking", command=self.confirm_booking, width=15, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=14, column=1, pady=10)

    def select_meal(self, meal):
        if meal not in self.meal_options:
            self.meal_options.append(meal)
        else:
            self.meal_options.remove(meal)

    def calculate_price(self):
        room_prices = {'Single': 1000, 'Double': 1500, 'Deluxe': 2000}
        meal_prices = {'Breakfast': 100, 'Lunch': 200, 'Dinner': 150, 'None': 0}

        room_choice = self.room_type.get()
        room_price = room_prices.get(room_choice, 0)

        total_meal_price = sum([meal_prices.get(meal, 0) for meal in self.meal_options])

        total_price = room_price + total_meal_price
        self.room_price.set(total_price)

        # Display pricing information
        tk.Label(self.form_frame, text=f"Room Type: {room_choice} - {room_price}", bg="white").grid(row=15, column=0, padx=10)
        tk.Label(self.form_frame, text=f"Meals: {', '.join(self.meal_options)} - {total_meal_price}", bg="white").grid(row=16, column=0, padx=10)
        tk.Label(self.form_frame, text=f"Total Price: {total_price}", bg="white").grid(row=17, column=0, padx=10)

        # Check for returning customer discount
        self.check_discount()

    def check_discount(self):
        # Check if customer is already in the database
        self.cursor.execute(f"SELECT COUNT(*) FROM customer WHERE contact = '{self.var_contact.get()}'")
        customer_count = self.cursor.fetchone()[0]
        
        if customer_count >= 2:
            discount = 0.15
        elif customer_count == 1:
            discount = 0.10
        else:
            discount = 0
        
        total_price = self.room_price.get()
        discounted_price = total_price - (total_price * discount)

        tk.Label(self.form_frame, text=f"Discounted Price: {discounted_price}", bg="white").grid(row=18, column=0, padx=10)

    def confirm_booking(self):
        name = self.var_name.get()
        contact = self.var_contact.get()
        email = self.var_email.get()
        aadhar = self.var_aadhar.get()
        father_name = self.var_father_name.get()
        age = self.var_age.get()
        room = self.room_type.get()
        price = self.room_price.get()
        meals = ', '.join(self.meal_options)
        
        try:
            self.cursor.execute(
                """INSERT INTO customer 
                (name, contact, email, aadhar, father_name, age, room, price, meals) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                (name, contact, email, aadhar, father_name, age, room, price, meals)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Booking Successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")
        finally:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = RoomBookingApp(root)
    root.mainloop()
