CREATE DATABASE careerai_db;

USE careerai_db;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender ENUM('Male','Female','Other'),
    branch VARCHAR(50),
    cgpa DECIMAL(3,2),
    tenth_percentage DECIMAL(5,2),
    twelfth_percentage DECIMAL(5,2),
    skills TEXT,
    projects INT DEFAULT 0,
    internships INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students
(name,email,password,gender,branch,cgpa,tenth_percentage,twelfth_percentage,skills,projects,internships)
VALUES
('Aditi Sharma','aditi@gmail.com','123456','Female','Computer Science',8.75,90,88,'Python, SQL, Machine Learning',4,2),
('Rahul Kumar','rahul@gmail.com','123456','Male','Computer Science',9.10,95,92,'Python, Java',5,3),
('Priya Singh','priya@gmail.com','123456','Female','Information Technology',8.20,91,89,'Python, SQL, Power BI',3,1),
('Arjun Sharma','arjun@gmail.com','123456','Male','Artificial Intelligence',7.90,86,84,'Python, C++',2,1),
('Sneha Patel','sneha@gmail.com','123456','Female','Computer Science',9.40,96,94,'Python, Deep Learning',6,2);