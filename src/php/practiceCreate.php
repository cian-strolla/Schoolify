<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// sql to create tables
$table1 = "CREATE TABLE USERS (
email VARCHAR(80) PRIMARY KEY,
password VARCHAR(50) NOT NULL,
account_type INT(1) NOT NULL
)";

$table2 = "CREATE TABLE STUDENTS (
email VARCHAR(80) PRIMARY KEY,
behaviour_points INT(4) NOT NULL,
test_grade_average INT(3) NOT NULL,
homework_grade_average INT(3) NOT NULL,
overall_grade_average INT(3) NOT NULL,
class INT(3) NOT NULL
)";

$table3 = "CREATE TABLE PARENTS (
email VARCHAR(80) PRIMARY KEY,
child_email1 VARCHAR(80) NOT NULL,
child_email2 VARCHAR(80),
child_email3 VARCHAR(80),
child_email4 VARCHAR(80),
child_email5 VARCHAR(80),
)";

$table4 = "CREATE TABLE ADMINS (
email VARCHAR(80) PRIMARY KEY,
)";

$table5 = "CREATE TABLE TEACHERS (
email VARCHAR(80) PRIMARY KEY,
class INT(3) NOT NULL
)";

$table6 = "CREATE TABLE SUBMISSIONS (
child_email VARCHAR(80) PRIMARY KEY,
teacher_email VARCHAR(80) NOT NULL,
file_name VARCHAR(80) NOT NULL
)";

$table7 = "CREATE TABLE HOMEWORK (
teacher_email VARCHAR(80) PRIMARY KEY,
file1 VARCHAR(80),
file2 VARCHAR(80),
file3 VARCHAR(80),
file4 VARCHAR(80),
file5 VARCHAR(80),
file6 VARCHAR(80),
file7 VARCHAR(80),
file8 VARCHAR(80),
file9 VARCHAR(80),
file10 VARCHAR(80),
)";

$table8 = "CREATE TABLE MATERIAL (
teacher_email VARCHAR(80) PRIMARY KEY,
file1 VARCHAR(80),
file2 VARCHAR(80),
file3 VARCHAR(80),
file4 VARCHAR(80),
file5 VARCHAR(80),
file6 VARCHAR(80),
file7 VARCHAR(80),
file8 VARCHAR(80),
file9 VARCHAR(80),
file10 VARCHAR(80),
)";

$table9 = "INSERT INTO homework (homework_id, teacher_email, student_id, filename, file_order, result, comments)
VALUES (2, 'johnhogan@gmail.com', '112', 'file2.txt', 2, 90, "Excellent Result!"),
VALUES (3, 'johnhogan@gmail.com', '112', 'file3.txt', 3, 45, "We'll have to talk :(");"



if ($conn->query($table1) === TRUE) {
    echo "table1 created successfully";
} else {
    echo "Error creating table1: " . $conn->error;
}


$conn->close();
?>
