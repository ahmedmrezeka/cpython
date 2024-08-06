import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store the data
DATA_FILE = "accounting_data.json"

def load_data():
    """Load data from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_data(data):
    """Save data to a JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def add_entry():
    """Add a new entry to the list and update total."""
    try:
        amount = float(amount_entry.get())
        description = description_entry.get()
        if description:
            entry = {"description": description, "amount": amount}
            data.append(entry)
            listbox.insert(tk.END, f"{description}: ${amount:.2f}")
            update_total()
            amount_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)
            save_data(data)
        else:
            messagebox.showwarning("Input Error", "Please enter a description.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid amount.")

def update_total():
    """Update the total amount."""
    total = sum(entry["amount"] for entry in data)
    total_label.config(text=f"Total: ${total:.2f}")

def clear_entries():
    """Clear the input fields."""
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

def delete_entry():
    """Delete the selected entry from the list and update total."""
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        del data[selected_index]
        update_total()
        save_data(data)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select an entry to delete.")

def reset_data():
    """Reset all data and clear the listbox and total."""
    global data
    data = []
    listbox.delete(0, tk.END)
    update_total()
    save_data(data)

# Initialize the main window
window = tk.Tk()
window.title("Accounting Program")

# Initialize data
data = load_data()

# Create and place widgets
tk.Label(window, text="Description:").grid(row=0, column=0, padx=5, pady=5)
description_entry = tk.Entry(window, width=30)
description_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(window, width=30)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(window, text="Add Entry", command=add_entry).grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(window, text="Clear", command=clear_entries).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(window, text="Delete Selected", command=delete_entry).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(window, text="Reset All", command=reset_data).grid(row=5, column=0, columnspan=2, pady=10)

listbox = tk.Listbox(window, width=50, height=10)
listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

total_label = tk.Label(window, text="Total: $0.00")
total_label.grid(row=7, column=0, columnspan=2, pady=10)

# Populate the listbox with saved data
for entry in data:
    listbox.insert(tk.END, f"{entry['description']}: ${entry['amount']:.2f}")

update_total()

# Run the application
window.mainloop()
