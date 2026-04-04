from crud import *
from analytics import *

def main():

    while True:
            print("\nChoose an option:")
            print("1. View Report Card")
            print("2. Add Student")
            print("3. Update Student Score")
            print("4. Delete Student")
            print("5. Top 3 Performers")
            print("6. Subject-wise Toppers")
            print("7. Weak students as per subject")
            print("8. Strong and weak subject for a specific student")
            print("9. Exit")

            choice = input("Enter your choice (1-9): ")

            if choice == '1':
                view_report_card()

            elif choice == '2':
                add_student()

            elif choice == '3':
                update_student_score()

            elif choice == '4':
                delete_student()

            elif choice == '5':
                top_performers()

            elif choice == '6':
                subject_toppers() 

            elif choice == '7': 
                weak_students_by_subject()

            elif choice == '8': 
                strong_weak_subject_for_student()

            elif choice == '9':
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  

