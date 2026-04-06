from db import get_connection
from utils import validate_input


def view_report_card():
    conn = get_connection()
    cursor = conn.cursor()

    name = validate_input("Enter the name of the student: ", str)
    query = """
        SELECT sub.subject_name, m.score
        FROM marks m
        JOIN students s ON s.std_id = m.std_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE s.std_name = %s
        ORDER BY sub.subject_name
        """
    cursor.execute(query, (name,))
    results = cursor.fetchall()

    if not results:
        print("No records found for the student.")  
    else:
        print("\n" + "="*30)
        print(f"Report Card: {name}")
        print("="*30)

        total_score = 0

        for subject_name, score in results:
            print(f"{subject_name}: {score}")
                    
            total_score += score

            if score >= 90:
                grade = 'A'
            elif score >= 75:
                grade = 'B'
            elif score >= 50:   
                grade = 'C'
            else:
                grade = 'F'
            
            print(f"grade: {grade}")
            print("\n" + "="*30)
        average_score = total_score / len(results)
        print(f"Total Score: {total_score}")
        print(f"Average Score: {average_score:.2f}")
        print(f"Grade: {grade}")
    if results == True:
        
        max_score = max(score for _, score in results)
        min_score = min(score for _, score in results)
    
        variance = max_score - min_score
        if variance > 40:
            print("Warning: The student's performance is inconsistent across subjects. Need urgent attention to weaker subjects.")
        elif variance < 10:
            print("The student's performance is consistent across subjects. Keep up the good work!")
        else:
            print("The student's performance shows some variation across subjects. Consider focusing on weaker subjects for improvement.")
    cursor.close()
    conn.close()

def add_student():
    conn = get_connection()
    cursor = conn.cursor()

    print("Adding a new student...")
    name = validate_input("Enter the name of the student: ", str)
    try:
        age = validate_input("Enter the age of the student: ", int)
    except ValueError:
        print("Invalid input for age. Please enter a valid integer.")
        return
    city = validate_input("Enter the city of the student: ", str)

    # Insert the new student into the database
    cursor.execute("INSERT INTO students (std_name, age, city) VALUES (%s, %s, %s)", (name, age, city))
    conn.commit()

    std_id = cursor.lastrowid
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    print("Available Subjects:")
    for subject in subjects:
        print(f"ID: {subject[0]}, Name: {subject[1]}")
    print("Enter subject IDs for this student separated by commas (e.g., 1,2,3): ")
    subjects = input().split(',')
    
    
    for sub in subjects:
        cursor.execute(
            "INSERT INTO student_subjects (std_id, subject_id) VALUES (%s, %s)", (std_id, int(sub.strip())) 
        )
        #Add score for the student in the marks table   
        score = validate_input(f"Enter the score for subject ID {sub.strip()}: ", int)
        if score < 0 or score > 100:
            print("Invalid score. Please enter a value between 0 and 100.Retry adding the student.")
            conn.rollback()
            return
        cursor.execute(
            "INSERT INTO marks (std_id, subject_id, score) VALUES (%s, %s, %s)", (std_id, int(sub.strip()), score) 
        )   
        conn.commit()
    print("Student added successfully.")

    cursor.close()
    conn.close()    
    
def update_student_score():
    conn = get_connection()
    cursor = conn.cursor()

    name = validate_input("Enter the name of the student: ", str)
    if not name.strip():
        print("Student name cannot be empty.")
        return
    cursor.execute("SELECT std_id FROM students WHERE std_name = %s", (name,))

    result = cursor.fetchone()

    if not result:
        print("Student not found.")
        return
    
    cursor.execute(
        """
        SELECT sub.subject_id, sub.subject_name, m.score
        FROM marks m
        JOIN students s ON m.std_id = s.std_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE s.std_name = %s
        ORDER BY sub.subject_name""", (name,)
    )

    subjects = cursor.fetchall()
    if not subjects:
        print("No subjects found for the student.")
        return
    
    print("Subjects and current scores:")
    for subject_id, subject_name, score in subjects:
        print(f"ID: {subject_id}, Name: {subject_name}, Current Score: {score}")   

    subject_id = int(input("Enter the subject ID to update the score for: "))
    try:
        cursor.execute("SELECT subject_id FROM subjects WHERE subject_id = %s", (subject_id,))
        if not cursor.fetchone():
            print("Subject not found.")
            conn.rollback()
            return
    except ValueError:
        print("Invalid input for subject ID. Please enter a valid integer.")
        return
    new_score = validate_input("Enter the new score: ", int)
    if not (0 <= new_score <= 100):
        print("Invalid score. Please enter a value between 0 and 100.")
        return
    cursor.execute("""
        UPDATE marks m
        JOIN students s ON m.std_id = s.std_id
        SET m.score = %s
        WHERE s.std_name = %s AND m.subject_id = %s
    """, (new_score, name, subject_id))

    cursor.execute("""
        SELECT sub.subject_name, m.score
        FROM marks m
        JOIN students s ON m.std_id = s.std_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE s.std_name = %s AND m.subject_id = %s
    """, (name, subject_id))
    updated_record = cursor.fetchone()
    if updated_record:
        subject_name, score = updated_record
        print(f"Updated Score for {subject_name}: {score}")

    conn.commit()
    if cursor.rowcount > 0:
        print("Score updated successfully.")
    else:
        print("Student or subject not found. Score update failed.") 
    
    cursor.close()
    conn.close()

def delete_student():
    conn = get_connection()
    cursor = conn.cursor()

    name = validate_input("Enter the name of the student to delete: ", str)
    cursor.execute("SELECT std_id FROM students WHERE std_name = %s", (name,))
    result = cursor.fetchone()
    if not result:
        print("Student not found.")
        return

    std_id = result[0]
    cursor.execute("DELETE FROM marks WHERE std_id = %s", (std_id,))
    cursor.execute("DELETE FROM student_subjects WHERE std_id = %s", (std_id,))
    cursor.execute("DELETE FROM students WHERE std_id = %s", (std_id,))
    conn.commit()
    print("Student deleted successfully.")

    cursor.close()
    conn.close()



    

