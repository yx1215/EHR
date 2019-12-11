DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS administrators;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS take_care;

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    gender TEXT CHECK (gender='male' or gender='female') NOT NULL,
    height TEXT NOT NULL,
    weight TEXT NOT NULL,
    data_of_birth TEXT NOT NULL,
    emergency_contacts TEXT
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    rate INTEGER CHECK (rate <= 10 and rate >=0) DEFAULT 0,
    number_of_rates INTEGER DEFAULT 0,
    gender TEXT CHECK (gender='male' or gender='female') NOT NULL,
    field TEXT NOT NULL,
    introduction TEXT,
    date_of_birth TEXT NOT NULL,
    date_of_join TEXT NOT NULL

);

CREATE TABLE administrators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    gender TEXT CHECK (gender='male' or gender='female' ) NOT NULL
);

CREATE TABLE take_care (
    doctor_id INTEGER,
    patient_id INTEGER,
    PRIMARY KEY (doctor_id, patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) on delete cascade,
    FOREIGN KEY (patient_id) REFERENCES patients (id) on delete cascade
);

CREATE TABLE schedule (
    doctor_id INTEGER,
    start_time TIMESTAMP NOT NULL,
    duration INTEGER NOT NULL check ( duration=30 or duration=60 ),
    occupied BOOLEAN NOT NULL,
    PRIMARY KEY (doctor_id, start_time),
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) on delete cascade
);

CREATE TABLE appointment (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    duration TEXT NOT NULL,
    location VARCHAR(8) NOT NULL,
    status VARCHAR(10) check ( status='pending' or status='accepted' ),
    medical_his TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id) on delete cascade,
    FOREIGN KEY (patient_id) REFERENCES patients (id) on delete cascade

);

