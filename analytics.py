from db import get_connection

def top_performers():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT s.std_name, AVG(m.score) AS average_score, SUM(m.score) AS total_score
        FROM students s
        JOIN marks m ON s.std_id = m.std_id
        GROUP BY s.std_id
        ORDER BY average_score DESC
        LIMIT 5
    """
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("No records found.")
    else:
        print("\n" + "="*30)
        print("Top Performers")
        print("="*30)
        for std_name, average_score, total_score in results:
            print(f"{std_name}: {average_score:.2f} (Total: {total_score})")

    cursor.close()
    conn.close()

def subject_toppers():
    conn = get_connection()
    cursor = conn.cursor()

    query = """ 
        SELECT s.std_name, sub.subject_name, m.score
        FROM students s
        JOIN marks m ON s.std_id = m.std_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE (m.subject_id, m.score) IN (
            SELECT subject_id, MAX(score)
            FROM marks
            GROUP BY subject_id
        )
        ORDER BY sub.subject_name
    """
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("No records found.")
    else:
        print("\n" + "="*40)
        print("Subject Toppers")
        print("="*40)
        for std_name, subject_name, score in results:
            print(f"{subject_name}: {std_name} - {score}")

    cursor.close()
    conn.close()

def weak_students_by_subject():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT sub.subject_name, s.std_name, m.score
        FROM subjects sub
        JOIN marks m ON sub.subject_id = m.subject_id
        JOIN students s ON m.std_id = s.std_id
        WHERE m.score < 50
        ORDER BY sub.subject_name, m.score ASC
    """
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("No records found, or no weak students identified.")
        return
    else:
        print("\n" + "="*40)
        print("Weak Students by Subject")
        print("="*40)
        current_subject = None
        for subject_name, std_name, score in results:
            if subject_name != current_subject:
                print(f"\n{subject_name}:")
                current_subject = subject_name
            print(f"  {std_name} - {score}")
    cursor.close()
    conn.close()

def strong_weak_subject_for_student():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter the name of the student: ")

    cursor.execute("""
        SELECT sub.subject_name, m.score,
               CASE 
                   WHEN m.score >= 90 THEN 'Strong'
                   WHEN m.score >= 75 THEN 'Moderate'
                   WHEN m.score >= 50 THEN 'Average'
                   ELSE 'Weak'
                END      
        FROM marks m
        JOIN students s ON s.std_id = m.std_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE s.std_name = %s
        """, (name,))
    
    results = cursor.fetchall()

    if not results:
        print("No records found for the student.")  
    else:
        print(f"\nPerformance of {name}:")
        print("="*30)
        for subject_name, score, performance in results:
            print(f"{subject_name}: {score} ({performance})")
        
        strong_subject = max(results, key=lambda x: x[1])
        weak_subject = min(results, key=lambda x: x[1])
        print("\n" + "="*30)
        print("\nStrongest Subject:")
        print(f"{strong_subject[0]} - {strong_subject[1]} ({strong_subject[2]})")
        print("\nWeakest Subject:")
        print(f"{weak_subject[0]} - {weak_subject[1]} ({weak_subject[2]})")
        print("="*30)
    cursor.close()
    conn.close()