import pymysql
from db_config import DB_CONFIG

def init_database():
    # Connect to MySQL server
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS tixify")
            cursor.execute("USE tixify")
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS User (
                    UserID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(100) NOT NULL,
                    Email VARCHAR(100) UNIQUE NOT NULL,
                    Phone VARCHAR(20),
                    Password VARCHAR(50) NOT NULL,
                    LoyaltyPoints INT DEFAULT 0
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Provider (
                    ProviderID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(100) NOT NULL,
                    Type VARCHAR(50),
                    Contact VARCHAR(100),
                    Rating DECIMAL(3,2),
                    Address TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Category (
                    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(50) NOT NULL,
                    Description TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Venue (
                    VenueID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(100) NOT NULL,
                    Address TEXT,
                    Capacity INT,
                    Contact VARCHAR(100)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Event (
                    EventID INT AUTO_INCREMENT PRIMARY KEY,
                    ProviderID INT,
                    CategoryID INT,
                    VenueID INT,
                    Title VARCHAR(200) NOT NULL,
                    Description TEXT,
                    Duration INT,
                    Price DECIMAL(10,2),
                    StartDate DATETIME,
                    EndDate DATETIME,
                    isOnline BOOLEAN,
                    Availability INT,
                    FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID),
                    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
                    FOREIGN KEY (VenueID) REFERENCES Venue(VenueID)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Booking (
                    BookingID INT AUTO_INCREMENT PRIMARY KEY,
                    UserID INT,
                    EventID INT,
                    BookingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                    NumberOfSeats INT,
                    TotalPrice DECIMAL(10,2),
                    PaymentStatus VARCHAR(20),
                    FOREIGN KEY (UserID) REFERENCES User(UserID),
                    FOREIGN KEY (EventID) REFERENCES Event(EventID)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Payment (
                    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
                    BookingID INT,
                    UserID INT,
                    PaymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                    Amount DECIMAL(10,2),
                    Method VARCHAR(50),
                    Status VARCHAR(20),
                    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
                    FOREIGN KEY (UserID) REFERENCES User(UserID)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Review (
                    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
                    UserID INT,
                    EventID INT,
                    Rating INT,
                    Comment TEXT,
                    ReviewDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (UserID) REFERENCES User(UserID),
                    FOREIGN KEY (EventID) REFERENCES Event(EventID)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Admin (
                    AdminID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(100) NOT NULL,
                    Email VARCHAR(100) UNIQUE NOT NULL,
                    Phone VARCHAR(20),
                    Role VARCHAR(50),
                    Password VARCHAR(50) NOT NULL
                )
            """)
            
            # Insert default categories
            categories = [
                ('Music', 'Live music events and concerts'),
                ('Dining', 'Food and dining experiences'),
                ('Comedy', 'Stand-up comedy shows'),
                ('Nightlife', 'Nightlife and party events'),
                ('Sports', 'Sports events and games')
            ]
            
            cursor.executemany(
                "INSERT IGNORE INTO Category (Name, Description) VALUES (%s, %s)",
                categories
            )
            
            # Insert default admin
            cursor.execute("""
                INSERT IGNORE INTO Admin (Name, Email, Phone, Role, Password)
                VALUES ('Admin', 'admin@tixify.com', '1234567890', 'Super Admin', 'admin123')
            """)
            
            connection.commit()
            print("Database and tables created successfully!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    init_database() 