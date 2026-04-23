USE school_transport_db;

INSERT INTO buses (bus_number, capacity) VALUES
('BUS-101', 40),
('BUS-102', 35),
('BUS-103', 45);

INSERT INTO drivers (name, phone, license_no) VALUES
('Ravi Kumar', '9876543210', 'DL-1001'),
('Amit Singh', '9876543211', 'DL-1002'),
('Suresh Patel', '9876543212', 'DL-1003');

INSERT INTO routes (route_name, start_point, end_point, bus_id, driver_id) VALUES
('Route-A', 'Green Colony', 'School Main Gate', 1, 1),
('Route-B', 'Lake View', 'School Main Gate', 2, 2),
('Route-C', 'Hill Street', 'School Main Gate', 3, 3);

INSERT INTO stops (stop_name, area, route_id) VALUES
('Central Park Stop', 'Green Colony', 1),
('Temple Stop', 'Sector 5', 1),
('Market Stop', 'Lake View', 2),
('Post Office Stop', 'Old Town', 2),
('Bus Stand Stop', 'Hill Street', 3);

INSERT INTO students (student_name, grade, phone, stop_id) VALUES
('Ananya', '6', '9998887771', 1),
('Rahul', '7', '9998887772', 2),
('Meera', '8', '9998887773', 3),
('Karan', '6', '9998887774', 4),
('Pooja', '9', '9998887775', 5);

-- JOIN report for demo
SELECT st.student_name, st.grade, sp.stop_name, r.route_name, b.bus_number, d.name AS driver_name
FROM students st
JOIN stops sp ON st.stop_id = sp.stop_id
JOIN routes r ON sp.route_id = r.route_id
JOIN buses b ON r.bus_id = b.bus_id
JOIN drivers d ON r.driver_id = d.driver_id;
