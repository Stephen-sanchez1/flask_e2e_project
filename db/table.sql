CREATE DATABASE diabetic_patient_registry;
USE diabetic_patient_registry;
CREATE TABLE diabetic_patient_info (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    blood_sugar_level DECIMAL(5, 2),
    last_checkup_date DATE
);
