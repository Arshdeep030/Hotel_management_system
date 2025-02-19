from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import random
from time import strftime
from datetime import datetime
import mysql.connector  # pip install mysql-connector-python


class DetailsRoom:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management System")
        self.root.geometry("1550x800+0+0")

        # title
        lbl_title = Label(self.root, text="Room Booking Details", font=(
            "Times new roman", 18, "bold"), bg="black", fg="#CD853F", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # Logo image
        img2 = Image.open("images\logo.png")
        
        img2 = img2.resize((100, 40), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        lblimg = Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=5, y=2, width=100, height=40)

        # label frame
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="New Room Add", font=(
            "Times new roman", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=540, height=350)

        # labels andd entry
        # Floor
        lbl_floor = Label(labelframeleft, text="Floor:", font=(
            "arial", 12, "bold"), padx=2, pady=6)
        lbl_floor.grid(row=0, column=0, sticky=W, padx=20)

        self.var_floor=StringVar()
        entry_floor = ttk.Entry(
            labelframeleft,textvariable=self.var_floor, width=20, font=("arial", 13, "bold"))
        entry_floor.grid(row=0, column=1, sticky=W)

        # Room No
        lbl_roomNo = Label(labelframeleft, font=(
            "arial", 12, "bold"), text="RoomNo: ", padx=2, pady=6)
        lbl_roomNo.grid(row=1, column=0, sticky=W, padx=20)

        self.var_RoomNo=StringVar()
        entry_roomNo = ttk.Entry(labelframeleft,textvariable=self.var_RoomNo, font=(
            "arial", 12, "bold"), width=20)
        entry_roomNo.grid(row=1, column=1, sticky=W)

       
        
        lbl_lbl_RoomType = Label(labelframeleft, font=("arial", 12, "bold"), text="RoomType: ", padx=2, pady=6)
        lbl_lbl_RoomType.grid(row=2, column=0, sticky=W)
        
        self.var_Roomtype = StringVar() 
        
        combo_lbl_RoomType = ttk.Combobox(labelframeleft, textvariable=self.var_Roomtype, font=("arial", 12, "bold"), width=27, state="readonly" )
        combo_lbl_RoomType["value"] = ("Single", "Double", "Luxury")
        combo_lbl_RoomType.current(0)
        combo_lbl_RoomType.grid(row=2, column=1)

        # Buttons
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=200, width=412, height=40)

        btnAdd = Button(btn_frame, text="Add",command=self.add_data, font=("arial", 11, "bold"), bg="black", fg="#CD853F", width=10)
        btnAdd.grid(row=0, column=0, padx=1)

        btnUpdate = Button(btn_frame, text="Update",command=self.update, font=(
            "arial", 11, "bold"), bg="black", fg="#CD853F", width=10)
        btnUpdate.grid(row=0, column=1, padx=1)

        btnDelete = Button(btn_frame, text="Delete",command=self.mDelete, font=(
            "arial", 11, "bold"), bg="black", fg="#CD853F", width=10)
        btnDelete.grid(row=0, column=2, padx=1)

        btnReset = Button(btn_frame, text="Reset",command=self.reset, font=(
            "arial", 11, "bold"), bg="black", fg="#CD853F", width=10)
        btnReset.grid(row=0, column=3, padx=1)
        
        # Table frame for search
        Table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View details and Search System", font=(
            "Times new roman", 12, "bold"), padx=2)
        Table_frame.place(x=600, y=55, width=600, height=350)
                
        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        self.room_table = ttk.Treeview(Table_frame, column=("floor", "roomno","roomtype"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)
        
        self.room_table.heading("floor", text="Floor")
        self.room_table.heading("roomno", text="RoomNo")  # Corrected column name
        self.room_table.heading("roomtype", text="RoomType")


        
        self.room_table["show"] = "headings"

        self.room_table.column("floor", width=100)
        self.room_table.column("roomno", width=100)
        self.room_table.column("roomtype", width=100)
        self.room_table.pack(fill=BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>",self.get_cuersor)
        self.fetch_data()
        
        
    def add_data(self):
        if self.var_floor.get() == "" or self.var_Roomtype.get()=="":
            messagebox.showerror("Error", "All fields are required",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", port="3306", username="root", password="sidhu1234@deep", database="management")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO details VALUES (%s, %s, %s)", (
                                                                                                    self.var_floor.get(),
                                                                                                    self.var_RoomNo.get(),
                                                                                                    self.var_Roomtype.get()
                                                                                                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "New Room added Succesfully", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning!", f"Something went wrong: {str(es)}", parent=self.root) 
    
    #fetch data
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", port="3306", username="root", password="sidhu1234@deep", database="management")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from details")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.room_table.delete(*self.room_table.get_children())
            for i in rows:
                self.room_table.insert("",END,values=i)
            conn.commit()
        conn.close()
        
    def get_cuersor(self,event=""):
        cursor_row=self.room_table.focus()
        content=self.room_table.item(cursor_row)
        row=content["values"]
        self.var_floor.set(row[0])
        self.var_RoomNo.set(row[1])
        self.var_Roomtype.set(row[2])
    
    def update(self):
           if self.var_floor.get() == "":
               messagebox.showerror("Error", "Please enter floor number", parent=self.root)
           else:
               conn = mysql.connector.connect(host="localhost", port="3306", username="root", password="sidhu1234@deep", database="management")
               my_cursor = conn.cursor()
               query = "UPDATE details SET floor=%s, RoomType=%s WHERE RoomNo=%s" 
               values = (self.var_floor.get(), self.var_Roomtype.get(), self.var_RoomNo.get())  # Updated the order of values
               my_cursor.execute(query, values)
               conn.commit()
               conn.close()
               self.fetch_data()
               messagebox.showinfo("Update", "Room details have been updated successfully", parent=self.root)


            
    def mDelete(self):
        mDelete = messagebox.askyesno("Hostel Management System", "Do you want to delete this Room details", parent=self.root)
        if mDelete:
            conn = mysql.connector.connect(host="localhost", port="3306", username="root", password="sidhu1234@deep", database="management")
            my_cursor = conn.cursor()
            query = "DELETE FROM details WHERE RoomNo=%s"
            value = (self.var_RoomNo.get(),)
            my_cursor.execute(query, value)
            
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Delete", "Customer details have been deleted successfully", parent=self.root)

    def reset(self):
        self.var_floor.set("")
        self.var_RoomNo.set("")
        self.var_Roomtype.set("")







if __name__ == "__main__":
    root = Tk()
    obj = DetailsRoom(root)
    root.mainloop()