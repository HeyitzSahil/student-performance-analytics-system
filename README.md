# Student Performance Analytics System (CLI)

A command-line based analytics system built using Python and MySQL to manage, process, and derive insights from student academic performance data.

## 🚀 Key Highlights

* Generates detailed student report cards
* Identifies top performers based on average scores
* Detects weak students subject-wise
* Finds subject-wise toppers using advanced SQL queries
* Modular backend architecture (CRUD + Analytics separation)

## 🛠️ Tech Stack

* Python
* MySQL
* MySQL Connector

## 📂 Project Structure

* db.py → Database connection
* crud.py → CRUD operations
* analytics.py → Performance analysis logic
* main.py → CLI interface

## ⚙️ Setup Instructions

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Setup MySQL database using provided schema (or manually create tables):
   
   CREATE TABLE students (
	std_id INT PRIMARY KEY AUTO_INCREMENT,
    std_name VARCHAR(50),
    age INT,
    city VARCHAR(50)
);

CREATE TABLE subjects (
	subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(50)
);

CREATE TABLE marks (
	marks_id INT PRIMARY KEY AUTO_INCREMENT,
    std_id INT,
    subject_id INT,
    score INT,
    FOREIGN KEY (std_id) REFERENCES students(std_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

ALTER TABLE students 
MODIFY std_name VARCHAR(50) NOT NULL;

ALTER TABLE marks 
MODIFY score INT NOT NULL;

CREATE INDEX idx_std_id ON marks(std_id);
CREATE INDEX idx_subject_id ON marks(subject_id);

CREATE TABLE student_subjects (
    std_id INT,
    subject_id INT,
    PRIMARY KEY (std_id, subject_id),
    FOREIGN KEY (std_id) REFERENCES students(std_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

ALTER TABLE marks
ADD CONSTRAINT fk_valid_subject
FOREIGN KEY (std_id, subject_id)
REFERENCES student_subjects(std_id, subject_id);

4. Run the application:
   python main.py

## 📊 Sample Features Output

* Student Report Card with total, average, and grade
* Top 3 performers ranked by average score
* Weak students listed per subject

## 🔮 Future Enhancements

* School and class hierarchy system
* Stream-based subject mapping (Science, Commerce, Arts)
* Advanced analytics dashboard
* AI-based performance recommendation system

## 👤 Author

Sahil Mukherjee
