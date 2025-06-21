import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import mysql.connector
from PIL import Image, ImageTk
import tempfile
import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import Scrollbar, Canvas
import numpy as np
from reportlab.pdfgen import canvas as pdf_canvas



# ------------------ DATABASE CONNECTION ------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tisha@111",
    database="Invoice_software"
)
cursor = db.cursor()

# ------------------ GUI SETUP ------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Invoice/Billing Management System")
app.geometry("1100x600")

last_invoice_data = {}

def save_transaction( user_id,cust_id,payment_mode,tot_price,tot_gst,grand_tot):
    cursor = db.cursor()
    invoice_date = datetime.now().strftime('%Y-%m-%d ')
    invoice_time = datetime.now().strftime('%H:%M:%S')

    sql = """
    INSERT INTO transactions 
    ( user_id,cust_id, invoice_date,invoice_time,payment_mode,tot_price,tot_gst,grand_tot)
    VALUES ( %s, %s, %s, %s, %s,%s,%s,%s)
    """
    values = (user_id,cust_id,invoice_date,invoice_time,payment_mode,tot_price,tot_gst,grand_tot)
    cursor.execute(sql, values)
    db.commit() 

# ------------------ FRAMES ------------------
frames = {}
current_user_role = None  # Track if Admin or Cashier logged in

def show_frame(name):
    for frame in frames.values():
        frame.pack_forget()
    frames[name].pack(padx=20, pady=20, fill="both", expand=True)

def update_sidebar_after_login():
    # Clear sidebar
    for widget in sidebar.winfo_children():
        widget.destroy()

    ctk.CTkLabel(sidebar, text="Menu", font=("Helvetica", 20, "bold")).pack(pady=20)

    # After login, show functions
    if current_user_role == "admin":
        admin_functions = [
            ("Billing", lambda: show_frame("billing")),
            ("Sales Analytics", lambda: show_frame("analytics")),
            ("Inventory Management", lambda: show_frame("inventory")),
            ("Product Catalog", lambda: show_frame("products")),
            ("Customer Management", lambda: show_frame("customers")),
            ("Setting", lambda: show_frame("setting")),
        ]
        for text, cmd in admin_functions:
            ctk.CTkButton(sidebar, text=text, command=cmd).pack(pady=10, fill="x", padx=10)
    elif current_user_role == "cashier":
        cashier_functions = [
            ("Billing", lambda: show_frame("billing")),
        ]
        for text, cmd in cashier_functions:
            ctk.CTkButton(sidebar, text=text, command=cmd).pack(pady=10, fill="x", padx=10)
# ------------------ LOGIN FUNCTIONS ------------------
def admin_login():
    global current_user_role
    global user_id
    username = ad_user.get()
    password = ad_pass.get()

    query = "SELECT * FROM users WHERE role='admin' AND u_name=%s AND pass=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    user_id=result[0]

    if result:
        current_user_role = "admin"
        messagebox.showinfo("Success", "Admin Login Successful!")
        update_sidebar_after_login()
        show_frame("billing")  # Default after login
    else:
        messagebox.showerror("Error", "Invalid Admin Credentials")

def cashier_login():
    global current_user_role
    global user_id
    username = cash_user.get()
    password = cash_pass.get()

    query = "SELECT * FROM users WHERE role='cashier' AND u_name=%s AND pass=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    user_id=result[0]

    if result:
        current_user_role = "cashier"
        messagebox.showinfo("Success", "Cashier Login Successful!")
        update_sidebar_after_login()
        show_frame("billing")  # Default after login
    else:
        messagebox.showerror("Error", "Invalid Cashier Credentials")

# ------------------ SIDEBAR ------------------
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="Login Menu", font=("Helvetica", 18)).pack(pady=20)

ctk.CTkButton(sidebar, text="Admin Login", command=lambda: show_frame("admin_login")).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Cashier Login", command=lambda: show_frame("cashier_login")).pack(pady=10, fill="x", padx=10)

# ------------------ FRAMES ------------------
# Admin Login Frame
frame_admin_login = ctk.CTkFrame(app)
frames["admin_login"] = frame_admin_login

ctk.CTkLabel(frame_admin_login, text="Admin Login", font=("Helvetica", 22)).pack(pady=20)
ad_user = ctk.CTkEntry(frame_admin_login, placeholder_text="Admin Username")
ad_user.pack(pady=10)
ad_pass = ctk.CTkEntry(frame_admin_login, placeholder_text="Admin Password", show="*")
ad_pass.pack(pady=10)
ctk.CTkButton(frame_admin_login, text="Login", command=admin_login).pack(pady=20)

# Cashier Login Frame
frame_cashier_login = ctk.CTkFrame(app)
frames["cashier_login"] = frame_cashier_login

ctk.CTkLabel(frame_cashier_login, text="Cashier Login", font=("Helvetica", 22)).pack(pady=20)
cash_user = ctk.CTkEntry(frame_cashier_login, placeholder_text="Cashier Username")
cash_user.pack(pady=10)
cash_pass = ctk.CTkEntry(frame_cashier_login, placeholder_text="Cashier password", show="*")
cash_pass.pack(pady=10)
ctk.CTkButton(frame_cashier_login, text="Login", command=cashier_login).pack(pady=20)

# ------------------ SIDEBAR UPDATE AFTER LOGIN ------------------

def update_sidebar_after_login():
    # Clear sidebar
    for widget in sidebar.winfo_children():
        widget.destroy()

    ctk.CTkLabel(sidebar, text="Menu", font=("Helvetica", 18)).pack(pady=20)

    # After login, show functions
    if current_user_role == "admin":
        admin_functions = [
            ("Billing", lambda: show_frame("billing")),
            ("Sales Analytics", lambda: show_frame("analytics")),
            ("Inventory Management", lambda: show_frame("inventory")),
            ("Product Catalog", lambda: show_frame("products")),
            ("Customer Management", lambda: show_frame("customers")),
            ("Setting", lambda: show_frame("setting")),
        ]
        for text, cmd in admin_functions:
            ctk.CTkButton(sidebar, text=text, command=cmd).pack(pady=10, fill="x", padx=10)
    elif current_user_role == "cashier":
        cashier_functions = [
            ("Billing", lambda: show_frame("billing")),
        ]
        for text, cmd in cashier_functions:
            ctk.CTkButton(sidebar, text=text, command=cmd).pack(pady=10, fill="x", padx=10)

# ------------------ FUNCTIONALITY FOR LOGINS ------------------

# Admin Login
def admin_login():
    global current_user_role
    username = ad_user.get()
    password = ad_pass.get()

    query = "SELECT * FROM users WHERE role='admin' AND u_name=%s AND pass=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        current_user_role = "admin"
        messagebox.showinfo("Success", "Admin Login Successful!")
        update_sidebar_after_login()
        show_frame("billing")  # Default after login
    else:
        messagebox.showerror("Error", "Invalid Admin Credentials")

# Cashier Login
def cashier_login():
    global current_user_role
    username = cash_user.get()
    password = cash_pass.get()

    query = "SELECT * FROM users WHERE role='cashier' AND u_name=%s AND pass=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        current_user_role = "cashier"
        messagebox.showinfo("Success", "Cashier Login Successful!")
        update_sidebar_after_login()
        show_frame("billing")  # Default after login
    else:
        messagebox.showerror("Error", "Invalid Cashier Credentials")



#----------------Billing Frame (Common for both Admin and Cashier)--------------------#
######## Biling functions

frame_billing = ctk.CTkFrame(app)
frames["billing"] = frame_billing

def fetch_products():
    cursor.execute("SELECT name FROM products")
    products = cursor.fetchall()
    return [p[0] for p in products]

def fetch_rate(event=None):
    selected = product_dropdown.get()
    cursor.execute("SELECT price FROM products WHERE name = %s", (selected,))
    price = cursor.fetchone()
    if price:
        rate_entry.configure(state="normal")
        rate_entry.delete(0, "end")
        rate_entry.insert(0, str(price[0]))
        rate_entry.configure(state="readonly")

# Add product to cart
cart = []
def add_to_cart():
    selected_product = product_dropdown.get()
    qty = int(quantity_dropdown.get())
    # Fetch from database
    cursor.execute("SELECT product_id, category, price, available_qty FROM products WHERE name = %s", (selected_product,))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Error", "Product not found in the database!")
        return
    product_id, category, price, available_qty = result
    if qty > available_qty:
        messagebox.showerror("Error", "Not enough stock available!")
        return
    gst_rate = float(0.18)  # 18% GST
    subtotal = float(qty * price)
    gst_amount = round((subtotal * gst_rate),2)
    # Add to cart
    cart.append({
        "id": product_id,
        "name": selected_product,
        "category": category,
        "rate": price,
        "qty": qty,
        "gst": gst_amount,
        "subtotal": subtotal  # Optional: include GST in subtotal
    })
    # Update stock in database
    cursor.execute("UPDATE products SET available_qty = available_qty - %s WHERE name = %s", (qty, selected_product))
    db.commit()
    update_cart_display()

def update_cart_display():
    # Clear Treeview
    global customer_id
    for item in cart_tree.get_children():
        cart_tree.delete(item)
    total_amount = 0
    for item in cart:
        cart_tree.insert("", "end", values=(
            item['id'],
            item['name'],
            item['category'],
            f"{item['rate']:.2f}",
            item['qty'],
            f"{item['subtotal']:.2f}"
        ))
        total_amount += (item['subtotal']+item['gst'])
    # Update total label
    total_label.configure(text=f"Total Billing Amount: ₹{total_amount:.2f}")

product_dropdown = ctk.CTkComboBox(frame_billing, values=fetch_products(), command=fetch_rate)
product_dropdown.pack(pady=5)
rate_entry = ctk.CTkEntry(frame_billing, placeholder_text="Rate", state="readonly")
rate_entry.pack(pady=5)
quantity_dropdown = ctk.CTkComboBox(frame_billing, values=[str(i) for i in range(1, 21)])
quantity_dropdown.pack(pady=5)
ctk.CTkButton(frame_billing, text="Add to Cart", command=add_to_cart).pack(pady=10)
style = ttk.Style()
style.theme_use("default")
# Bold header font and increased row height/font
style.configure("Treeview.Heading", font=("Arial", 13, "bold"),color="#3B82F6")
style.configure("Treeview", font=("Arial", 12), rowheight=35)  # Normal font for row data
# Treeview widgetl
columns = ("Product ID", "Name", "Category", "Rate", "Qty", "Subtotal")
cart_tree = ttk.Treeview(frame_billing, columns=columns, show="headings", height=10)  # Adjusted height
for col in columns:
    cart_tree.heading(col, text=col)
    cart_tree.column(col, anchor="center", width=150)  # Wider columns for better readability
cart_tree.pack(pady=10)
# Total label and navigation button
total_label = ctk.CTkLabel(frame_billing, text="Total Billing Amount: ₹0.00", font=("Arial", 13, "bold"))
total_label.pack(pady=5)

ctk.CTkButton(frame_billing, text="Proceed to Customer Info", command=lambda: show_frame("customer_info")).pack(pady=10)
frame_customer_info = ctk.CTkFrame(app)
frames["customer_info"] = frame_customer_info

ctk.CTkLabel(frame_customer_info, text="Customer Details", font=("Helvetica", 24)).pack(pady=10)

# --- Entry Fields ---
cust_name_entry = ctk.CTkEntry(frame_customer_info, placeholder_text="Customer Name")
cust_name_entry.pack(pady=5)

cust_mobile_entry = ctk.CTkEntry(frame_customer_info, placeholder_text="Mobile Number")
cust_mobile_entry.pack(pady=5)

payment_mode_dropdown = ctk.CTkComboBox(frame_customer_info, values=["Cash", "UPI", "Card", "Net Banking", "Pay by Credits"])
payment_mode_dropdown.pack(pady=5)

# --- Global variable for storing customer_id ---
customer_id = None

# --- Function to lookup or create customer ---
def lookup_customer():
    global customer_id
    name = cust_name_entry.get()
    mobile = cust_mobile_entry.get()

    if not name or not mobile:
        messagebox.showerror("Error", "Please enter both Name and Mobile Number.")
        return

    cursor.execute("SELECT cust_id FROM customer WHERE name=%s AND phno=%s", (name, mobile))
    result = cursor.fetchone()

    if result:
        customer_id = result[0]
        messagebox.showinfo("Success", f"Customer Found! ID: {customer_id}")
    else:
        customer_id = random.randint(1000, 1100)  # You can also switch to auto-increment DB ID on insert
        cursor.execute("INSERT INTO customer (cust_id, name, phno, last_trans_date, no_of_visits) VALUES (%s, %s, %s, %s, %s)",
                   (customer_id, cust_name_entry.get(), cust_mobile_entry.get(), datetime.datetime.now().strftime('%Y-%m-%d'), 1))
        db.commit()
        messagebox.showinfo("New Customer", f"No existing record found. Assigned New ID: {customer_id}")
    

# --- Lookup Button ---
lookup_btn = ctk.CTkButton(frame_customer_info, text="Check Customer", command=lookup_customer)
lookup_btn.pack(pady=10)
payment_mode_dropdown.pack()
# Payment Mode
def load_payment_fields(event=None):
    for widget in payment_details_frame.winfo_children():
        widget.destroy()
    mode = payment_mode_dropdown.get()
    if mode == "Card":
        card_entry = ctk.CTkEntry(payment_details_frame, placeholder_text="Card Number")
        card_entry.pack(pady=5)
        cvv_entry = ctk.CTkEntry(payment_details_frame, placeholder_text="CVV")
        cvv_entry.pack(pady=5)
        otp_entry = ctk.CTkEntry(payment_details_frame, placeholder_text="Enter OTP")
        otp_entry.pack(pady=5)
        def validate_card():
            card = card_entry.get()
            cvv = cvv_entry.get()
            otp = otp_entry.get()
            if not (card.isdigit() and len(card) == 16):
                ctk.CTkLabel(payment_details_frame, text="Invalid card number!", text_color="red").pack()
                return
            if not (cvv.isdigit() and len(cvv) == 3):
                ctk.CTkLabel(payment_details_frame, text="Invalid CVV!", text_color="red").pack()
                return
            if not (otp.isdigit() and 4 <= len(otp) <= 6):
                ctk.CTkLabel(payment_details_frame, text="Invalid OTP!", text_color="red").pack()
                return
            ctk.CTkLabel(payment_details_frame, text="✅ Successful Payment!!").pack()
        ctk.CTkButton(payment_details_frame, text="Validate & Pay", command=validate_card).pack(pady=5)
    elif mode == "Net Banking":
        bank_entry = ctk.CTkEntry(payment_details_frame, placeholder_text="Bank Name")
        bank_entry.pack(pady=5)
        acc_entry = ctk.CTkEntry(payment_details_frame, placeholder_text="Account Number")
        acc_entry.pack(pady=5)
        def validate_netbanking():
            bank = bank_entry.get()
            acc = acc_entry.get()
            if not bank.strip():
                ctk.CTkLabel(payment_details_frame, text="Bank name cannot be empty!", text_color="red").pack()
                return
            if not (acc.isdigit() and 9 <= len(acc) <= 18):
                ctk.CTkLabel(payment_details_frame, text="Invalid account number!", text_color="red").pack()
                return
            ctk.CTkLabel(payment_details_frame, text="✅ Successful Payment!!").pack()
        ctk.CTkButton(payment_details_frame, text="Validate & Pay", command=validate_netbanking).pack(pady=5)
    elif mode == "UPI":
        ctk.CTkLabel(payment_details_frame, text="Enter UPI ID or Scan QR").pack(pady=5)
        upi_id_entry = ctk.CTkEntry(payment_details_frame, placeholder_text="Enter UPI ID")
        upi_id_entry.pack(pady=5)
        try:
            img = Image.open("sample_qr.png")
            img = img.resize((200, 200))
            qr_img = ImageTk.PhotoImage(img)
            qr_display = ctk.CTkLabel(payment_details_frame, image=qr_img, text="")
            qr_display.image = qr_img
            qr_display.pack()
            def validate_upi():
                upi_id = upi_id_entry.get()
                if not upi_id or "@" not in upi_id:
                    ctk.CTkLabel(payment_details_frame, text="Invalid UPI ID!", text_color="red").pack()
                    return
                ctk.CTkLabel(payment_details_frame, text="✅ UPI Payment Successful!").pack()
            ctk.CTkButton(payment_details_frame, text="Validate & Pay", command=validate_upi).pack(pady=5)
        except:
            ctk.CTkLabel(payment_details_frame, text="QR code image not found").pack()
    elif mode == "Pay by Credits":
        mobile = cust_mobile_entry.get()
        if not mobile:
            ctk.CTkLabel(payment_details_frame, text="Please enter mobile number above to check credits!").pack()
            return
        try:
            cursor.execute("SELECT credits FROM customer WHERE phno = %s", (mobile,))
            result = cursor.fetchone()
            if not result:
                ctk.CTkLabel(payment_details_frame, text="Customer not found in database!").pack()
                return
            credits = int(result[0])
            total = sum(item['subtotal'] for item in cart)
            required_credits = int(total) // 1000
            remaining = credits - required_credits
            if remaining < 0:
                ctk.CTkLabel(payment_details_frame, text="❌ Insufficient Credits!", text_color="red").pack()
            else:
                ctk.CTkLabel(payment_details_frame, text=f"✅ {required_credits} credits used successfully!.\nRemaining: {remaining}").pack()
        except Exception as e:
            ctk.CTkLabel(payment_details_frame, text=f"DB Error: {e}").pack()
    elif mode == "Cash":
        ctk.CTkLabel(payment_details_frame, text="✅ Successful Payment! Cash is received at counter!").pack()
payment_mode_dropdown.configure(command=load_payment_fields)
# Frame to load payment-specific widgets
payment_details_frame = ctk.CTkFrame(frame_customer_info)
payment_details_frame.pack(pady=10)
#Generate Invoice Method
def generate_invoice():
    if not cust_name_entry.get() or not cust_mobile_entry.get():
        messagebox.showerror("Error", "Please fill customer details before generating invoice!")
        return
    if not cart:
        messagebox.showerror("Error", "Cart is empty. Please add products before generating invoice!")
        return
    
    total = float(sum(item['subtotal'] for item in cart))
    sgst = total * 0.09
    cgst = total * 0.09
    grand_total = total + sgst + cgst
    payment_mode = payment_mode_dropdown.get()

    show_frame("final_invoice")

    # Prepare product lines
    product_lines = []
    for item in cart:
        product_lines.append([
            item['name'][:20],            # Trim if long
            item['category'][:30],
            float(item['rate']),
            item['qty'],
            float(item['gst']),
            float(item['subtotal'])
        ])

    invoice_text.configure(state="normal")
    invoice_text.delete("1.0", "end")
    invoice_text.configure(font=("Courier New", 10))  # Monospaced font

    # Header
    invoice_text.insert("end", "\n FINAL INVOICE\n", "center_bold")
    invoice_text.insert("end", f"\nCustomer ID: {customer_id}\nName: {cust_name_entry.get()}\nMobile: {cust_mobile_entry.get()}\nPayment Mode: {payment_mode}\n", "center_bold")
    invoice_text.insert("end", "\n" + "-" * 115 + "\n", "center_bold")

    # Table header
    headers = ["Name", "Category", "Rate", "Qty", "GST", "Total"]
    col_format = "{:<20} {:<40} {:>8} {:>5} {:>8} {:>10}"
    invoice_text.insert("end", col_format.format(*headers) + "\n", "center_bold")
    invoice_text.insert("end","\n" + "-" * 115 + "\n","center_bold")

    # Table rows
    for line in product_lines:
        invoice_text.insert("end", col_format.format(
            line[0],
            line[1],
            f"₹{line[2]:.2f}",
            str(line[3]),
            f"₹{line[4]:.2f}",
            f"₹{line[5]:.2f}"
        ) + "\n")

    # Footer
    invoice_text.insert("end", "\n" +"-" * 115 + "\n", "center_bold")
    invoice_text.insert("end", f"\nSubtotal: ₹{total:.2f}\nSGST (9%): ₹{sgst:.2f}\nCGST (9%): ₹{cgst:.2f}\nGrand Total: ₹{grand_total:.2f}\n", "bold")

    invoice_text.see("end")
    invoice_text.update_idletasks()
    invoice_text.configure(state="disabled")

    save_transaction(
        user_id=user_id,
        cust_id=customer_id,
        payment_mode=payment_mode_dropdown.get(),
        tot_price=total,
        tot_gst=sgst+cgst,
        grand_tot=grand_total
    )

    messagebox.showinfo("Success", "Transaction Saved!")
    cart.clear()
    update_cart_display()

    # Save for PDF export
    global last_invoice_data
    last_invoice_data = {
        "cust_id": customer_id,
        "name": cust_name_entry.get(),
        "mobile": cust_mobile_entry.get(),
        "payment_mode": payment_mode,
        "products": product_lines,
        "total": total,
        "sgst": sgst,
        "cgst": cgst,
        "grand_total": grand_total
    }

def proceed_to_invoice():
    if not cust_name_entry.get() or not cust_mobile_entry.get():
        messagebox.showerror("Error", "Please fill customer details!")
        return
    selected_mode = payment_mode_dropdown.get()
    if not selected_mode:
        messagebox.showerror("Error", "Select a payment mode!")
        return
    generate_invoice()
ctk.CTkButton(frame_customer_info, text="Proceed to Invoice", command=proceed_to_invoice).pack(pady=20)

# ---- Export PDF Function ---- 

def export_invoice_pdf():
    try:
        data = last_invoice_data
        file_path = tempfile.gettempdir() + f"/Invoice_{data['cust_id'] or 'UNKNOWN'}.pdf"
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        y = height - 50

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, y, " FINAL INVOICE")
        y -= 30

        # Date and Invoice number (optional)
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, y, f"Invoice #: INV-{data.get('cust_id', '000')} | Date: {data.get('date', 'N/A')}")
        y -= 30

        # Customer Info
        c.setFont("Helvetica", 12)
        c.drawString(40, y, f" Customer ID: {data['cust_id'] or 'Not Available'}")
        y -= 20
        c.drawString(40, y, f" Name: {data['name']}")
        y -= 20
        c.drawString(40, y, f" Mobile: {data['mobile']}")
        y -= 20
        c.drawString(40, y, f" Payment Mode: {data['payment_mode']}")
        y -= 30

        # Table Headers
        c.setFont("Helvetica-Bold", 11)
        headers = ["Name", "Category", "Rate ", "Qty", "GST ", "Total "]
        x_pos = [40, 150, 300, 350, 390, 460]
        for i, h in enumerate(headers):
            c.drawString(x_pos[i], y, h)
        y -= 15
        c.line(40, y, 550, y)
        y -= 15

        # Table Rows
        c.setFont("Helvetica", 10)
        for row in data['products']:
            for i, val in enumerate(row):
                c.drawString(x_pos[i], y, str(val))
            y -= 15

        y -= 25
        # Totals Box
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(520, y, f"Subtotal: Rs.{data['total']:.2f}")
        y -= 15
        c.drawRightString(520, y, f"SGST (9%): Rs.{data['sgst']:.2f}")
        y -= 15
        c.drawRightString(520, y, f"CGST (9%): Rs.{data['cgst']:.2f}")
        y -= 15
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(520, y, f"Grand Total: Rs.{data['grand_total']:.2f}")
        y -= 40
        
        # Footer
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, y, "NOTE : All transactions are done in Indian Rupees!")
        y -= 15
        c.drawCentredString(width / 2, y, " D-Mart, Kothrud, Pune |  +91-9876543210 |  support@dmart.com")
        y -= 15
        c.drawCentredString(width / 2, y, " Thank You for Shopping with Us! Visit Again.")

        # Save and open
        c.save()
        os.startfile(file_path)  # Windows only. Use subprocess for cross-platform.
    except Exception as e:
        messagebox.showerror("Export Error", str(e)) 
frame_final_invoice = ctk.CTkFrame(app)
frames["final_invoice"] = frame_final_invoice
ctk.CTkLabel(frame_final_invoice, text="Final Invoice ", font=("Helvetica", 24)).pack(pady=10)
qr_label = ctk.CTkLabel(frame_final_invoice, text="")
qr_label.pack(pady=10)
invoice_text = tk.Text(frame_final_invoice, height=30, width=100, wrap=tk.WORD, font=("Arial", 12))
invoice_text.tag_configure("bold", font=("Arial", 12, "bold"))
invoice_text.tag_configure("center_bold", font=("Arial", 13, "bold"))
invoice_text.pack(pady=10)
# Export PDF Button
# ctk.CTkButton(frame_final_invoice, text="📄 Download Invoice as PDF", command=export_invoice_pdf, fg_color="#3B82F6").pack(pady=10) 



# Sales Analytics Frame (Admin)
#-----------sales and analytics------------

# Frame for Analytics
frame_analytics = ctk.CTkFrame(app)
frames["analytics"] = frame_analytics
frame_analytics.pack(fill="both", expand=True)  # Ensure frame takes full space and is centered

# Title
title_label = ctk.CTkLabel(frame_analytics, text="📊 Sales & Customer Analytics Dashboard", font=("Helvetica", 22))
title_label.pack(pady=20, anchor="center")

# Scrollable Area for better space management
canvas = Canvas(frame_analytics)
scrollbar = Scrollbar(frame_analytics, orient="vertical", command=canvas.yview)
scrollable_frame = ctk.CTkFrame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set, width=1000, height=600)

# Center-align the scrollable area
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Period Selection - Center-align
period_var = ctk.StringVar(value="Weekly")
period_options = ["Daily", "Weekly", "Monthly", "Yearly"]
period_menu = ctk.CTkOptionMenu(scrollable_frame, variable=period_var, values=period_options, command=lambda _: plot_analytics())
period_menu.pack(pady=20, padx=20, anchor="center")

# Center-align the plots
plot_frame = ctk.CTkFrame(scrollable_frame)
plot_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Fetch Functions

def fetch_sales_data(period):
    if period == "Daily":
        query = """
        SELECT DATE(invoice_date), SUM(grand_tot) FROM transaction
        WHERE invoice_date >= CURDATE() - INTERVAL 1 DAY
        GROUP BY DATE(invoice_date)
        """
    elif period == "Weekly":
        query = """
        SELECT DATE(invoice_date), SUM(grand_tot) FROM transaction
        WHERE invoice_date >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE(invoice_date)
        """
    elif period == "Monthly":
        query = """
        SELECT DATE(invoice_date), SUM(grand_tot) FROM transaction
        WHERE invoice_date >= CURDATE() - INTERVAL 1 MONTH
        GROUP BY DATE(invoice_date)
        """
    elif period == "Yearly":
        query = """
        SELECT DATE_FORMAT(invoice_date, '%Y-%m'), SUM(grand_tot) FROM transaction
        WHERE invoice_date >= CURDATE() - INTERVAL 1 YEAR
        GROUP BY DATE_FORMAT(invoice_date, '%Y-%m')
        """
    else:
        return []
    cursor.execute(query)
    return cursor.fetchall()

def fetch_sales_distribution():
    query = "SELECT grand_tot FROM transaction"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def fetch_customer_credits():
    query = """
    SELECT name, credits FROM customer ORDER BY credits DESC LIMIT 10
    """
    cursor.execute(query)
    return cursor.fetchall()

def fetch_peak_sales_hours():
    query = """
    SELECT HOUR(invoice_date) AS hour, AVG(grand_tot) FROM transaction
    GROUP BY hour ORDER BY hour
    """
    cursor.execute(query)
    return cursor.fetchall()

def fetch_customer_retention():
    query = """
    WITH first_purchase AS (
        SELECT cust_id, MIN(invoice_date) AS first_purchase_date
        FROM transaction
        GROUP BY cust_id
    )
    SELECT WEEK(t.invoice_date) AS week, COUNT(DISTINCT t.cust_id) AS retained_customers
    FROM transaction t
    JOIN first_purchase fp ON t.cust_id = fp.cust_id
    WHERE t.invoice_date >= fp.first_purchase_date
    AND WEEK(t.invoice_date) > WEEK(fp.first_purchase_date)
    GROUP BY WEEK(t.invoice_date)
    """
    cursor.execute(query)
    return cursor.fetchall()

# Plotting Analytics
def plot_analytics():
    from tkinter import messagebox  # Add this import at top if not already present

    # Clear previous plots
    for widget in plot_frame.winfo_children():
        widget.destroy()

    try:
        sales_data = fetch_sales_data(period_var.get())
        if sales_data:
            x, y = zip(*sales_data)
            fig, ax = plt.subplots(figsize=(7, 3.5))
            ax.plot(x, y, marker='o', color='steelblue')
            ax.set_title(f"Total Sales Over Time ({period_var.get()})")
            ax.set_xlabel("Date")
            ax.set_ylabel("Sales Amount (₹)")
            ax.grid(True)
            fig.tight_layout()
            canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame).get_tk_widget()
            canvas_widget.pack(fill="x", padx=40, pady=10, anchor="n")
    except Exception as e:
        messagebox.showerror("Plot Error", f"Sales Over Time plot failed:\n{e}")

    try:
        dist = fetch_sales_distribution()
        if dist:
            fig, ax = plt.subplots(figsize=(7, 3.5))
            ax.hist(dist, bins=20, color='mediumpurple', edgecolor='black')
            ax.set_title("Distribution of Invoice Amounts")
            ax.set_xlabel("Invoice Amount (₹)")
            ax.set_ylabel("Frequency")
            fig.tight_layout()
            canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame).get_tk_widget()
            canvas_widget.pack(fill="x", padx=40, pady=10, anchor="n")
    except Exception as e:
        messagebox.showerror("Plot Error", f"Invoice Distribution plot failed:\n{e}")

    # Add similar try/except blocks for other plot sections if needed
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Customer Credits
    credit_data = fetch_customer_credits()
    if credit_data:
        names, credits = zip(*credit_data)
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.barh(names, credits, color='darkorange')
        ax.set_title("Top 10 Customers by Credits Earned")
        ax.set_xlabel("Credits")
        ax.set_ylabel("Customer")
        ax.invert_yaxis()
        fig.tight_layout()
        canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame).get_tk_widget()
        canvas_widget.pack(fill="x", padx=40, pady=10, anchor="n")  # Center-aligning the plot under the title

    # Peak Hours Scatter Plot
    peak = fetch_peak_sales_hours()
    if peak:
        hours, avgs = zip(*peak)
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.scatter(hours, avgs, color='seagreen')
        ax.plot(hours, avgs, linestyle='--', color='gray')
        ax.set_title("Average Sales by Hour of Day")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Avg Sales (₹)")
        fig.tight_layout()
        canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame).get_tk_widget()
        canvas_widget.pack(fill="x", padx=40, pady=10, anchor="n")  # Center-aligning the plot under the title

    # Customer Retention
    retention = fetch_customer_retention()
    if retention:
        weeks, retained_customers = zip(*retention)
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(weeks, retained_customers, marker='o', color='crimson')
        ax.set_title("Customer Retention Over Weeks")
        ax.set_xlabel("Week")
        ax.set_ylabel("Retained Customers")
        fig.tight_layout()
        canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame).get_tk_widget()
        canvas_widget.pack(fill="x", padx=40, pady=10, anchor="n")  # Center-aligning the plot under the title

    # Dynamically adjust the canvas height based on content
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Centering the Frame and Calling Plotting on Visibility
frame_analytics.bind("<Visibility>", lambda e: plot_analytics())

# Inventory Management Frame (Admin)

frame_inventory = ctk.CTkFrame(app)
frames["inventory"] = frame_inventory

ctk.CTkLabel(frame_inventory, text="Inventory Management", font=("Helvetica", 24)).pack(pady=20)

# Function to place stock orders
def place_stock_order():
    product_id = stock_product_id.get()
    quantity = stock_quantity.get()

    # Fetch product details from database
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        messagebox.showerror("Error", "Product not found.")
        return

    available_qty = product[3]  # available_qty from products table (index 3 in this case)
    price = product[2]  # price from products table (index 2 in this case)

    # Calculate total amount for the order
    total_amount = price * int(quantity)
    status = "pending"

    # Insert stock order into the database
    cursor.execute("""
    INSERT INTO stock_orders (product_id, quantity, order_date, status, total_amount)
    VALUES (%s, %s, %s, %s, %s)
    """, (product_id, quantity, datetime.date.today(), status, total_amount))

    db.commit()

    messagebox.showinfo("Success", "Stock Order Placed Successfully!")
    stock_product_id.delete(0, 'end')
    stock_quantity.delete(0, 'end')

def mark_order_as_received(order_id):
    # Fetch order info
    cursor.execute("SELECT product_id, quantity FROM stock_orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()

    if not order:
        raise ValueError("Order not found. Please check the Order ID.")

    product_id, quantity = order

    # Update product quantity
    cursor.execute("UPDATE products SET available_qty = available_qty + %s WHERE product_id = %s", (quantity, product_id))

    # Update order status
    cursor.execute("UPDATE stock_orders SET status = 'received' WHERE order_id = %s", (order_id,))
    db.commit()
   

# Low stock alert (below reorder threshold)
def check_low_stock():
    cursor.execute("""
    SELECT * FROM products WHERE available_qty <= reorder_threshold
    """)
    low_stock_products = cursor.fetchall()

    if low_stock_products:
        low_stock_text = "Low Stock Products:\n"
        for product in low_stock_products:
            low_stock_text += f"Product ID: {product[0]}, Name: {product[1]}, Available Qty: {product[3]}\n"
    else:
        low_stock_text = "No low stock products found."

    messagebox.showinfo("Low Stock Alert", low_stock_text)

# Function to generate purchasing bill for stock order
def generate_purchasing_bill():
    product_id = stock_product_id.get()
    quantity = stock_quantity.get()

    # Fetch product details
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        messagebox.showerror("Error", "Product not found.")
        return

    product_name = product[1]
    unit_price = product[2]  # price from products table
    total_amount = unit_price * int(quantity)

    # Create PDF for purchasing bill
    custom_dir = "C:/Users/HP/mini_bills"
    os.makedirs(custom_dir, exist_ok=True)  # Create directory if it doesn't exist
    pdf_path = os.path.join(custom_dir, f"purchasing_bill_{datetime.date.today()}.pdf")
  
    pdf = pdf_canvas.Canvas(pdf_path, pagesize=letter)

    
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 750, f"Purchasing Bill - {datetime.date.today()}")
    pdf.drawString(50, 730, f"Product Name: {product_name}")
    pdf.drawString(50, 710, f"Product ID: {product_id}")
    pdf.drawString(50, 690, f"Quantity: {quantity}")
    pdf.drawString(50, 670, f"Unit Price: {unit_price}")
    pdf.drawString(50, 650, f"Total Amount: {total_amount}")
    pdf.save()

    # Show PDF
    messagebox.showinfo("Success", f"Purchasing Bill Generated: {pdf_path}")
    

#
def on_mark_received_click():
    order_id = order_id_entry.get()
    if not order_id:
        messagebox.showerror("Error", "Please enter Order ID.")
        return
    try:
        mark_order_as_received(int(order_id))
        messagebox.showinfo("Success", f"Order {order_id} marked as received.")
        order_id_entry.delete(0, 'end')
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Unexpected Error", str(e))


# UI Elements for placing stock order
ctk.CTkLabel(frame_inventory, text="Place Stock Order", font=("Helvetica", 20)).pack(pady=10)

stock_product_id = ctk.CTkEntry(frame_inventory, placeholder_text="Product ID")
stock_product_id.pack(pady=10)

stock_quantity = ctk.CTkEntry(frame_inventory, placeholder_text="Quantity")
stock_quantity.pack(pady=10)

ctk.CTkButton(frame_inventory, text="Place Order", command=place_stock_order).pack(pady=10)

order_id_entry = ctk.CTkEntry(frame_inventory, placeholder_text="Order ID to Mark as Received")
order_id_entry.pack(pady=10)
ctk.CTkButton(frame_inventory, text="Mark Order as Received", command=on_mark_received_click).pack(pady=10)

ctk.CTkButton(frame_inventory, text="Check Low Stock", command=check_low_stock).pack(pady=10)
ctk.CTkButton(frame_inventory, text="Generate Purchasing Bill", command=generate_purchasing_bill).pack(pady=10)

# ------------------ Product Catalog Frame ------------------ #

# Frame Setup
frame_products = ctk.CTkFrame(app)
frames["products"] = frame_products

ctk.CTkLabel(frame_products, text="Product Catalog", font=("Helvetica", 24)).pack(pady=10)

# Treeview Styling
style = ttk.Style()
style.configure("Treeview", background="#f5f5f5", foreground="black", rowheight=30,
                fieldbackground="#f5f5f5", font=("Segoe UI", 12))
style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"), background="#d9d9d9")

# Treeview + Scrollbar
table_frame = ctk.CTkFrame(master=frame_products)
table_frame.pack(pady=20)

tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Type", "Rate", "Quantity"), show='headings', height=10)
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.grid(row=0, column=0, sticky='nsew')
scrollbar.grid(row=0, column=1, sticky='ns')

# Configure headings
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Type", text="Type")
tree.heading("Rate", text="Rate (₹)")
tree.heading("Quantity", text="Available Qty")

# Configure columns
tree.column("ID", width=80, anchor='center')
tree.column("Name", width=200, anchor='w')
tree.column("Type", width=150, anchor='center')
tree.column("Rate", width=100, anchor='center')
tree.column("Quantity", width=130, anchor='center')

# Load products
def load_products():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT product_id, name, category, price, available_qty FROM products")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

load_products()

# ----------------- Form Frame (Add / Update / Delete) ----------------- #

form_frame = ctk.CTkFrame(frame_products)
form_widgets = []

def clear_form():
    for widget in form_widgets:
        widget.destroy()
    form_widgets.clear()

# ----------------- Add Product ----------------- #
def show_add_form():
    clear_form()
    form_frame.pack(pady=10)

    entries = {
        "ID": ctk.CTkEntry(form_frame, placeholder_text="Product ID", width=100),
        "Name": ctk.CTkEntry(form_frame, placeholder_text="Product Name", width=180),
        "Type": ctk.CTkEntry(form_frame, placeholder_text="Product Type", width=150),
        "Rate": ctk.CTkEntry(form_frame, placeholder_text="Rate", width=100),
        "Qty": ctk.CTkEntry(form_frame, placeholder_text="Available Quantity", width=120),
    }

    for i, entry in enumerate(entries.values()):
        entry.grid(row=0, column=i, padx=5, pady=5)
        form_widgets.append(entry)

    def submit_add():
        values = [e.get() for e in entries.values()]
        if not all(values):
            messagebox.showerror("Error", "Fill all fields to add product!")
            return
        try:
            cursor.execute(
                "INSERT INTO products (product_id, name, category, price, available_qty) VALUES (%s, %s, %s, %s, %s)",
                (values[0], values[1], values[2], float(values[3]), int(values[4]))
            )
            db.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            load_products()
            clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add product:\n{e}")

    add_btn = ctk.CTkButton(form_frame, text="Submit", command=submit_add)
    add_btn.grid(row=1, column=0, columnspan=5, pady=10)
    form_widgets.append(add_btn)

# ----------------- Update Product ----------------- #
def show_update_form():
    clear_form()
    form_frame.pack(pady=10)

    entries = {
        "ID": ctk.CTkEntry(form_frame, placeholder_text="Product ID", width=100),
        "Name": ctk.CTkEntry(form_frame, placeholder_text="Product Name", width=150),
        "Type": ctk.CTkEntry(form_frame, placeholder_text="Product Type", width=120),
        "Rate": ctk.CTkEntry(form_frame, placeholder_text="Rate", width=100),
        "Qty": ctk.CTkEntry(form_frame, placeholder_text="Available Quantity", width=130),
    }

    for i, entry in enumerate(entries.values()):
        entry.grid(row=0, column=i, padx=5)
        form_widgets.append(entry)

    def submit_update():
        pid, name, ptype, rate, qty = [e.get() for e in entries.values()]
        if not (pid and name and ptype and rate and qty):
            messagebox.showerror("Error", "Fill all fields to update product!")
            return
        try:
            cursor.execute(
                "UPDATE products SET name=%s,category =%s, price=%s, available_qty=%s WHERE product_id=%s",
                (name, ptype, float(rate), int(qty), pid)
            )
            db.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            load_products()
            clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update product:\n{e}")

    submit_btn = ctk.CTkButton(form_frame, text="Update", command=submit_update)
    submit_btn.grid(row=0, column=len(entries), padx=5)
    form_widgets.append(submit_btn)

# ----------------- Delete Product ----------------- #
def show_delete_form():
    clear_form()
    form_frame.pack(pady=10)

    id_entry = ctk.CTkEntry(form_frame, placeholder_text="Product ID", width=200)
    id_entry.grid(row=0, column=0, padx=10)

    def submit_delete():
        pid = id_entry.get()
        if not pid:
            messagebox.showerror("Error", "Enter Product ID to delete!")
            return
        try:
            cursor.execute("DELETE FROM products WHERE product_id=%s", (pid,))
            db.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
            load_products()
            clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete product:\n{e}")

    submit_btn = ctk.CTkButton(form_frame, text="Delete", command=submit_delete)
    submit_btn.grid(row=0, column=1, padx=10)

    form_widgets.extend([id_entry, submit_btn])

# ----------------- Search Product ----------------- #
search_frame = ctk.CTkFrame(master=frame_products)
search_frame.pack(pady=10)

ctk.CTkLabel(search_frame, text="Enter Product Name:").pack(side="left", padx=(0, 10))
search_entry = ctk.CTkEntry(search_frame, width=200)
search_entry.pack(side="left")

def search_product():
    product_name = search_entry.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    if product_name:
        cursor.execute("SELECT product_id, name,category, price, available_qty FROM products WHERE name LIKE %s", ("%" + product_name + "%",))
    else:
        cursor.execute("SELECT product_id, name, category,price, available_qty FROM products")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

ctk.CTkButton(search_frame, text="Search", command=search_product).pack(side="left", padx=(10, 0))

# ----------------- Action Buttons ----------------- #
btn_frame = ctk.CTkFrame(frame_products)
btn_frame.pack(pady=15)

ctk.CTkButton(btn_frame, text="Add Product", command=show_add_form).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="Update Product", command=show_update_form).grid(row=0, column=1, padx=10)
ctk.CTkButton(btn_frame, text="Delete Product", command=show_delete_form).grid(row=0, column=2, padx=10)



# Customer Management Frame (Admin)
frame_customers = ctk.CTkFrame(app)
frames["customers"] = frame_customers

ctk.CTkLabel(frame_customers, text="Customer Management", font=("Helvetica", 24)).pack(pady=20)

# Entry for Customer ID
cust_id_entry = ctk.CTkEntry(frame_customers, placeholder_text="Enter Customer ID")
cust_id_entry.pack(pady=10)

def view_customer_info_gui():
    cust_id = cust_id_entry.get()
    if not cust_id.isdigit():
        messagebox.showerror("Invalid Input", "Customer ID must be numeric.")
        return

    try:
        cursor.execute("SELECT * FROM customer WHERE cust_id = %s", (cust_id,))
        customer = cursor.fetchone()

        if customer:
            name = customer[1]
            phone = customer[2]
            visits = customer[3]
            last_date = customer[4]
            credits = customer[5]

            if isinstance(last_date, str):
                last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()

            days_retained = (datetime.date.today() - last_date).days

            info = f"""
Name: {name}
Phone: {phone}
Visits: {visits}
Last Transaction: {last_date}
Days Since Last Visit: {days_retained}
Credits: ₹{credits}
            """

            discount_msg = ""
            if visits >= 5 or days_retained > 10:
                discount_msg = "\n🎁 Eligible for Discount Coupon: ₹50 credited!"
                cursor.execute("UPDATE customer SET credits = credits + 50 WHERE cust_id = %s", (cust_id,))
                db.commit()

            messagebox.showinfo("Customer Info", info + discount_msg)
        else:
            messagebox.showwarning("Not Found", "Customer ID not found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


    cursor.close()
    db.close()

# View Info Button
view_info_btn = ctk.CTkButton(frame_customers, text="View Customer Info", command=view_customer_info_gui)
view_info_btn.pack(pady=10)

#--------------- Setting (Admin)--------------------

# Frame for Settings
frame_setting = ctk.CTkFrame(app)
frames["setting"] = frame_setting

ctk.CTkLabel(frame_setting, text="Settings", font=("Helvetica", 24)).pack(pady=20)

# Buttons
ctk.CTkButton(frame_setting, text="Change Password", command=lambda: show_change_password()).pack(pady=10)
ctk.CTkButton(frame_setting, text="Change Authority", command=lambda: show_change_authority()).pack(pady=10)
ctk.CTkButton(frame_setting, text="Add Employee", command=lambda: show_add_employee()).pack(pady=10)
ctk.CTkButton(frame_setting, text="Delete Employee", command=lambda: show_delete_employee()).pack(pady=10)

# Frame to hold dynamic content inside settings
frame_setting_content = ctk.CTkFrame(frame_setting)
frame_setting_content.pack(pady=20)

# Clear dynamic content
def clear_setting_content():
    for widget in frame_setting_content.winfo_children():
        widget.destroy()

# Show Change Password Section
def show_change_password():
    clear_setting_content()

    ctk.CTkLabel(frame_setting_content, text="Change User Password", font=("Helvetica", 18)).pack(pady=10)

    username_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="Username")
    username_entry.pack(pady=5)

    new_pass_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="New Password", show="*")
    new_pass_entry.pack(pady=5)

    confirm_pass_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="Confirm New Password", show="*")
    confirm_pass_entry.pack(pady=5)

    def update_password():
        username = username_entry.get()
        new_password = new_pass_entry.get()
        confirm_password = confirm_pass_entry.get()

        if not username or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        cursor.execute("SELECT * FROM users WHERE u_name = %s", (username,))
        user = cursor.fetchone()

        if not user:
            messagebox.showerror("Error", "Username not found!")
            return

        cursor.execute("UPDATE users SET pass = %s WHERE u_name = %s", (new_password, username))
        db.commit()
        messagebox.showinfo("Success", f"Password updated for {username}!")

    ctk.CTkButton(frame_setting_content, text="Update Password", command=update_password).pack(pady=10)

# Show Change Authority Section
def show_change_authority():
    clear_setting_content()

    ctk.CTkLabel(frame_setting_content, text="Change User Authority", font=("Helvetica", 18)).pack(pady=10)

    username_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="Username")
    username_entry.pack(pady=5)

    authority_dropdown = ctk.CTkComboBox(frame_setting_content, values=["Admin", "Cashier"])
    authority_dropdown.pack(pady=5)

    def update_authority():
        username = username_entry.get()
        new_role = authority_dropdown.get()

        if not username or not new_role:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        cursor.execute("SELECT * FROM users WHERE u_name = %s", (username,))
        user = cursor.fetchone()

        if not user:
            messagebox.showerror("Error", "Username not found!")
            return

        cursor.execute("UPDATE users SET role = %s WHERE u_name = %s", (new_role, username))
        db.commit()
        messagebox.showinfo("Success", f"Authority updated to {new_role} for {username}!")

    ctk.CTkButton(frame_setting_content, text="Update Authority", command=update_authority).pack(pady=10)

# Show Add Employee Section
def show_add_employee():
    clear_setting_content()

    ctk.CTkLabel(frame_setting_content, text="Add New Employee", font=("Helvetica", 18)).pack(pady=10)

    username_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="Username")
    username_entry.pack(pady=5)

    password_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="Password", show="*")
    password_entry.pack(pady=5)

    role_dropdown = ctk.CTkComboBox(frame_setting_content, values=["Admin", "Cashier"])
    role_dropdown.pack(pady=5)

    def add_employee():
        username = username_entry.get()
        password = password_entry.get()
        role = role_dropdown.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        cursor.execute("SELECT * FROM users WHERE u_name = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists!")
            return

        cursor.execute("INSERT INTO users (u_name, pass, role) VALUES (%s, %s, %s)", (username, password, role))
        db.commit()
        messagebox.showinfo("Success", f"Employee {username} added as {role}!")

    ctk.CTkButton(frame_setting_content, text="Add Employee", command=add_employee).pack(pady=10)

# Show Delete Employee Section
def show_delete_employee():
    clear_setting_content()

    ctk.CTkLabel(frame_setting_content, text="Delete Employee", font=("Helvetica", 18)).pack(pady=10)

    username_entry = ctk.CTkEntry(frame_setting_content, placeholder_text="Username")
    username_entry.pack(pady=5)

    def delete_employee():
        username = username_entry.get()

        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return

        cursor.execute("SELECT * FROM users WHERE u_name = %s", (username,))
        user = cursor.fetchone()

        if not user:
            messagebox.showerror("Error", "Username not found!")
            return

        cursor.execute("DELETE FROM users WHERE u_name = %s", (username,))
        db.commit()
        messagebox.showinfo("Success", f"Employee {username} deleted!")

    ctk.CTkButton(frame_setting_content, text="Delete Employee", command=delete_employee).pack(pady=10)

# ------------------ DEFAULT VIEW ------------------
show_frame("admin_login")

app.mainloop()
