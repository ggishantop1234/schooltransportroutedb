CREATE DATABASE IF NOT EXISTS school_transport_db;
USE school_transport_db;

CREATE TABLE buses (
    bus_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_number VARCHAR(20) UNIQUE NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0)
);

CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    license_no VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(50) UNIQUE NOT NULL,
    start_point VARCHAR(100) NOT NULL,
    end_point VARCHAR(100) NOT NULL,
    bus_id INT NOT NULL,
    driver_id INT NOT NULL,
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id) ON DELETE RESTRICT,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE RESTRICT
);

CREATE TABLE stops (
    stop_id INT AUTO_INCREMENT PRIMARY KEY,
    stop_name VARCHAR(100) NOT NULL,
    area VARCHAR(100) NOT NULL,
    route_id INT NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    grade VARCHAR(20) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    stop_id INT NOT NULL,
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id) ON DELETE RESTRICT
);
