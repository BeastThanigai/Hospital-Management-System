CREATE DATABASE ExpenseTrackerDB;

USE ExpenseTrackerDB;

CREATE TABLE expenses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date DATE,
  category VARCHAR(100),
  description VARCHAR(255),
  amount DOUBLE
);

desc expenses;

select * from expenses;