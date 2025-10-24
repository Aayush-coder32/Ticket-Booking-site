import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random

# -------------------------
# Fare data and helpers
# -------------------------
station_distance = {
    ("Delhi", "Mumbai"): 1400,
    ("Delhi", "Kolkata"): 1500,
    ("Delhi", "Chennai"): 2200,
    ("Delhi", "Bangalore"): 2150,
    ("Mumbai", "Chennai"): 1300,
    ("Kolkata", "Chennai"): 1650,
    ("Jaipur", "Delhi"): 280,
    ("Mumbai", "Jaipur"): 1150,
    ("Bangalore", "Kolkata"): 1850,
    ("Bangalore", "Chennai"): 350,
}

base_fares = {
    "Sleeper": 1.2,     # ₹ per km
    "AC 3-Tier": 2.5,
    "AC 2-Tier": 3.5,
    "First Class": 5.0
}


def calculate_fare(source, dest, seat_class):
    dist = station_distance.get((source, dest)) or station_distance.get((dest, source))
    if not dist:
        return None
    fare = dist * base_fares[seat_class]
    return round(fare, 2)


# -------------------------
# PDF Ticket Generator
# -------------------------
def generate_pdf(name, age, source, dest, train, date, seat_class, fare, seat_no, coach):
    c = canvas.Canvas(f"{name}_Train_Ticket.pdf", pagesize=A4)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(180, 780, "🚆 Indian Railways E-Ticket")

    c.setFont("Helvetica", 13)
    c.drawString(100, 730, f"Passenger Name: {name}")
    c.drawString(100, 710, f"Age: {age}")
    c.drawString(100, 690, f"Train: {train}")
    c.drawString(100, 670, f"Class: {seat_class}")
    c.drawString(100, 650, f"From: {source}")
    c.drawString(100, 630, f"To: {dest}")
    c.drawString(100, 610, f"Date of Journey: {date}")
    c.drawString(100, 590, f"Coach: {coach}    Seat No: {seat_no}")
    c.drawString(100, 570, f"Total Fare: ₹ {fare}")

    c.setFont("Helvetica-Oblique", 12)
    c.drawString(100, 530, "Have a pleasant and safe journey!")
    c.save()


# -------------------------
# Main Booking Function
# -------------------------
def book_ticket():
    name = name_var.get()
    age = age_var.get()
    source = source_var.get()
    dest = dest_var.get()
    train = train_var.get()
    date = date_var.get()
    seat_class = class_var.get()

    if not all([name, age, source, dest, train, date, seat_class]):
        messagebox.showwarning("Missing Info", "Please fill all fields!")
        return

    if source == dest:
        messagebox.showerror("Invalid Route", "Source and destination cannot be the same!")
        return

    fare = calculate_fare(source, dest, seat_class)
    if fare is None:
        messagebox.showwarning("Route Not Found", "No route data found for this journey.")
        return

    seat_no = random.randint(1, 72)
    coach = random.choice(["S1", "S2", "B1", "A1", "FC1"])

    summary = (
        f"Passenger: {name}\n"
        f"Age: {age}\n"
        f"Train: {train}\n"
        f"From: {source} ➜ {dest}\n"
        f"Date: {date}\n"
        f"Class: {seat_class}\n"
        f"Coach: {coach}, Seat: {seat_no}\n"
        f"Fare: ₹{fare}\n\nConfirm booking?"
    )

    confirm = messagebox.askyesno("Confirm Ticket", summary)
    if confirm:
        generate_pdf(name, age, source, dest, train, date, seat_class, fare, seat_no, coach)
        messagebox.showinfo("Success", f"Ticket booked successfully!\nSaved as {name}_Train_Ticket.pdf")
        clear_fields()


def clear_fields():
    for var in [name_var, age_var, source_var, dest_var, train_var, date_var, class_var]:
        var.set("")


# -------------------------
# GUI Design
# -------------------------
root = tk.Tk()
root.title("IRCTC Mini Train Booking System")
root.geometry("600x650")
root.configure(bg="#eaf3ff")

title = tk.Label(root, text="🚄 IRCTC Mini Train Booking", font=("Helvetica", 22, "bold"),
                 bg="#007acc", fg="white", pady=10)
title.pack(fill="x")

# Variables
name_var = tk.StringVar()
age_var = tk.StringVar()
source_var = tk.StringVar()
dest_var = tk.StringVar()
train_var = tk.StringVar()
date_var = tk.StringVar()
class_var = tk.StringVar()

frame = tk.Frame(root, bg="#eaf3ff", padx=20, pady=20)
frame.pack(pady=10)

# Entry fields
fields = [
    ("Passenger Name:", name_var),
    ("Age:", age_var),
    ("Date (DD/MM/YYYY):", date_var)
]

for i, (label, var) in enumerate(fields):
    tk.Label(frame, text=label, font=("Helvetica", 12, "bold"), bg="#eaf3ff").grid(row=i, column=0, sticky="w", pady=8)
    tk.Entry(frame, textvariable=var, font=("Helvetica", 12), width=25).grid(row=i, column=1, pady=8)

# Dropdowns
stations = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Jaipur"]
trains = ["Rajdhani Express", "Shatabdi Express", "Duronto Express", "Vande Bharat", "Garib Rath"]
classes = list(base_fares.keys())

tk.Label(frame, text="Source Station:", font=("Helvetica", 12, "bold"), bg="#eaf3ff").grid(row=3, column=0, sticky="w", pady=8)
ttk.Combobox(frame, textvariable=source_var, values=stations, font=("Helvetica", 12), width=23, state="readonly").grid(row=3, column=1)

tk.Label(frame, text="Destination:", font=("Helvetica", 12, "bold"), bg="#eaf3ff").grid(row=4, column=0, sticky="w", pady=8)
ttk.Combobox(frame, textvariable=dest_var, values=stations, font=("Helvetica", 12), width=23, state="readonly").grid(row=4, column=1)

tk.Label(frame, text="Select Train:", font=("Helvetica", 12, "bold"), bg="#eaf3ff").grid(row=5, column=0, sticky="w", pady=8)
ttk.Combobox(frame, textvariable=train_var, values=trains, font=("Helvetica", 12), width=23, state="readonly").grid(row=5, column=1)

tk.Label(frame, text="Seat Class:", font=("Helvetica", 12, "bold"), bg="#eaf3ff").grid(row=6, column=0, sticky="w", pady=8)
ttk.Combobox(frame, textvariable=class_var, values=classes, font=("Helvetica", 12), width=23, state="readonly").grid(row=6, column=1)

# Buttons
btn_frame = tk.Frame(root, bg="#eaf3ff")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Book Ticket", bg="#007acc", fg="white",
          font=("Helvetica", 14, "bold"), width=15, command=book_ticket).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Clear", bg="gray", fg="white",
          font=("Helvetica", 14, "bold"), width=10, command=clear_fields).grid(row=0, column=1, padx=10)

root.mainloop()
