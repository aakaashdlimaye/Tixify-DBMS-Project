# Tixify - Event Booking System

Tixify is a comprehensive event booking and management system built with Python and MySQL. It provides a user-friendly interface for both event organizers and attendees to manage events, bookings, and user profiles.

## Features

### User Features
- User registration and login
- View available events with detailed information
- Advanced search functionality for events
- Book events with multiple payment options
- View and manage personal bookings
- User profile management
- Loyalty points system
- View event descriptions and details

### Admin Features
- Event management (add, edit, delete events)
- Venue management
- User management
- View all bookings
- Advanced search for bookings
- Manage event categories and providers

### Event Management
- Add events with comprehensive details
- Set event duration and online status
- Manage event availability
- Set pricing and categories
- Link events to venues and providers

## Database Schema

The system uses the following main tables:
- User
- Event
- Booking
- Payment
- Category
- Provider
- Venue

## Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your MySQL database and update the connection details in `db_config.py`
4. Run the application:
   ```bash
   python tixify.py
   ```

## Usage

### User Login
- Register a new account or login with existing credentials
- Browse available events
- Use the search functionality to find specific events
- Book events and manage your bookings
- View and update your profile

### Admin Login
- Access the admin dashboard
- Manage events, venues, and users
- View all bookings and search through them
- Monitor the system's overall status

## Requirements

- Python 3.x
- MySQL
- Required Python packages (see requirements.txt)
