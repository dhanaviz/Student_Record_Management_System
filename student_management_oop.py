import json
import os


# Student Class
class Student:
    def __init__(self, student_id, name, department, marks, attendance):
        self.student_id = student_id
        self.name = name
        self.department = department
        self.marks = marks
        self.attendance = attendance
        self.status = "Active"

    @property
    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0

    def update(self, name=None, department=None, marks=None, attendance=None):
        if name:
            self.name = name
        if department:
            self.department = department
        if marks is not None:
            self.marks = marks
        if attendance is not None:
            self.attendance = attendance

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "marks": self.marks,
            "attendance": self.attendance,
            "status": self.status
        }


# FileManager Class
class FileManager:
    FILE_NAME = "students.json"

    @staticmethod
    def save(students):
        try:
            data = [s.to_dict() for s in students.values()]
            with open(FileManager.FILE_NAME, "w") as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully!")
        except (OSError, TypeError) as e:
            print("File saving error:", e)

    @staticmethod
    def load():
        students = {}
        if not os.path.exists(FileManager.FILE_NAME):
            return students

        try:
            with open(FileManager.FILE_NAME, "r") as file:
                data = json.load(file)

            for item in data:
                student = Student(
                    item["student_id"],
                    item["name"],
                    item["department"],
                    item["marks"],
                    item["attendance"]
                )
                student.status = item.get("status", "Active")
                students[student.student_id] = student

        except (OSError, ValueError, KeyError, TypeError) as e:
            print("File loading error:", e)

        return students


# StudentManager Class
class StudentManager:
    def __init__(self):
        self.students = FileManager.load()

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("Student ID already exists!")
        self.students[student.student_id] = student
        FileManager.save(self.students)

    def update_student(self, student_id, name, department):
        if student_id not in self.students:
            raise ValueError("Student not found!")
        self.students[student_id].update(name, department)
        FileManager.save(self.students)

    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError("Student not found!")
        del self.students[student_id]
        FileManager.save(self.students)

    def display_students(self):
        if not self.students:
            print("No students found.")
            return

        for student in self.students.values():
            print(
                student.student_id, "|",
                student.name, "|",
                student.department, "|",
                f"Average: {student.average:.1f}%"
            )


# ReportGenerator Class
class ReportGenerator:
    @staticmethod
    def generate(student):
        if student.average >= 75:
            performance = "Excellent"
        elif student.average >= 60:
            performance = "Good"
        elif student.average >= 40:
            performance = "Average"
        else:
            performance = "Needs Improvement"

        print("\nStudent Report")
        print("--------------------")
        print(student.student_id, "|", student.name, "|", student.department)
        print(f"Average: {student.average:.1f}%")
        print(f"Attendance: {student.attendance}%")
        print("Performance:", performance)
        print("Status:", student.status)


# Main Application
def main():
    manager = StudentManager()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Update Student")
        print("3. View Students")
        print("4. Generate Report")
        print("5. Delete Student")
        print("6. Save and Exit")

        try:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                sid = input("Student ID: ").strip()
                name = input("Name: ").strip()
                department = input("Department: ").strip()
                marks = [float(x) for x in input(
                    "Enter marks separated by commas: "
                ).split(",")]
                attendance = float(input("Attendance percentage: "))

                if not sid or not name or not department:
                    raise ValueError("Fields cannot be empty!")
                if not marks or any(m < 0 or m > 100 for m in marks):
                    raise ValueError("Marks must be between 0 and 100!")
                if not 0 <= attendance <= 100:
                    raise ValueError("Attendance must be between 0 and 100!")

                student = Student(sid, name, department, marks, attendance)
                manager.add_student(student)
                print("Student added successfully!")

            elif choice == "2":
                sid = input("Enter Student ID: ").strip()
                name = input("New Name: ").strip()
                department = input("New Department: ").strip()
                manager.update_student(sid, name, department)
                print("Student updated successfully!")

            elif choice == "3":
                manager.display_students()

            elif choice == "4":
                sid = input("Enter Student ID: ").strip()
                if sid not in manager.students:
                    raise ValueError("Student not found!")
                ReportGenerator.generate(manager.students[sid])

            elif choice == "5":
                sid = input("Enter Student ID: ").strip()
                manager.delete_student(sid)
                print("Student deleted successfully!")

            elif choice == "6":
                FileManager.save(manager.students)
                print("Thank you!")
                break

            else:
                print("Invalid choice! Try again.")

        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)


if __name__ == "__main__":
    main()