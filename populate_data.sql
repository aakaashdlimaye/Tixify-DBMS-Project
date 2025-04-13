-- Insert sample data for Admin table
INSERT INTO Admin (Name, Email, Password, Phone) VALUES
('Admin One', 'admin1@tixify.com', 'admin123', '9876543210'),
('Admin Two', 'admin2@tixify.com', 'admin123', '9876543211'),
('Admin Three', 'admin3@tixify.com', 'admin123', '9876543212'),
('Admin Four', 'admin4@tixify.com', 'admin123', '9876543213'),
('Admin Five', 'admin5@tixify.com', 'admin123', '9876543214'),
('Admin Six', 'admin6@tixify.com', 'admin123', '9876543215'),
('Admin Seven', 'admin7@tixify.com', 'admin123', '9876543216'),
('Admin Eight', 'admin8@tixify.com', 'admin123', '9876543217'),
('Admin Nine', 'admin9@tixify.com', 'admin123', '9876543218'),
('Admin Ten', 'admin10@tixify.com', 'admin123', '9876543219');

-- Insert sample data for Provider table
INSERT INTO Provider (Name, Type, Contact, Rating, Address) VALUES
('Event Masters', 'Corporate', '9876543220', 4.5, '123 Business Park, Andheri East, Mumbai'),
('Party Planners', 'Entertainment', '9876543221', 4.2, '456 Celebration Street, Bandra West, Mumbai'),
('Concert Kings', 'Music', '9876543222', 4.8, '789 Music Lane, Juhu, Mumbai'),
('Sports Events Co', 'Sports', '9876543223', 4.3, '321 Stadium Road, Worli, Mumbai'),
('Cultural Events', 'Cultural', '9876543224', 4.6, '654 Heritage Avenue, Fort, Mumbai'),
('Tech Conferences', 'Technology', '9876543225', 4.4, '987 Tech Park, Powai, Mumbai'),
('Food Festivals', 'Food', '9876543226', 4.7, '147 Food Street, Lower Parel, Mumbai'),
('Art Exhibitions', 'Art', '9876543227', 4.1, '258 Gallery Road, Colaba, Mumbai'),
('Music Festivals', 'Music', '9876543228', 4.9, '369 Melody Lane, Khar, Mumbai'),
('Corporate Events', 'Corporate', '9876543229', 4.5, '741 Business Center, BKC, Mumbai');

-- Insert sample data for User table
INSERT INTO User (Name, Email, Password, Phone, LoyaltyPoints) VALUES
('Rahul Sharma', 'rahul.sharma@gmail.com', 'user123', '9876543230', 150),
('Priya Patel', 'priya.patel@gmail.com', 'user123', '9876543231', 200),
('Amit Kumar', 'amit.kumar@gmail.com', 'user123', '9876543232', 75),
('Neha Gupta', 'neha.gupta@gmail.com', 'user123', '9876543233', 300),
('Vikram Singh', 'vikram.singh@gmail.com', 'user123', '9876543234', 50),
('Ananya Reddy', 'ananya.reddy@gmail.com', 'user123', '9876543235', 100),
('Rohan Mehta', 'rohan.mehta@gmail.com', 'user123', '9876543236', 250),
('Sneha Joshi', 'sneha.joshi@gmail.com', 'user123', '9876543237', 180),
('Arjun Malhotra', 'arjun.malhotra@gmail.com', 'user123', '9876543238', 90),
('Ishaan Verma', 'ishaan.verma@gmail.com', 'user123', '9876543239', 120); 