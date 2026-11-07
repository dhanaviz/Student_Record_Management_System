# Student Record Management System
# Python Fundamentals Internship - Task D

import json
import os

FILE_NAME = "students.json"
PASS_MARK = 50

# Original Task 1 student records
students = [
    {
        "id": "S001",
        "name": "Dass",
        "age": 20,
        "department": "CSE",
        "marks": [78, 85, 72],
        "attendance": 91
    },
    {
        "id": "S002",
        "name": "Chandra",
        "age": 20,
        "department": "CSE",
        "marks": [65, 71, 68],
        "attendance": 84
    },
    {
        "id": "S003",
        "name": "Parvathi",
        "age": 19,
        "department": "ECE",
        "marks": [45, 52, 48],
        "attendance": 72
    }
]


# Calculate Average Mark
def calculate_average(student):
    return sum(student["marks"]) / len(student["marks"])


# Find Student by ID
def find_student(student_id):
    for student in students:
        if student["id"].lower() == student_id.lower():
            return student
    return None


# Save Records using JSON
def save_records():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(students, file, indent=4)
        print("Records saved successfully!")
    except (OSError, TypeError) as error:
        print("Error saving records:", error)


# Load Records from JSON
def load_records():
    global students

    if not os.path.exists(FILE_NAME):
        save_records()
        print("Original Task 1 records loaded.")
        return

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid file format. Keeping current records.")
            return

        for student in data:
            if not isinstance(student, dict):
                print("Invalid student data. Keeping current records.")
                return

            required = [
                "id", "name", "age", "department",
                "marks", "attendance"
            ]

            if not all(key in student for key in required):
                print("Invalid student record. Keeping current records.")
                return

            if (
                not isinstance(student["marks"], list)
                or len(student["marks"]) != 3
                or not all(
                    isinstance(mark, (int, float))
                    and 0 <= mark <= 100
                    for mark in student["marks"]
                )
                or not isinstance(student["attendance"], (int, float))
                or not 0 <= student["attendance"] <= 100
            ):
                print("Invalid student data. Keeping current records.")
                return

        ids = [student["id"].lower() for student in data]

        if len(ids) != len(set(ids)):
            print("Duplicate IDs found in file. Keeping current records.")
            return

        students = data
        print("Records loaded successfully!")

    except json.JSONDecodeError:
        print("File is empty or invalid. Keeping current records.")
    except OSError as error:
        print("Error loading records:", error)


# Get Valid Marks
def get_marks():
    while True:
        try:
            marks = list(map(float, input(
                "Enter 3 marks separated by commas: "
            ).split(",")))

            if len(marks) != 3:
                print("Enter exactly 3 marks.")
                continue

            if any(mark < 0 or mark > 100 for mark in marks):
                print("Marks must be between 0 and 100.")
                continue

            return marks

        except ValueError:
            print("Invalid marks. Enter numbers only.")


# Get Valid Attendance
def get_attendance():
    while True:
        try:
            attendance = float(input("Enter attendance percentage: "))

            if 0 <= attendance <= 100:
                return attendance

            print("Attendance must be between 0 and 100.")

        except ValueError:
            print("Enter a valid attendance percentage.")


# 1. Add Student
def add_student():
    print("\n--- ADD STUDENT ---")

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if find_student(student_id):
        print("Duplicate Student ID! Try another ID.")
        return

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Enter age: "))
        if age <= 0:
            print("Age must be positive.")
            return
    except ValueError:
        print("Invalid age.")
        return

    department = input("Enter department: ").strip()
    if not department:
        print("Department cannot be empty.")
        return

    marks = get_marks()
    attendance = get_attendance()

    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "department": department,
        "marks": marks,
        "attendance": attendance
    }

    students.append(student)
    save_records()
    print("Student added successfully!")


# 2. View All Students
def display_students():
    print("\n--- ALL STUDENT RECORDS ---")

    if not students:
        print("No student records available.")
        return

    for student in students:
        print("\n-------------------------")
        print("Student ID:", student["id"])
        print("Name:", student["name"])
        print("Age:", student["age"])
        print("Department:", student["department"])
        print("Marks:", student["marks"])
        print("Average:", round(calculate_average(student), 2))
        print("Attendance:", str(student["attendance"]) + "%")


# 3. Search Student
def search_student():
    print("\n--- SEARCH STUDENT ---")

    keyword = input("Enter Student ID or Name: ").strip().lower()

    if not keyword:
        print("Search cannot be empty.")
        return

    found = [
        student for student in students
        if keyword == student["id"].lower()
        or keyword in student["name"].lower()
    ]

    if not found:
        print("Student not found.")
        return

    for student in found:
        print("\nStudent Found")
        print("-------------------------")
        print("ID:", student["id"])
        print("Name:", student["name"])
        print("Department:", student["department"])
        print("Average:", round(calculate_average(student), 2), "%")
        print("Attendance:", student["attendance"], "%")


# 4. Update Student
def update_student():
    print("\n--- UPDATE STUDENT ---")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    print("Leave text fields empty to keep old values.")

    name = input("New name: ").strip()
    if name:
        student["name"] = name

    department = input("New department: ").strip()
    if department:
        student["department"] = department

    age = input("New age: ").strip()
    if age:
        try:
            new_age = int(age)
            if new_age > 0:
                student["age"] = new_age
            else:
                print("Invalid age. Old age retained.")
        except ValueError:
            print("Invalid age. Old age retained.")

    if input("Update marks? (y/n): ").lower() == "y":
        student["marks"] = get_marks()

    if input("Update attendance? (y/n): ").lower() == "y":
        student["attendance"] = get_attendance()

    save_records()
    print("Student updated successfully!")


# 5. Delete Student
def delete_student():
    print("\n--- DELETE STUDENT ---")

    student_id = input("Enter Student ID: ").strip()
    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    confirm = input("Confirm delete? (y/n): ").strip().lower()

    if confirm == "y":
        students.remove(student)
        save_records()
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")


# 6. Display Pass / Fail Results
def display_results():
    print("\n--- STUDENT RESULTS ---")

    if not students:
        print("No student records available.")
        return

    for student in students:
        average = calculate_average(student)
        result = "PASS" if average >= PASS_MARK else "FAIL"
        print(student["name"], "-", result)


# 7. Find Top Performer
def find_top_performer():
    if not students:
        print("No student records available.")
        return

    top_student = max(students, key=calculate_average)

    print("\n--- TOP PERFORMER ---")
    print("Name:", top_student["name"])
    print("Average:", round(calculate_average(top_student), 2))


# 8. Filter by Attendance
def filter_by_attendance():
    print("\n--- ATTENDANCE BELOW 75% ---")

    found = False

    for student in students:
        if student["attendance"] < 75:
            print(student["name"], "-", student["attendance"], "%")
            found = True

    if not found:
        print("No students found.")


# 9. Filter by Marks
def filter_by_marks():
    try:
        limit = float(input("Enter minimum average mark: "))

        if not 0 <= limit <= 100:
            print("Enter a mark between 0 and 100.")
            return

    except ValueError:
        print("Invalid mark.")
        return

    print("\n--- STUDENTS ABOVE MARK LIMIT ---")
    found = False

    for student in students:
        average = calculate_average(student)

        if average >= limit:
            print(student["name"], "-", round(average, 2))
            found = True

    if not found:
        print("No students found.")


# 10. Class Summary and Performance Report
def class_summary():
    print("\n--- CLASS PERFORMANCE REPORT ---")

    if not students:
        print("No student records available.")
        return

    total_students = len(students)
    all_marks = [
        mark for student in students
        for mark in student["marks"]
    ]

    class_average = sum(all_marks) / len(all_marks)

    print("Total Students:", total_students)
    print("Average Class Mark:", round(class_average, 2))

    display_results()
    find_top_performer()
    filter_by_attendance()


# Main Menu
def main():
    load_records()

    while True:
        print("\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Performance Report")
        print("7. Display Pass / Fail Results")
        print("8. Find Top Performer")
        print("9. Filter by Attendance")
        print("10. Filter by Marks")
        print("11. Class Summary")
        print("12. Save Records")
        print("13. Load Records")
        print("14. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            class_summary()
        elif choice == "7":
            display_results()
        elif choice == "8":
            find_top_performer()
        elif choice == "9":
            filter_by_attendance()
        elif choice == "10":
            filter_by_marks()
        elif choice == "11":
            class_summary()
        elif choice == "12":
            save_records()
        elif choice == "13":
            load_records()
        elif choice == "14":
            save_records()
            print("Thank you for using Student Record Management System!")
            break
        else:
            print("Invalid choice! Please select 1 to 14.")


# Run Program
if __name__ == "__main__":
    main()