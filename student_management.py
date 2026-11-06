# Student Record Management System
# Python Fundamentals Internship Task

# Student Records using List and Dictionary

students = [
    {
        "name": "Dass",
        "age": 20,
        "department": "CSE",
        "marks": [78, 85, 72],
        "attendance": 91
    },
    {
        "name": "Chandra",
        "age": 20,
        "department": "CSE",
        "marks": [65, 71, 68],
        "attendance": 84
    },
    {
        "name": "Parvathi",
        "age": 19,
        "department": "ECE",
        "marks": [45, 52, 48],
        "attendance": 72
    }
]

PASS_MARK = 50


# 1. Calculate Average Mark
def calculate_average(student):
    return sum(student["marks"]) / len(student["marks"])


# 2. Display All Students
def display_students():
    print("\n--- STUDENT DETAILS ---")

    for student in students:
        print("\nName:", student["name"])
        print("Age:", student["age"])
        print("Department:", student["department"])
        print("Marks:", student["marks"])
        print("Average:", round(calculate_average(student), 1))
        print("Attendance:", str(student["attendance"]) + "%")


# 3. Identify Pass or Fail Students
def display_results():
    print("\n--- STUDENT RESULTS ---")

    for student in students:
        average = calculate_average(student)

        if average >= PASS_MARK:
            result = "PASS"
        else:
            result = "FAIL"

        print(student["name"], "-", result)


# 4. Find Top Performing Student
def find_top_performer():
    top_student = max(students, key=calculate_average)

    print("\n--- TOP PERFORMER ---")
    print("Name:", top_student["name"])
    print("Average:", round(calculate_average(top_student), 1))


# 5. Filter Students by Attendance
def filter_by_attendance():
    print("\n--- ATTENDANCE BELOW 75% ---")

    found = False

    for student in students:
        if student["attendance"] < 75:
            print(student["name"], "-", str(student["attendance"]) + "%")
            found = True

    if not found:
        print("No students found.")


# Filter Students by Average Marks
def filter_by_marks():
    limit = float(input("Enter minimum average mark: "))

    print("\n--- STUDENTS ABOVE THE MARK LIMIT ---")

    found = False

    for student in students:
        average = calculate_average(student)

        if average >= limit:
            print(student["name"], "-", round(average, 1))
            found = True

    if not found:
        print("No students found.")


# 6. Display Class Summary
def class_summary():
    total_students = len(students)

    all_marks = [
        mark
        for student in students
        for mark in student["marks"]
    ]

    class_average = sum(all_marks) / len(all_marks)

    print("\n--- CLASS SUMMARY ---")
    print("Total Students:", total_students)
    print("Average Class Mark:", round(class_average, 1))

    find_top_performer()
    filter_by_attendance()


# Add New Student
def add_student():
    print("\n--- ADD NEW STUDENT ---")

    name = input("Enter student name: ")
    age = int(input("Enter age: "))
    department = input("Enter department: ")

    marks = []

    for i in range(3):
        mark = float(input(f"Enter mark {i + 1}: "))
        marks.append(mark)

    attendance = float(input("Enter attendance percentage: "))

    student = {
        "name": name,
        "age": age,
        "department": department,
        "marks": marks,
        "attendance": attendance
    }

    students.append(student)

    print("Student added successfully!")


# Main Menu
def main():

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Display All Students")
        print("2. Calculate Average Marks")
        print("3. Display Pass / Fail Results")
        print("4. Find Top Performer")
        print("5. Filter by Attendance")
        print("6. Filter by Marks")
        print("7. Display Class Summary")
        print("8. Add New Student")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_students()

        elif choice == "2":
            for student in students:
                print(
                    student["name"],
                    "- Average:",
                    round(calculate_average(student), 1)
                )

        elif choice == "3":
            display_results()

        elif choice == "4":
            find_top_performer()

        elif choice == "5":
            filter_by_attendance()

        elif choice == "6":
            filter_by_marks()

        elif choice == "7":
            class_summary()

        elif choice == "8":
            add_student()

        elif choice == "9":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice! Please try again.")


# Run the Program
if __name__ == "__main__":
    main()