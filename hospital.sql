use hospital;
select * from lab_tests;
describe billing;
describe insurance;
describe patients;
describe doctors;

-- Add a sample patient
INSERT INTO patients (name, age, gender, contact, address, medical_history)
VALUES ('John Doe', 35, 'Male', '1234567890', '123 Main St, City', 'No medical history');

-- Get the patient ID
SET @patient_id = LAST_INSERT_ID();

-- Add sample insurance data
INSERT INTO insurance (patient_id, provider, policy_number)
VALUES (@patient_id, 'HealthCare Co.', 'HC123456789');

describe insurance;
CREATE TABLE insurance_claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    provider VARCHAR(100),
    policy_number VARCHAR(50),
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

select * from insurance_claims;
select * from pharmacy;
select * from suppliers;
select id from suppliers where name='hello';
select id from pharmacy where supplier_id=2 && medicine_name='tablet2';
describe pharmacy;
describe suppliers;

select * from patients;
SELECT * 
FROM pharmacy 
WHERE supplier_id NOT IN (SELECT id FROM suppliers);


SELECT p.*
FROM pharmacy p
LEFT JOIN suppliers s ON p.supplier_id = s.id
WHERE s.id IS NULL;

SELECT p.medicine_name, p.stock, p.expiry_date, s.name AS supplier_name
FROM pharmacy p
JOIN suppliers s ON p.supplier_id = s.id;

select * from users;
select * from medical_records;
SELECT * FROM DOCTORS;
select * from patients;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM doctors WHERE id IN (SELECT id FROM users WHERE role = 'Doctor');
DELETE FROM users WHERE id = '12';
delete from medical_records;
delete from pharmacy;

SET SQL_SAFE_UPDATES = 1;

describe appointments;
describe doctors;
select * from doctors;
select * from users;
select * from appointments;
select * from patients;
ALTER TABLE medical_records ADD COLUMN date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE appointments
MODIFY COLUMN status ENUM('Scheduled', 'Completed', 'Cancelled', 'Waiting');


ALTER TABLE billing ADD COLUMN final_amount DECIMAL(10, 2) AFTER amount;
ALTER TABLE insurance ADD COLUMN coverage_percent INT DEFAULT 0;

drop table pharmacy;
CREATE TABLE pharmacy (
    id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_name VARCHAR(255),
    stock INT,
    expiry_date DATE,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
select * from pharmacy;
describe pharmacy;
select * from suppliers;
select * from lab_tests;


