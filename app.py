import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re
from datetime import datetime
import database


class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Manager")
        self.root.geometry("300x250")

        # Initialize database
        database.initialize_db()

        # Create the Appointments LabelFrame for Treeview, filter input, and Add Appointment button
        self.appointments_frame = tk.LabelFrame(root, text="Appointments", padx=10, pady=10)
        self.appointments_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)


        # Add Appointment button
        self.add_appointment_button = tk.Button(self.appointments_frame, text="Add appointment", command=self.add_appointment)
        self.add_appointment_button.pack(fill=tk.BOTH, pady=5)

        # Delete appointments button
        delete_button = tk.Button(self.appointments_frame, text="Delete appointments", command=self.open_delete_window)
        delete_button.pack(fill=tk.BOTH, pady=5)

        # Edit appointments button
        edit_button = tk.Button(self.appointments_frame, text="Edit appointments", command=self.open_edit_window)
        edit_button.pack(fill=tk.BOTH, pady=5)

        # Show appointments button
        show_button = tk.Button(self.appointments_frame, text="Show appointments", command=self.open_show_window)
        show_button.pack(fill=tk.BOTH, pady=5)

        busy_hours_button = tk.Button(self.appointments_frame, text="Show Busy hours", command=self.open_busy_window)
        busy_hours_button.pack(fill=tk.BOTH, pady=5)


    def add_appointment(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Appointment")
        add_window.geometry("300x330")

        tk.Label(add_window, text="Name:").pack(anchor=tk.W, padx=10, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(add_window, text="Date:").pack(anchor=tk.W, padx=10, pady=5)
        date_picker = DateEntry(add_window, date_pattern="yyyy-mm-dd")
        date_picker.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(add_window, text="Hour:").pack(anchor=tk.W, padx=10, pady=5)
        hour_var = tk.StringVar(add_window)
        hour_dropdown = ttk.Combobox(add_window, textvariable=hour_var, state="readonly")
        hour_dropdown["values"] = [f"{hour:02}" for hour in range(9, 19)]  # Hours from 9 to 18 (9 AM to 6 PM)
        hour_dropdown.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(add_window, text="Minute:").pack(anchor=tk.W, padx=10, pady=5)
        minute_var = tk.StringVar(add_window)
        minute_dropdown = ttk.Combobox(add_window, textvariable=minute_var, state="readonly")
        minute_dropdown["values"] = [f"{minute:02}" for minute in range(0, 60, 15)]  # Minutes from 0 to 59
        minute_dropdown.pack(fill=tk.X, padx=10, pady=5)

        def save_appointment():
            name = name_entry.get().strip()
            date = date_picker.get_date()
            hour = hour_var.get()
            minute = minute_var.get()
            if len(name) < 2:
                messagebox.showerror("Validation Error", "Name must be longer.")
                return
            if not re.match(r"^[a-zA-Z\s]+$", name):
                messagebox.showerror("Validation Error", "Name must contain only letters.")
                return

            if not hour or not minute:
                messagebox.showerror("Validation Error", "Please select a valid time.")
                return

            try:
                appointment_time = datetime.strptime(f"{date} {hour}:{minute}:00", "%Y-%m-%d %H:%M:%S")
                database.add_appointment(name, appointment_time)
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(add_window, text="Save", command=save_appointment).pack(pady=10)

    def open_delete_window(self):
        """Open a new window for editing (deleting) appointments."""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Delete Appointments")
        edit_window.geometry("300x150")

        # Dropdown for selecting a name
        tk.Label(edit_window, text="Select Appointment to Delete:").pack(pady=10)
        names = [row[0] for row in database.fetch_appointments()]  # Fetch all names
        name_dropdown = ttk.Combobox(edit_window, values=names, state="readonly", width=25)
        name_dropdown.pack(fill=tk.X, padx=10, pady=10)

        # Delete button
        def delete_selected_appointment():
            selected_name = name_dropdown.get()
            if not selected_name:
                messagebox.showwarning("Warning", "Please select an appointment.")
                return

            # Call the database function to delete the selected name
            database.delete_appointment(selected_name)
            messagebox.showinfo("Success", f"Appointment for '{selected_name}' deleted.")
            edit_window.destroy()  # Close the edit window

        delete_button = tk.Button(edit_window, text="Delete", command=delete_selected_appointment)
        delete_button.pack(fill=tk.X, padx=10, pady=10)

    def open_edit_window(self):
        """Open a new window for editing appointment times."""
        edit_window  = tk.Toplevel(self.root)
        edit_window .title("Edit Appointment")
        edit_window .geometry("300x390")

        # Dropdown to select a name
        tk.Label(edit_window, text="Select customer:").pack(anchor=tk.W, padx=5, pady=5)
        names = [row[0] for row in database.fetch_appointments()]  # Fetch all names
        name_dropdown = ttk.Combobox(edit_window, values=names, state="readonly", width=30)
        name_dropdown.pack(fill=tk.X, padx=5, pady=5)

        edit_appointments_frame = tk.LabelFrame(edit_window, text="New date and time", padx=10, pady=10)
        edit_appointments_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)


        tk.Label(edit_appointments_frame , text="Date:").pack(anchor=tk.W, padx=5, pady=5)
        date_picker = DateEntry(edit_appointments_frame , date_pattern="yyyy-mm-dd")
        date_picker.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(edit_appointments_frame , text="Hour:").pack(anchor=tk.W, padx=5, pady=5)
        hour_var = tk.StringVar(edit_appointments_frame)
        hour_dropdown = ttk.Combobox(edit_appointments_frame , textvariable=hour_var, state="readonly")
        hour_dropdown["values"] = [f"{hour:02}" for hour in range(9, 19)]  # Hours from 9 to 18 (9 AM to 6 PM)
        hour_dropdown.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(edit_appointments_frame , text="Minute:").pack(anchor=tk.W, padx=5, pady=5)
        minute_var = tk.StringVar(edit_appointments_frame )
        minute_dropdown = ttk.Combobox(edit_appointments_frame , textvariable=minute_var, state="readonly")
        minute_dropdown["values"] = [f"{minute:02}" for minute in range(0, 60, 15)]  # Minutes from 0 to 59
        minute_dropdown.pack(fill=tk.X, padx=5, pady=5)

        # Function to edit the appointment
        def edit_appointment():
            selected_name = name_dropdown.get()
            selected_date = date_picker.get_date()
            selected_hour = hour_var.get()
            selected_minute = minute_var.get()

            if not selected_name or not selected_date or not selected_hour or not selected_minute:
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return

            # Combine selected date and time
            new_time = f"{selected_date} {selected_hour}:{selected_minute}:00"

            # Validate the new time
            if database.check_appointment_time(new_time):
                messagebox.showerror("Error", f"The time '{new_time}' is already taken.")
                return

            # Update the database
            database.update_appointment_time(selected_name, new_time)
            messagebox.showinfo("Success", f"Appointment for '{selected_name}' updated.")
            edit_window.destroy()  # Close the edit window

        # Edit button
        edit_button = tk.Button(edit_appointments_frame, text="Edit Appointment", command=edit_appointment)
        edit_button.pack(fill=tk.X, pady=10)

    def open_show_window(self):
        """Open a new window for editing appointment times."""
        show_window  = tk.Toplevel(self.root)
        show_window .title("List of appointments")
        show_window .geometry("400x500")



        # Treeview for displaying appointments
        treeview = ttk.Treeview(show_window, columns=("Name", "Time"), show="headings")
        treeview.heading("Name", text="Name")
        treeview.heading("Time", text="Time")

        # Scrollbar for Treeview
        treeview_scroll = ttk.Scrollbar(treeview, orient="vertical", command=treeview.yview)
        treeview.config(yscrollcommand=treeview_scroll.set)

        treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        treeview_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_treeview():
            # Clear the Treeview
            for row in treeview.get_children():
                treeview.delete(row)

            # Fetch all appointments from the database
            appointments = database.fetch_appointments()

            # Insert all appointments into the Treeview
            for name, time in appointments:
                treeview.insert("", "end", values=(name, time))

        refresh_treeview()

        # Filter button
        filter_button = tk.Button(show_window, text="Refresh table", command=refresh_treeview)
        filter_button.pack(fill=tk.BOTH, padx=5, pady=5)

        # Filter by Name input field
        filter_label = tk.Label(show_window, text="Filter by Name:")
        filter_label.pack(anchor=tk.W, padx=5, pady=5)

        filter_entry = tk.Entry(show_window)
        filter_entry.pack(fill=tk.BOTH, padx=5, pady=5)

        def load_appointments():
            # Clear the existing entries in the Treeview
            for row in treeview.get_children():
                treeview.delete(row)

            # Fetch appointments from the database
            appointments = database.fetch_appointments()

            # Insert fetched appointments into the Treeview
            for name, time in appointments:
                treeview.insert("", "end", values=(name, time))

        load_appointments()



        def filter_table():
            # Clear the existing Treeview
            for row in treeview.get_children():
                treeview.delete(row)

            # Get the filter text
            filter_text = filter_entry.get().lower()

            # Fetch all appointments from the database
            appointments = database.fetch_appointments()

            # Filter the appointments by name (case-insensitive)
            filtered_appointments = [
                (name, time) for name, time in appointments if filter_text in name.lower()
            ]

            # Insert the filtered data into the Treeview
            for name, time in filtered_appointments:
                treeview.insert("", "end", values=(name, time))



        # Filter button
        filter_button = tk.Button(show_window, text="Filter", command=filter_table)
        filter_button.pack(fill=tk.BOTH, padx=5, pady=5)

    def open_busy_window(self):
        """Open a new window for editing appointment times."""
        busy_window = tk.Toplevel(self.root)
        busy_window.title("Busy hours")
        busy_window.geometry("600x700")

        # Create the Busy Hours LabelFrame for Date Picker and Graph
        busy_hours_frame = tk.LabelFrame(busy_window, text="Busy Hours", padx=10, pady=10)
        busy_hours_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=10)

        # Date Picker inside the Busy Hours frame
        date_label = tk.Label(busy_hours_frame, text="Select Date:")
        date_label.pack(anchor=tk.W, pady=5)

        date_picker = DateEntry(busy_hours_frame, date_pattern="yyyy-mm-dd", width=10)
        date_picker.pack(fill=tk.X, pady=5)

        def show_graph():
            selected_date = date_picker.get_date()

            # Convert selected_date to datetime to match the database format
            start_of_day = datetime.combine(selected_date, datetime.min.time())
            end_of_day = datetime.combine(selected_date, datetime.max.time())

            # Fetch appointments for the selected date
            appointments = database.fetch_appointments()
            filtered_appointments = [
                (name, time) for name, time in appointments
                if start_of_day <= datetime.strptime(time, "%Y-%m-%d %H:%M:%S") <= end_of_day
            ]

            if not filtered_appointments:
                messagebox.showinfo("No Appointments", "No appointments found for the selected date.")
                return

            # Make the graph visible by packing the canvas
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Update the graph with filtered appointments
            update_graph(filtered_appointments)

        # Button to show the graph
        show_graph_button = tk.Button(busy_hours_frame, text="Show Graph", command=show_graph)
        show_graph_button.pack(fill=tk.X, pady=5)

        # Frame for the graph itself (Initially hidden)
        graph_frame = tk.Frame(busy_hours_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Set up the figure and canvas for the plot
        figure = Figure(figsize=(5, 3), dpi=100)
        ax = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, graph_frame)

        # Initially hide the graph
        canvas.get_tk_widget().pack_forget()

        def update_graph(appointments):
            ax.clear()
            hours = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S").hour for _, time in appointments]
            hour_counts = {hour: hours.count(hour) for hour in range(9, 19)}  # Only show from 9 AM to 6 PM

            ax.bar(hour_counts.keys(), hour_counts.values())
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Number of Appointments")

            # Ensure there is no title on the graph itself
            ax.set_title("")  # Clear title text

            # Redraw the canvas
            canvas.draw()






if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()
