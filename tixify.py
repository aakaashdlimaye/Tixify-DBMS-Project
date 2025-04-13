import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from db_config import get_db_connection
from datetime import datetime

class TixifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tixify - Event Booking Platform")
        self.root.geometry("800x600")
        
        # Initialize database connection
        self.conn = get_db_connection()
        self.current_user = None
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Show login screen initially
        self.show_login_screen()
    
    def show_login_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Login form
        ttk.Label(self.main_frame, text="Login to Tixify", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="Email:").grid(row=1, column=0, pady=5)
        self.email_entry = ttk.Entry(self.main_frame, width=30)
        self.email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.main_frame, text="Password:").grid(row=2, column=0, pady=5)
        self.password_entry = ttk.Entry(self.main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.main_frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Register", command=self.show_register_screen).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.main_frame, text="Admin Login", command=self.show_admin_login).grid(row=5, column=0, columnspan=2, pady=5)
    
    def show_register_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Registration form
        ttk.Label(self.main_frame, text="Register for Tixify", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="Name:").grid(row=1, column=0, pady=5)
        self.reg_name_entry = ttk.Entry(self.main_frame, width=30)
        self.reg_name_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.main_frame, text="Email:").grid(row=2, column=0, pady=5)
        self.reg_email_entry = ttk.Entry(self.main_frame, width=30)
        self.reg_email_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.main_frame, text="Phone:").grid(row=3, column=0, pady=5)
        self.reg_phone_entry = ttk.Entry(self.main_frame, width=30)
        self.reg_phone_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(self.main_frame, text="Password:").grid(row=4, column=0, pady=5)
        self.reg_password_entry = ttk.Entry(self.main_frame, width=30, show="*")
        self.reg_password_entry.grid(row=4, column=1, pady=5)
        
        ttk.Button(self.main_frame, text="Register", command=self.register).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Back to Login", command=self.show_login_screen).grid(row=6, column=0, columnspan=2, pady=5)
    
    def show_admin_login(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Admin login form
        ttk.Label(self.main_frame, text="Admin Login", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="Email:").grid(row=1, column=0, pady=5)
        self.admin_email_entry = ttk.Entry(self.main_frame, width=30)
        self.admin_email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.main_frame, text="Password:").grid(row=2, column=0, pady=5)
        self.admin_password_entry = ttk.Entry(self.main_frame, width=30, show="*")
        self.admin_password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.main_frame, text="Login", command=self.admin_login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_frame, text="Back to User Login", command=self.show_login_screen).grid(row=4, column=0, columnspan=2, pady=5)
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM User WHERE Email = %s AND Password = %s", (email, password))
                user = cursor.fetchone()
                
                if user:
                    self.current_user = user
                    self.show_user_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid email or password")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def register(self):
        name = self.reg_name_entry.get()
        email = self.reg_email_entry.get()
        phone = self.reg_phone_entry.get()
        password = self.reg_password_entry.get()
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("INSERT INTO User (Name, Email, Phone, Password) VALUES (%s, %s, %s, %s)",
                             (name, email, phone, password))
                self.conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def admin_login(self):
        email = self.admin_email_entry.get()
        password = self.admin_password_entry.get()
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Admin WHERE Email = %s AND Password = %s", (email, password))
                admin = cursor.fetchone()
                
                if admin:
                    self.show_admin_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid admin credentials")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_user_dashboard(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Check if user is logged in
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            self.show_login_screen()
            return
        
        # Welcome message
        ttk.Label(self.main_frame, text=f"Welcome, {self.current_user['Name']}!", font=("Arial", 16)).pack(pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=10)
        
        # User profile button
        ttk.Button(buttons_frame, text="My Profile", command=self.show_user_profile).pack(side="left", padx=5)
        
        # Other buttons
        ttk.Button(buttons_frame, text="View Events", command=self.show_events).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="My Bookings", command=self.show_my_bookings).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Logout", command=self.logout).pack(side="left", padx=5)

    def show_user_profile(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Check if user is logged in
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            self.show_login_screen()
            return
        
        # --- Scroll setup ---
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        # ---------------------
        
        # Title and edit button
        title_frame = ttk.Frame(scrollable_frame)
        title_frame.pack(pady=10, fill="x")
        
        ttk.Label(title_frame, text="My Profile", font=("Arial", 16)).pack(side="left")
        ttk.Button(title_frame, text="Edit Profile", command=self.show_edit_profile).pack(side="right", padx=5)
        
        # Get user's loyalty points
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT LoyaltyPoints FROM User WHERE UserID = %s", (self.current_user['UserID'],))
                user_points = cursor.fetchone()['LoyaltyPoints']
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch loyalty points")
            return
        
        # Create profile frame
        profile_frame = ttk.Frame(scrollable_frame, padding="20")
        profile_frame.pack(pady=10)
        
        # User details
        ttk.Label(profile_frame, text=f"Name: {self.current_user['Name']}", font=("Arial", 12)).pack(pady=5)
        ttk.Label(profile_frame, text=f"Email: {self.current_user['Email']}", font=("Arial", 12)).pack(pady=5)
        ttk.Label(profile_frame, text=f"Phone: {self.current_user['Phone']}", font=("Arial", 12)).pack(pady=5)
        ttk.Label(profile_frame, text=f"Loyalty Points: {user_points}", font=("Arial", 12)).pack(pady=5)
        
        # Get booking statistics
        try:
            with self.conn.cursor() as cursor:
                # Total bookings
                cursor.execute("""
                    SELECT COUNT(*) as total_bookings, 
                           SUM(TotalPrice) as total_spent
                    FROM Booking 
                    WHERE UserID = %s
                """, (self.current_user['UserID'],))
                stats = cursor.fetchone()
                
                ttk.Label(profile_frame, text=f"Total Bookings: {stats['total_bookings']}", font=("Arial", 12)).pack(pady=5)
                ttk.Label(profile_frame, text=f"Total Spent: ₹{stats['total_spent']:.2f}", font=("Arial", 12)).pack(pady=5)
                
                # Recent bookings
                cursor.execute("""
                    SELECT b.*, e.Title, e.StartDate
                    FROM Booking b
                    JOIN Event e ON b.EventID = e.EventID
                    WHERE b.UserID = %s
                    ORDER BY b.BookingDate DESC
                    LIMIT 5
                """, (self.current_user['UserID'],))
                recent_bookings = cursor.fetchall()
                
                if recent_bookings:
                    ttk.Label(profile_frame, text="Recent Bookings:", font=("Arial", 12, "bold")).pack(pady=10)
                    
                    for booking in recent_bookings:
                        booking_frame = ttk.Frame(profile_frame)
                        booking_frame.pack(pady=5, padx=5, fill="x")
                        
                        ttk.Label(booking_frame, text=f"Event: {booking['Title']}").pack(anchor="w")
                        ttk.Label(booking_frame, text=f"Date: {booking['StartDate'].strftime('%d-%m-%Y')}").pack(anchor="w")
                        ttk.Label(booking_frame, text=f"Amount: ₹{booking['TotalPrice']}").pack(anchor="w")
                        ttk.Label(booking_frame, text=f"Status: {booking['PaymentStatus']}").pack(anchor="w")
                        
                        # Add separator
                        ttk.Separator(profile_frame, orient="horizontal").pack(fill="x", pady=5)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        # Back button
        ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_user_dashboard).pack(pady=10)

    def show_edit_profile(self):
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("400x500")

        # --- Scroll setup ---
        canvas = tk.Canvas(edit_window)
        scrollbar = ttk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # ---------------------

        # Create main frame with padding
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="Edit Profile", font=("Arial", 16)).pack(pady=10)

        # Form fields
        ttk.Label(main_frame, text="Name:").pack(pady=5)
        name_var = tk.StringVar(value=self.current_user['Name'])
        name_entry = ttk.Entry(main_frame, textvariable=name_var, width=30)
        name_entry.pack(pady=5)

        ttk.Label(main_frame, text="Email:").pack(pady=5)
        email_var = tk.StringVar(value=self.current_user['Email'])
        email_entry = ttk.Entry(main_frame, textvariable=email_var, width=30)
        email_entry.pack(pady=5)

        ttk.Label(main_frame, text="Phone:").pack(pady=5)
        phone_var = tk.StringVar(value=self.current_user['Phone'])
        phone_entry = ttk.Entry(main_frame, textvariable=phone_var, width=30)
        phone_entry.pack(pady=5)

        ttk.Label(main_frame, text="New Password (leave blank to keep current):").pack(pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=password_var, width=30, show="*")
        password_entry.pack(pady=5)

        ttk.Label(main_frame, text="Confirm New Password:").pack(pady=5)
        confirm_password_var = tk.StringVar()
        confirm_password_entry = ttk.Entry(main_frame, textvariable=confirm_password_var, width=30, show="*")
        confirm_password_entry.pack(pady=5)

        def save_changes():
            try:
                # Validate inputs
                name = name_var.get().strip()
                email = email_var.get().strip()
                phone = phone_var.get().strip()
                new_password = password_var.get()
                confirm_password = confirm_password_var.get()

                if not name or not email or not phone:
                    raise ValueError("All fields are required")

                if new_password and new_password != confirm_password:
                    raise ValueError("Passwords do not match")

                # Check if email is already taken by another user
                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT UserID FROM User 
                        WHERE Email = %s AND UserID != %s
                    """, (email, self.current_user['UserID']))
                    if cursor.fetchone():
                        raise ValueError("Email is already taken by another user")

                    # Update user information
                    if new_password:
                        cursor.execute("""
                            UPDATE User 
                            SET Name = %s, Email = %s, Phone = %s, Password = %s
                            WHERE UserID = %s
                        """, (name, email, phone, new_password, self.current_user['UserID']))
                    else:
                        cursor.execute("""
                            UPDATE User 
                            SET Name = %s, Email = %s, Phone = %s
                            WHERE UserID = %s
                        """, (name, email, phone, self.current_user['UserID']))
                    
                    self.conn.commit()

                    # Update current user data
                    self.current_user['Name'] = name
                    self.current_user['Email'] = email
                    self.current_user['Phone'] = phone

                    messagebox.showinfo("Success", "Profile updated successfully!")
                    edit_window.destroy()
                    self.show_user_profile()  # Refresh profile view

            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        ttk.Button(main_frame, text="Save Changes", command=save_changes).pack(pady=20)
        ttk.Button(main_frame, text="Cancel", command=edit_window.destroy).pack(pady=5)
    
    def show_events(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # --- Scroll setup ---
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        # ---------------------

        # Search button
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        ttk.Button(search_frame, text="Advanced Search", 
                  command=self.show_search_window).pack(side="right", padx=5)
        
        # Events list
        ttk.Label(scrollable_frame, text="Available Events", font=("Arial", 16)).pack(pady=10)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT e.*, c.Name as CategoryName, p.Name as ProviderName,
                           v.Name as VenueName,
                           DATE_FORMAT(e.StartDate, '%Y-%m-%d') as FormattedDate,
                           TIME_FORMAT(e.StartDate, '%H:%i') as FormattedTime
                    FROM Event e
                    LEFT JOIN Category c ON e.CategoryID = c.CategoryID
                    LEFT JOIN Provider p ON e.ProviderID = p.ProviderID
                    LEFT JOIN Venue v ON e.VenueID = v.VenueID
                """)
                events = cursor.fetchall()
                
                if len(events) == 0:
                    ttk.Label(scrollable_frame, text="No events found", font=("Arial", 12)).pack(pady=20)
                
                for event in events:
                    event_frame = ttk.Frame(scrollable_frame)
                    event_frame.pack(pady=5, padx=5, fill="x")
                    
                    ttk.Label(event_frame, text=f"{event['Title']} - {event['CategoryName']}").grid(row=0, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Provider: {event['ProviderName']}").grid(row=1, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Venue: {event['VenueName']}").grid(row=2, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Price: ₹{event['Price']}").grid(row=3, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Availability: {event['Availability']}").grid(row=4, column=0, sticky="w")
                    ttk.Button(event_frame, text="Book Now", 
                             command=lambda e=event: self.book_event(e)).grid(row=0, column=1, rowspan=3, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_user_dashboard).pack(pady=10)

    def show_search_window(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Advanced Search")
        search_window.geometry("400x600")

        # --- Scroll setup ---
        canvas = tk.Canvas(search_window)
        scrollbar = ttk.Scrollbar(search_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # ---------------------

        # Create main frame with padding
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="Advanced Search", font=("Arial", 16)).pack(pady=10)

        # Search by name
        ttk.Label(main_frame, text="Event Name:").pack(pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=name_var, width=30)
        name_entry.pack(pady=5)

        # Category filter
        ttk.Label(main_frame, text="Category:").pack(pady=5)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(main_frame, textvariable=category_var, width=30)
        category_dropdown.pack(pady=5)

        # Price range
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(pady=5)
        ttk.Label(price_frame, text="Price Range:").pack()
        
        min_price_var = tk.StringVar()
        max_price_var = tk.StringVar()
        
        ttk.Label(price_frame, text="Min:").pack(side="left", padx=5)
        min_price_entry = ttk.Entry(price_frame, textvariable=min_price_var, width=10)
        min_price_entry.pack(side="left", padx=5)
        
        ttk.Label(price_frame, text="Max:").pack(side="left", padx=5)
        max_price_entry = ttk.Entry(price_frame, textvariable=max_price_var, width=10)
        max_price_entry.pack(side="left", padx=5)

        # Date range
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(pady=5)
        ttk.Label(date_frame, text="Date Range:").pack()
        
        start_date_var = tk.StringVar()
        end_date_var = tk.StringVar()
        
        ttk.Label(date_frame, text="From:").pack(side="left", padx=5)
        start_date_entry = ttk.Entry(date_frame, textvariable=start_date_var, width=10)
        start_date_entry.pack(side="left", padx=5)
        
        ttk.Label(date_frame, text="To:").pack(side="left", padx=5)
        end_date_entry = ttk.Entry(date_frame, textvariable=end_date_var, width=10)
        end_date_entry.pack(side="left", padx=5)

        # Get categories for dropdown
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT CategoryID, Name FROM Category")
                categories = cursor.fetchall()
                category_dropdown['values'] = ['All'] + [f"{cat['CategoryID']}: {cat['Name']}" for cat in categories]
                category_dropdown.set('All')
        except Exception as e:
            messagebox.showerror("Error", str(e))

        def perform_search():
            try:
                # Build query
                query = """
                    SELECT e.*, c.Name as CategoryName, p.Name as ProviderName,
                           v.Name as VenueName,
                           DATE_FORMAT(e.StartDate, '%%Y-%%m-%%d') as FormattedDate,
                           TIME_FORMAT(e.StartDate, '%%H:%%i') as FormattedTime
                    FROM Event e
                    LEFT JOIN Category c ON e.CategoryID = c.CategoryID
                    LEFT JOIN Provider p ON e.ProviderID = p.ProviderID
                    LEFT JOIN Venue v ON e.VenueID = v.VenueID
                    WHERE 1=1
                """
                params = []

                # Add search conditions
                if name_var.get():
                    query += " AND e.Title LIKE %s"
                    params.append(f"%{name_var.get()}%")

                if category_var.get() != 'All':
                    query += " AND e.CategoryID = %s"
                    params.append(category_var.get().split(':')[0])

                if min_price_var.get():
                    query += " AND e.Price >= %s"
                    params.append(float(min_price_var.get()))

                if max_price_var.get():
                    query += " AND e.Price <= %s"
                    params.append(float(max_price_var.get()))

                if start_date_var.get():
                    query += " AND e.StartDate >= %s"
                    params.append(start_date_var.get())

                if end_date_var.get():
                    query += " AND e.StartDate <= %s"
                    params.append(end_date_var.get())

                with self.conn.cursor() as cursor:
                    cursor.execute(query, tuple(params))
                    events = cursor.fetchall()

                    # Clear existing events
                    for widget in self.main_frame.winfo_children():
                        widget.destroy()

                    # --- Scroll setup ---
                    canvas = tk.Canvas(self.main_frame)
                    scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
                    scrollable_frame = ttk.Frame(canvas)

                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )

                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)

                    canvas.grid(row=1, column=0, sticky="nsew")
                    scrollbar.grid(row=1, column=1, sticky="ns")
                    
                    # Configure grid weights
                    self.main_frame.grid_columnconfigure(0, weight=1)
                    self.main_frame.grid_rowconfigure(1, weight=1)
                    # ---------------------

                    # Search button
                    search_frame = ttk.Frame(self.main_frame)
                    search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
                    
                    ttk.Button(search_frame, text="Advanced Search", 
                              command=self.show_search_window).pack(side="right", padx=5)

                    # Events list
                    ttk.Label(scrollable_frame, text="Search Results", font=("Arial", 16)).pack(pady=10)
                    
                    if len(events) == 0:
                        ttk.Label(scrollable_frame, text="No events found", font=("Arial", 12)).pack(pady=20)
                    
                    for event in events:
                        event_frame = ttk.Frame(scrollable_frame)
                        event_frame.pack(pady=5, padx=5, fill="x")
                        
                        ttk.Label(event_frame, text=f"{event['Title']} - {event['CategoryName']}").grid(row=0, column=0, sticky="w")
                        ttk.Label(event_frame, text=f"Provider: {event['ProviderName']}").grid(row=1, column=0, sticky="w")
                        ttk.Label(event_frame, text=f"Venue: {event['VenueName']}").grid(row=2, column=0, sticky="w")
                        ttk.Label(event_frame, text=f"Price: ₹{event['Price']}").grid(row=3, column=0, sticky="w")
                        ttk.Label(event_frame, text=f"Availability: {event['Availability']}").grid(row=4, column=0, sticky="w")
                        ttk.Button(event_frame, text="Book Now", 
                                 command=lambda e=event: self.book_event(e)).grid(row=0, column=1, rowspan=3, padx=5)
                    
                    ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_user_dashboard).pack(pady=10)

                    search_window.destroy()  # Close search window

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Search button
        ttk.Button(main_frame, text="Search", command=perform_search).pack(pady=20)
        ttk.Button(main_frame, text="Cancel", command=search_window.destroy).pack(pady=5)
    
    def book_event(self, event):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            return
        
        # Create booking window
        booking_window = tk.Toplevel(self.root)
        booking_window.title("Book Event")
        booking_window.geometry("400x500")

        # --- Scroll setup ---
        canvas = tk.Canvas(booking_window)
        scrollbar = ttk.Scrollbar(booking_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # ---------------------

        # Create main frame with padding
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="Book Event", font=("Arial", 16)).pack(pady=10)
        ttk.Label(main_frame, text=event['Title'], font=("Arial", 12)).pack(pady=5)

        # Event details
        ttk.Label(main_frame, text=f"Date: {event.get('FormattedDate', '')}").pack(pady=2)
        ttk.Label(main_frame, text=f"Time: {event.get('FormattedTime', '')}").pack(pady=2)
        ttk.Label(main_frame, text=f"Price: ₹{event['Price']}").pack(pady=2)
        ttk.Label(main_frame, text=f"Available Seats: {event['Availability']}").pack(pady=2)

        # Description
        ttk.Label(main_frame, text="Description:", font=("Arial", 10, "bold")).pack(pady=5)
        desc_text = tk.Text(main_frame, height=3, width=40, wrap=tk.WORD)
        desc_text.insert("1.0", event.get('Description', 'No description available'))
        desc_text.config(state="disabled")
        desc_text.pack(pady=5)

        # Get user's loyalty points
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT LoyaltyPoints FROM User WHERE UserID = %s", (self.current_user['UserID'],))
                user_points = cursor.fetchone()['LoyaltyPoints']
        except Exception as e:
            messagebox.showerror("Error", "Failed to fetch loyalty points")
            return

        # Number of tickets
        ttk.Label(main_frame, text="Number of Tickets:").pack(pady=5)
        tickets_var = tk.StringVar(value="1")
        tickets_entry = ttk.Entry(main_frame, textvariable=tickets_var)
        tickets_entry.pack(pady=5)

        # Loyalty points display and redemption
        points_frame = ttk.Frame(main_frame)
        points_frame.pack(pady=10)
        ttk.Label(points_frame, text=f"Your Loyalty Points: {user_points}").pack()
        
        # Points redemption option
        if user_points >= 10:  # Minimum 10 points required for ₹1 discount
            redeem_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(points_frame, 
                          text=f"Redeem all points for ₹{user_points/10:.2f} discount", 
                          variable=redeem_var).pack(pady=5)

        # Calculate total amount
        def update_total(*args):
            try:
                num_tickets = int(tickets_var.get())
                total = num_tickets * float(event['Price'])
                
                if user_points >= 10 and redeem_var.get():
                    discount = user_points / 10  # 10 points = ₹1
                    total = max(0, total - discount)
                
                total_label.config(text=f"Total Amount: ₹{total:.2f}")
            except ValueError:
                total_label.config(text="Total Amount: ₹0.00")

        tickets_var.trace('w', update_total)
        if user_points >= 10:
            redeem_var.trace('w', update_total)
        total_label = ttk.Label(main_frame, text="Total Amount: ₹0.00")
        total_label.pack(pady=10)

        # Payment method dropdown
        ttk.Label(main_frame, text="Payment Method:").pack(pady=5)
        payment_var = tk.StringVar()
        payment_methods = ['Credit Card', 'Debit Card', 'Net Banking', 'UPI', 'Wallet']
        payment_dropdown = ttk.Combobox(main_frame, textvariable=payment_var, values=payment_methods)
        payment_dropdown.set('Credit Card')  # default value
        payment_dropdown.pack(pady=5)

        def process_payment():
            try:
                num_tickets = int(tickets_var.get())
                if num_tickets <= 0:
                    raise ValueError("Please enter a valid number of tickets")
                if num_tickets > event['Availability']:
                    raise ValueError("Not enough tickets available")

                payment_method = payment_var.get()
                if not payment_method:
                    raise ValueError("Please select a payment method")

                total_amount = num_tickets * float(event['Price'])
                points_redeemed = 0
                
                if user_points >= 10 and redeem_var.get():
                    points_redeemed = user_points
                    discount = points_redeemed / 10  # 10 points = ₹1
                    total_amount = max(0, total_amount - discount)

                with self.conn.cursor() as cursor:
                    # Start transaction
                    cursor.execute("START TRANSACTION")

                    try:
                        # Create booking
                        cursor.execute("""
                            INSERT INTO Booking (UserID, EventID, NumberOfSeats, TotalPrice, BookingDate, PaymentStatus)
                            VALUES (%s, %s, %s, %s, NOW(), 'Completed')
                        """, (self.current_user['UserID'], event['EventID'], num_tickets, total_amount))
                        
                        # Get the booking ID
                        booking_id = cursor.lastrowid

                        # Create payment record
                        cursor.execute("""
                            INSERT INTO Payment (BookingID, UserID, PaymentDate, Amount, Method, Status)
                            VALUES (%s, %s, NOW(), %s, %s, 'Completed')
                        """, (booking_id, self.current_user['UserID'], total_amount, payment_method))

                        # Update event availability
                        cursor.execute("""
                            UPDATE Event 
                            SET Availability = Availability - %s
                            WHERE EventID = %s AND Availability >= %s
                        """, (num_tickets, event['EventID'], num_tickets))

                        if cursor.rowcount == 0:
                            raise ValueError("Not enough tickets available")

                        # Calculate and update loyalty points
                        points_earned = int(total_amount / 100) * 10  # 10 points per ₹100
                        cursor.execute("""
                            UPDATE User 
                            SET LoyaltyPoints = LoyaltyPoints + %s - %s
                            WHERE UserID = %s
                        """, (points_earned, points_redeemed, self.current_user['UserID']))

                        # Commit transaction
                        self.conn.commit()

                        messagebox.showinfo("Success", 
                            f"Booking successful!\nBooking ID: {booking_id}\nTotal Amount: ₹{total_amount:.2f}\n"
                            f"Points Earned: {points_earned}\nPoints Redeemed: {points_redeemed}")
                        booking_window.destroy()
                        self.show_events()  # Refresh events list

                    except Exception as e:
                        # Rollback transaction on error
                        self.conn.rollback()
                        print(f"Database error: {str(e)}")  # Debug print
                        raise Exception("Failed to process booking. Please check all fields and try again.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        ttk.Button(main_frame, text="Confirm Payment", command=process_payment).pack(pady=20)
        ttk.Button(main_frame, text="Cancel", command=booking_window.destroy).pack(pady=5)
    
    def show_my_bookings(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # My bookings list
        ttk.Label(self.main_frame, text="My Bookings", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT b.*, e.Title, e.Price
                    FROM Booking b
                    JOIN Event e ON b.EventID = e.EventID
                    WHERE b.UserID = %s
                """, (self.current_user['UserID'],))
                bookings = cursor.fetchall()
                
                for i, booking in enumerate(bookings, 1):
                    booking_frame = ttk.Frame(self.main_frame)
                    booking_frame.grid(row=i, column=0, columnspan=2, pady=5, padx=5, sticky="w")
                    
                    ttk.Label(booking_frame, text=f"Event: {booking['Title']}").grid(row=0, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Seats: {booking['NumberOfSeats']}").grid(row=1, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Total Price: ₹{booking['TotalPrice']}").grid(row=2, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Status: {booking['PaymentStatus']}").grid(row=3, column=0, sticky="w")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        ttk.Button(self.main_frame, text="Back to Dashboard", command=self.show_user_dashboard).grid(row=len(bookings)+1, column=0, columnspan=2, pady=10)
    
    def manage_events(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # --- Scroll setup ---
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        # ---------------------

        # Search button
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        ttk.Button(search_frame, text="Advanced Search", 
                  command=self.show_search_window).pack(side="right", padx=5)
        
        # Add new event button
        ttk.Button(search_frame, text="Add New Event", 
                  command=self.add_event).pack(side="left", padx=5)
        
        # Events list
        ttk.Label(scrollable_frame, text="Manage Events", font=("Arial", 16)).pack(pady=10)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT e.*, c.Name as CategoryName, p.Name as ProviderName,
                           v.Name as VenueName,
                           DATE_FORMAT(e.StartDate, '%%Y-%%m-%%d') as FormattedDate,
                           TIME_FORMAT(e.StartDate, '%%H:%%i') as FormattedTime
                    FROM Event e
                    LEFT JOIN Category c ON e.CategoryID = c.CategoryID
                    LEFT JOIN Provider p ON e.ProviderID = p.ProviderID
                    LEFT JOIN Venue v ON e.VenueID = v.VenueID
                """)
                events = cursor.fetchall()
                
                if len(events) == 0:
                    ttk.Label(scrollable_frame, text="No events found", font=("Arial", 12)).pack(pady=20)
                
                for event in events:
                    event_frame = ttk.Frame(scrollable_frame)
                    event_frame.pack(pady=5, padx=5, fill="x")
                    
                    ttk.Label(event_frame, text=f"{event['Title']} - {event['CategoryName']}").grid(row=0, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Provider: {event['ProviderName']}").grid(row=1, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Venue: {event['VenueName']}").grid(row=2, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Price: ₹{event['Price']}").grid(row=3, column=0, sticky="w")
                    ttk.Label(event_frame, text=f"Availability: {event['Availability']}").grid(row=4, column=0, sticky="w")
                    
                    button_frame = ttk.Frame(event_frame)
                    button_frame.grid(row=0, column=1, rowspan=4, padx=5)
                    
                    ttk.Button(button_frame, text="Edit", 
                             command=lambda e=event: self.edit_event(e)).pack(side="left", padx=2)
                    ttk.Button(button_frame, text="Delete", 
                             command=lambda e=event: self.delete_event(e)).pack(side="left", padx=2)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_admin_dashboard).pack(pady=10)

    def add_event(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Event")

        # Dynamically center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 800  # Increased height for new fields
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        add_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Scrollable canvas setup
        canvas = tk.Canvas(add_window)
        scrollbar = ttk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Configure grid weights
        add_window.grid_columnconfigure(0, weight=1)
        add_window.grid_rowconfigure(0, weight=1)
        
        # Place canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Title
        ttk.Label(scrollable_frame, text="Add New Event", font=("Arial", 16)).pack(pady=10)

        def create_form_entry(label, default_value=""):
            ttk.Label(scrollable_frame, text=label).pack(pady=5)
            entry = ttk.Entry(scrollable_frame)
            if default_value:
                entry.insert(0, default_value)
            entry.pack(pady=5)
            return entry

        # Form fields
        title_entry = create_form_entry("Title:")
        desc_entry = create_form_entry("Description:")
        
        # Date and Duration fields
        ttk.Label(scrollable_frame, text="Start Date (YYYY-MM-DD):").pack(pady=5)
        start_date_entry = ttk.Entry(scrollable_frame)
        start_date_entry.pack(pady=5)
        
        ttk.Label(scrollable_frame, text="Duration (in hours):").pack(pady=5)
        duration_entry = ttk.Entry(scrollable_frame)
        duration_entry.pack(pady=5)
        
        price_entry = create_form_entry("Price:")
        availability_entry = create_form_entry("Availability:")

        # Category dropdown
        ttk.Label(scrollable_frame, text="Category:").pack(pady=5)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(scrollable_frame, textvariable=category_var)
        category_dropdown.pack(pady=5)

        # Provider dropdown
        ttk.Label(scrollable_frame, text="Provider:").pack(pady=5)
        provider_var = tk.StringVar()
        provider_dropdown = ttk.Combobox(scrollable_frame, textvariable=provider_var)
        provider_dropdown.pack(pady=5)

        # Venue dropdown
        ttk.Label(scrollable_frame, text="Venue:").pack(pady=5)
        venue_var = tk.StringVar()
        venue_dropdown = ttk.Combobox(scrollable_frame, textvariable=venue_var)
        venue_dropdown.pack(pady=5)
        
        # Online event checkbox
        is_online_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(scrollable_frame, text="Online Event", 
                       variable=is_online_var).pack(pady=10)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT CategoryID, Name FROM Category")
                categories = cursor.fetchall()
                category_dropdown['values'] = [f"{cat['CategoryID']}: {cat['Name']}" for cat in categories]

                cursor.execute("SELECT ProviderID, Name FROM Provider")
                providers = cursor.fetchall()
                provider_dropdown['values'] = [f"{prov['ProviderID']}: {prov['Name']}" for prov in providers]

                cursor.execute("SELECT VenueID, Name FROM Venue")
                venues = cursor.fetchall()
                venue_dropdown['values'] = [f"{venue['VenueID']}: {venue['Name']}" for venue in venues]
        except Exception as e:
            messagebox.showerror("Error", str(e))

        def save_event():
            try:
                title = title_entry.get()
                description = desc_entry.get()
                start_date = start_date_entry.get()
                duration = duration_entry.get()
                price = price_entry.get()
                availability = availability_entry.get()
                is_online = is_online_var.get()
                
                # Handle empty or invalid dropdown selections
                try:
                    venue_id = venue_var.get().split(':')[0].strip()
                except (IndexError, AttributeError):
                    venue_id = None
                try:
                    category_id = category_var.get().split(':')[0].strip()
                except (IndexError, AttributeError):
                    category_id = None
                try:
                    provider_id = provider_var.get().split(':')[0].strip()
                except (IndexError, AttributeError):
                    provider_id = None

                with self.conn.cursor() as cursor:
                    # Calculate end date based on start date and duration
                    cursor.execute("""
                        SELECT DATE_ADD(%s, INTERVAL %s HOUR) as EndDate
                    """, (start_date, duration))
                    result = cursor.fetchone()
                    end_date = result['EndDate']
                    
                    cursor.execute("""
                        INSERT INTO Event (Title, Description, StartDate, EndDate, Duration,
                                         VenueID, Price, Availability, CategoryID, 
                                         ProviderID, IsOnline)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        title, description, start_date, end_date, duration,
                        venue_id, price, availability, category_id, 
                        provider_id, is_online
                    ))
                    self.conn.commit()

                messagebox.showinfo("Success", "Event added successfully!")
                add_window.destroy()
                self.manage_events()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        ttk.Button(scrollable_frame, text="Save Event", command=save_event).pack(pady=20)
        ttk.Button(scrollable_frame, text="Cancel", command=add_window.destroy).pack(pady=10)

    def edit_event(self, event):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Event")

        # Dynamically center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 750
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Scrollable canvas setup
        canvas = tk.Canvas(edit_window)
        scrollbar = ttk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Configure grid weights
        edit_window.grid_columnconfigure(0, weight=1)
        edit_window.grid_rowconfigure(0, weight=1)
        
        # Place canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Title
        ttk.Label(scrollable_frame, text="Edit Event", font=("Arial", 16)).pack(pady=10)

        def create_form_entry(label, default_value=""):
            ttk.Label(scrollable_frame, text=label).pack(pady=5)
            entry = ttk.Entry(scrollable_frame)
            if default_value:
                entry.insert(0, default_value)
            entry.pack(pady=5)
            return entry

        # Form fields
        title_entry = create_form_entry("Title:", event['Title'])
        desc_entry = create_form_entry("Description:", event.get('Description', ''))
        
        # Format date and time from StartDate
        start_date = event['StartDate']
        formatted_date = start_date.strftime('%Y-%m-%d')
        formatted_time = start_date.strftime('%H:%M')
        
        date_entry = create_form_entry("Date (YYYY-MM-DD):", formatted_date)
        time_entry = create_form_entry("Time (HH:MM):", formatted_time)
        price_entry = create_form_entry("Price:", str(event['Price']))
        availability_entry = create_form_entry("Availability:", str(event['Availability']))

        # Category dropdown
        ttk.Label(scrollable_frame, text="Category:").pack(pady=5)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(scrollable_frame, textvariable=category_var)
        category_dropdown.pack(pady=5)

        # Provider dropdown
        ttk.Label(scrollable_frame, text="Provider:").pack(pady=5)
        provider_var = tk.StringVar()
        provider_dropdown = ttk.Combobox(scrollable_frame, textvariable=provider_var)
        provider_dropdown.pack(pady=5)

        # Venue dropdown
        ttk.Label(scrollable_frame, text="Venue:").pack(pady=5)
        venue_var = tk.StringVar()
        venue_dropdown = ttk.Combobox(scrollable_frame, textvariable=venue_var)
        venue_dropdown.pack(pady=5)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT CategoryID, Name FROM Category")
                categories = cursor.fetchall()
                category_dropdown['values'] = [f"{cat['CategoryID']}: {cat['Name']}" for cat in categories]
                category_dropdown.set(f"{event['CategoryID']}: {event['CategoryName']}")

                cursor.execute("SELECT ProviderID, Name FROM Provider")
                providers = cursor.fetchall()
                provider_dropdown['values'] = [f"{prov['ProviderID']}: {prov['Name']}" for prov in providers]
                provider_dropdown.set(f"{event['ProviderID']}: {event['ProviderName']}")

                cursor.execute("SELECT VenueID, Name FROM Venue")
                venues = cursor.fetchall()
                venue_dropdown['values'] = [f"{venue['VenueID']}: {venue['Name']}" for venue in venues]
                venue_dropdown.set(f"{event['VenueID']}: {event['VenueName']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

        def save_changes():
            try:
                title = title_entry.get()
                description = desc_entry.get()
                date = date_entry.get()
                time = time_entry.get()
                # Handle empty or invalid dropdown selections
                try:
                    venue_id = venue_var.get().split(':')[0].strip()
                except (IndexError, AttributeError):
                    venue_id = event['VenueID']  # Fallback to original value
                try:
                    category_id = category_var.get().split(':')[0].strip()
                except (IndexError, AttributeError):
                    category_id = event['CategoryID']  # Fallback to original value
                try:
                    provider_id = provider_var.get().split(':')[0].strip()
                except (IndexError, AttributeError):
                    provider_id = event['ProviderID']  # Fallback to original value
                
                price = price_entry.get()
                availability = availability_entry.get()

                with self.conn.cursor() as cursor:
                    # Combine date and time and format properly for MySQL
                    datetime_str = f"{date} {time}"
                    cursor.execute("""
                        UPDATE Event 
                        SET Title = %s, Description = %s, StartDate = %s,
                            VenueID = %s, Price = %s, Availability = %s,
                            CategoryID = %s, ProviderID = %s
                        WHERE EventID = %s
                    """, (
                        title, description, datetime_str, venue_id,
                        price, availability, category_id, provider_id,
                        event['EventID']
                    ))
                    self.conn.commit()

                messagebox.showinfo("Success", "Event updated successfully!")
                edit_window.destroy()
                self.manage_events()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        ttk.Button(scrollable_frame, text="Save Changes", command=save_changes).pack(pady=20)
        ttk.Button(scrollable_frame, text="Cancel", command=edit_window.destroy).pack(pady=10)

    def delete_event(self, event):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {event['Title']}?"):
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Event WHERE EventID = %s", (event['EventID'],))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Event deleted successfully!")
                    self.manage_events()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def manage_users(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # --- Scroll setup ---
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        # ---------------------
        
        # Users management
        ttk.Label(scrollable_frame, text="Manage Users", font=("Arial", 16)).pack(pady=10)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM User")
                users = cursor.fetchall()
                
                for user in users:
                    user_frame = ttk.Frame(scrollable_frame)
                    user_frame.pack(pady=5, padx=5, fill="x")
                    
                    ttk.Label(user_frame, text=f"Name: {user['Name']}").grid(row=0, column=0, sticky="w")
                    ttk.Label(user_frame, text=f"Email: {user['Email']}").grid(row=1, column=0, sticky="w")
                    ttk.Label(user_frame, text=f"Phone: {user['Phone']}").grid(row=2, column=0, sticky="w")
                    
                    ttk.Button(user_frame, text="Delete", 
                             command=lambda u=user: self.delete_user(u)).grid(row=0, column=1, rowspan=3, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_admin_dashboard).pack(pady=10)
    
    def delete_user(self, user):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user['Name']}?"):
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute("DELETE FROM User WHERE UserID = %s", (user['UserID'],))
                    self.conn.commit()
                    messagebox.showinfo("Success", "User deleted successfully!")
                    self.manage_users()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def view_all_bookings(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # --- Scroll setup ---
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        # ---------------------

        # Search button
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        ttk.Button(search_frame, text="Advanced Search", 
                  command=self.show_booking_search_window).pack(side="right", padx=5)
        
        # All bookings list
        ttk.Label(scrollable_frame, text="All Bookings", font=("Arial", 16)).pack(pady=10)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT b.*, e.Title, u.Name as UserName, b.BookingDate
                    FROM Booking b
                    JOIN Event e ON b.EventID = e.EventID
                    JOIN User u ON b.UserID = u.UserID
                """)
                bookings = cursor.fetchall()
                
                if len(bookings) == 0:
                    ttk.Label(scrollable_frame, text="No bookings found", font=("Arial", 12)).pack(pady=20)
                
                for booking in bookings:
                    booking_frame = ttk.Frame(scrollable_frame)
                    booking_frame.pack(pady=5, padx=5, fill="x")
                    
                    ttk.Label(booking_frame, text=f"User: {booking['UserName']}").grid(row=0, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Event: {booking['Title']}").grid(row=1, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Seats: {booking['NumberOfSeats']}").grid(row=2, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Total Price: ₹{booking['TotalPrice']}").grid(row=3, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Status: {booking['PaymentStatus']}").grid(row=4, column=0, sticky="w")
                    ttk.Label(booking_frame, text=f"Date: {booking['BookingDate'].strftime('%d-%m-%Y')}").grid(row=5, column=0, sticky="w")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_admin_dashboard).pack(pady=10)

    def show_booking_search_window(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Advanced Booking Search")
        search_window.geometry("400x600")

        # --- Scroll setup ---
        canvas = tk.Canvas(search_window)
        scrollbar = ttk.Scrollbar(search_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # ---------------------

        # Create main frame with padding
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="Advanced Booking Search", font=("Arial", 16)).pack(pady=10)

        # Search by user name
        ttk.Label(main_frame, text="User Name:").pack(pady=5)
        user_var = tk.StringVar()
        user_entry = ttk.Entry(main_frame, textvariable=user_var, width=30)
        user_entry.pack(pady=5)

        # Search by event name
        ttk.Label(main_frame, text="Event Name:").pack(pady=5)
        event_var = tk.StringVar()
        event_entry = ttk.Entry(main_frame, textvariable=event_var, width=30)
        event_entry.pack(pady=5)

        # Price range
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(pady=5)
        ttk.Label(price_frame, text="Price Range:").pack()
        
        min_price_var = tk.StringVar()
        max_price_var = tk.StringVar()
        
        ttk.Label(price_frame, text="Min:").pack(side="left", padx=5)
        min_price_entry = ttk.Entry(price_frame, textvariable=min_price_var, width=10)
        min_price_entry.pack(side="left", padx=5)
        
        ttk.Label(price_frame, text="Max:").pack(side="left", padx=5)
        max_price_entry = ttk.Entry(price_frame, textvariable=max_price_var, width=10)
        max_price_entry.pack(side="left", padx=5)

        # Date range
        date_frame = ttk.Frame(main_frame)
        date_frame.pack(pady=5)
        ttk.Label(date_frame, text="Booking Date Range:").pack()
        
        start_date_var = tk.StringVar()
        end_date_var = tk.StringVar()
        
        ttk.Label(date_frame, text="From:").pack(side="left", padx=5)
        start_date_entry = ttk.Entry(date_frame, textvariable=start_date_var, width=10)
        start_date_entry.pack(side="left", padx=5)
        
        ttk.Label(date_frame, text="To:").pack(side="left", padx=5)
        end_date_entry = ttk.Entry(date_frame, textvariable=end_date_var, width=10)
        end_date_entry.pack(side="left", padx=5)

        # Payment status
        ttk.Label(main_frame, text="Payment Status:").pack(pady=5)
        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(main_frame, textvariable=status_var, width=30)
        status_dropdown['values'] = ['All', 'Completed', 'Pending', 'Cancelled']
        status_dropdown.set('All')
        status_dropdown.pack(pady=5)

        def perform_search():
            try:
                # Build query
                query = """
                    SELECT b.*, e.Title, u.Name as UserName, b.BookingDate
                    FROM Booking b
                    JOIN Event e ON b.EventID = e.EventID
                    JOIN User u ON b.UserID = u.UserID
                    WHERE 1=1
                """
                params = []

                # Add search conditions
                if user_var.get():
                    query += " AND u.Name LIKE %s"
                    params.append(f"%{user_var.get()}%")

                if event_var.get():
                    query += " AND e.Title LIKE %s"
                    params.append(f"%{event_var.get()}%")

                if min_price_var.get():
                    query += " AND b.TotalPrice >= %s"
                    params.append(float(min_price_var.get()))

                if max_price_var.get():
                    query += " AND b.TotalPrice <= %s"
                    params.append(float(max_price_var.get()))

                if start_date_var.get():
                    query += " AND b.BookingDate >= %s"
                    params.append(start_date_var.get())

                if end_date_var.get():
                    query += " AND b.BookingDate <= %s"
                    params.append(end_date_var.get())

                if status_var.get() != 'All':
                    query += " AND b.PaymentStatus = %s"
                    params.append(status_var.get())

                with self.conn.cursor() as cursor:
                    cursor.execute(query, tuple(params))
                    bookings = cursor.fetchall()

                    # Clear existing bookings
                    for widget in self.main_frame.winfo_children():
                        widget.destroy()

                    # --- Scroll setup ---
                    canvas = tk.Canvas(self.main_frame)
                    scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
                    scrollable_frame = ttk.Frame(canvas)

                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )

                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)

                    canvas.grid(row=1, column=0, sticky="nsew")
                    scrollbar.grid(row=1, column=1, sticky="ns")
                    
                    # Configure grid weights
                    self.main_frame.grid_columnconfigure(0, weight=1)
                    self.main_frame.grid_rowconfigure(1, weight=1)
                    # ---------------------

                    # Search button
                    search_frame = ttk.Frame(self.main_frame)
                    search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
                    
                    ttk.Button(search_frame, text="Advanced Search", 
                              command=self.show_booking_search_window).pack(side="right", padx=5)

                    # Bookings list
                    ttk.Label(scrollable_frame, text="Search Results", font=("Arial", 16)).pack(pady=10)
                    
                    if len(bookings) == 0:
                        ttk.Label(scrollable_frame, text="No bookings found", font=("Arial", 12)).pack(pady=20)
                    
                    for booking in bookings:
                        booking_frame = ttk.Frame(scrollable_frame)
                        booking_frame.pack(pady=5, padx=5, fill="x")
                        
                        ttk.Label(booking_frame, text=f"User: {booking['UserName']}").grid(row=0, column=0, sticky="w")
                        ttk.Label(booking_frame, text=f"Event: {booking['Title']}").grid(row=1, column=0, sticky="w")
                        ttk.Label(booking_frame, text=f"Seats: {booking['NumberOfSeats']}").grid(row=2, column=0, sticky="w")
                        ttk.Label(booking_frame, text=f"Total Price: ₹{booking['TotalPrice']}").grid(row=3, column=0, sticky="w")
                        ttk.Label(booking_frame, text=f"Status: {booking['PaymentStatus']}").grid(row=4, column=0, sticky="w")
                        ttk.Label(booking_frame, text=f"Date: {booking['BookingDate'].strftime('%d-%m-%Y')}").grid(row=5, column=0, sticky="w")
                    
                    ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_admin_dashboard).pack(pady=10)

                    search_window.destroy()  # Close search window

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Search button
        ttk.Button(main_frame, text="Search", command=perform_search).pack(pady=20)
        ttk.Button(main_frame, text="Cancel", command=search_window.destroy).pack(pady=5)
    
    def logout(self):
        self.current_user = None
        self.show_login_screen()

    def manage_venues(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # --- Scroll setup ---
        canvas = tk.Canvas(self.main_frame)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Venues management
        ttk.Label(scrollable_frame, text="Manage Venues", font=("Arial", 16)).pack(pady=10)
        
        # Add new venue button
        ttk.Button(scrollable_frame, text="Add New Venue", command=self.show_add_venue_form).pack(pady=5)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Venue")
                venues = cursor.fetchall()
                
                if len(venues) == 0:
                    ttk.Label(scrollable_frame, text="No venues found", font=("Arial", 12)).pack(pady=20)
                
                for venue in venues:
                    venue_frame = ttk.Frame(scrollable_frame)
                    venue_frame.pack(pady=5, padx=5, fill="x")
                    
                    ttk.Label(venue_frame, text=f"Name: {venue['Name']}").grid(row=0, column=0, sticky="w")
                    ttk.Label(venue_frame, text=f"Address: {venue['Address']}").grid(row=1, column=0, sticky="w")
                    ttk.Label(venue_frame, text=f"Capacity: {venue['Capacity']}").grid(row=2, column=0, sticky="w")
                    ttk.Label(venue_frame, text=f"Contact: {venue['Contact']}").grid(row=3, column=0, sticky="w")
                    
                    button_frame = ttk.Frame(venue_frame)
                    button_frame.grid(row=0, column=1, rowspan=4, padx=5)
                    
                    ttk.Button(button_frame, text="Edit", 
                             command=lambda v=venue: self.edit_venue(v)).pack(side="left", padx=2)
                    ttk.Button(button_frame, text="Delete", 
                             command=lambda v=venue: self.delete_venue(v)).pack(side="left", padx=2)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        ttk.Button(scrollable_frame, text="Back to Dashboard", command=self.show_admin_dashboard).pack(pady=10)

    def show_add_venue_form(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Venue")
        add_window.geometry("400x500")

        # Create main frame with padding
        main_frame = ttk.Frame(add_window, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="Add New Venue", font=("Arial", 16)).pack(pady=10)

        # Form fields
        ttk.Label(main_frame, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(main_frame, width=40)
        name_entry.pack(pady=5)

        ttk.Label(main_frame, text="Address:").pack(pady=5)
        address_entry = ttk.Entry(main_frame, width=40)
        address_entry.pack(pady=5)

        ttk.Label(main_frame, text="Capacity:").pack(pady=5)
        capacity_entry = ttk.Entry(main_frame, width=40)
        capacity_entry.pack(pady=5)

        ttk.Label(main_frame, text="Contact:").pack(pady=5)
        contact_entry = ttk.Entry(main_frame, width=40)
        contact_entry.pack(pady=5)

        def save_venue():
            try:
                name = name_entry.get()
                address = address_entry.get()
                capacity = capacity_entry.get()
                contact = contact_entry.get()

                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Venue (Name, Address, Capacity, Contact)
                        VALUES (%s, %s, %s, %s)
                    """, (name, address, capacity, contact))
                    self.conn.commit()

                messagebox.showinfo("Success", "Venue added successfully!")
                add_window.destroy()
                self.manage_venues()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        ttk.Button(main_frame, text="Save Venue", command=save_venue).pack(pady=20)
        ttk.Button(main_frame, text="Cancel", command=add_window.destroy).pack(pady=5)

    def edit_venue(self, venue):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Venue")
        edit_window.geometry("400x500")

        # Create main frame with padding
        main_frame = ttk.Frame(edit_window, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(main_frame, text="Edit Venue", font=("Arial", 16)).pack(pady=10)

        # Form fields
        ttk.Label(main_frame, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(main_frame, width=40)
        name_entry.insert(0, venue['Name'])
        name_entry.pack(pady=5)

        ttk.Label(main_frame, text="Address:").pack(pady=5)
        address_entry = ttk.Entry(main_frame, width=40)
        address_entry.insert(0, venue['Address'])
        address_entry.pack(pady=5)

        ttk.Label(main_frame, text="Capacity:").pack(pady=5)
        capacity_entry = ttk.Entry(main_frame, width=40)
        capacity_entry.insert(0, str(venue['Capacity']))
        capacity_entry.pack(pady=5)

        ttk.Label(main_frame, text="Contact:").pack(pady=5)
        contact_entry = ttk.Entry(main_frame, width=40)
        contact_entry.insert(0, venue['Contact'])
        contact_entry.pack(pady=5)

        def save_changes():
            try:
                name = name_entry.get()
                address = address_entry.get()
                capacity = capacity_entry.get()
                contact = contact_entry.get()

                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE Venue 
                        SET Name = %s, Address = %s, Capacity = %s, Contact = %s
                        WHERE VenueID = %s
                    """, (name, address, capacity, contact, venue['VenueID']))
                    self.conn.commit()

                messagebox.showinfo("Success", "Venue updated successfully!")
                edit_window.destroy()
                self.manage_venues()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Buttons
        ttk.Button(main_frame, text="Save Changes", command=save_changes).pack(pady=20)
        ttk.Button(main_frame, text="Cancel", command=edit_window.destroy).pack(pady=10)

    def delete_venue(self, venue):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete venue {venue['Name']}?"):
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Venue WHERE VenueID = %s", (venue['VenueID'],))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Venue deleted successfully!")
                    self.manage_venues()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def show_admin_dashboard(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Title
        ttk.Label(self.main_frame, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=20)
        
        # Management buttons
        ttk.Button(buttons_frame, text="Manage Events", 
                  command=self.manage_events).pack(pady=10, padx=10, fill="x")
        ttk.Button(buttons_frame, text="Manage Venues", 
                  command=self.manage_venues).pack(pady=10, padx=10, fill="x")
        ttk.Button(buttons_frame, text="Manage Users", 
                  command=self.manage_users).pack(pady=10, padx=10, fill="x")
        ttk.Button(buttons_frame, text="View All Bookings", 
                  command=self.view_all_bookings).pack(pady=10, padx=10, fill="x")
        
        # Logout button
        ttk.Button(self.main_frame, text="Logout", 
                  command=self.logout).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = TixifyApp(root)
    root.mainloop() 