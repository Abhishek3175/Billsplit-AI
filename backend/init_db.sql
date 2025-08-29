-- BillSplit AI Database Initialization Script
-- Run this script to create the database and tables

-- Create database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS billsplit_db;
USE billsplit_db;

-- Create Bill table
CREATE TABLE IF NOT EXISTS Bill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_date VARCHAR(50),
    vendor VARCHAR(255),
    subtotal FLOAT,
    tax FLOAT,
    total FLOAT,
    currency VARCHAR(10) DEFAULT 'USD',
    items_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_bill_date ON Bill(bill_date);
CREATE INDEX IF NOT EXISTS idx_vendor ON Bill(vendor);
CREATE INDEX IF NOT EXISTS idx_created_at ON Bill(created_at);

-- Insert sample data (optional)
INSERT INTO Bill (bill_date, vendor, subtotal, tax, total, currency, items_json) VALUES
('2024-01-15', 'Sample Restaurant', 45.00, 3.60, 48.60, 'USD', 
 '[{"name": "Burger", "quantity": 2, "price": 15.00}, {"name": "Fries", "quantity": 1, "price": 8.00}, {"name": "Soda", "quantity": 1, "price": 7.00}]');

-- Show table structure
DESCRIBE Bill;

-- Show sample data
SELECT * FROM Bill;
