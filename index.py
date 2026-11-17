
import requests

FILE_NAME = "system_result.txt"

SUBJECTS = [
    "English",
    "Math",
    "Python",
    "Database",
    "Computer"
]

def detect_gender(name):
    try:
        response = requests.get(
            "https://api.genderize.io",
            params={"name": name.strip()},
            timeout=5
        )
        response.raise_for_status()

        data = response.json()
        gender = data.get("gender")

        if gender == "male":
            return "Male"
        elif gender == "female":
            return "Female"
        else:
            return "Unknown"

    except requests.RequestException:
        return "Unknown"



def get_integer(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Value must not exceed {maximum}.")
                continue

            return value

        except ValueError:
            print("Invalid input! Please enter a number.")



def read_all_students():
    students = []
    student = {}

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.startswith("Student ID:"):
                if student:
                    students.append(student)

                student = {
                    "student_id": int(line.split(":", 1)[1].strip())
                }

            elif line.startswith("Student Name:"):
                student["name"] = line.split(":", 1)[1].strip()

            elif line.startswith("Gender:"):
                student["gender"] = line.split(":", 1)[1].strip()

            elif line.startswith("English:"):
                student["English"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("Math:"):
                student["Math"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("Python:"):
                student["Python"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("Database:"):
                student["Database"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("Computer:"):
                student["Computer"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("Total:"):
                student["total"] = line.split(":", 1)[1].strip()

            elif line.startswith("Percentage:"):
                student["percentage"] = line.split(":", 1)[1].strip()

            elif line.startswith("Grade:"):
                student["grade"] = line.split(":", 1)[1].strip()

            elif line.startswith("Division:"):
                student["division"] = line.split(":", 1)[1].strip()

            elif line.startswith("Result:"):
                student["result"] = line.split(":", 1)[1].strip()

        if student:
            students.append(student)

    except FileNotFoundError:
        pass

    except (ValueError, OSError) as error:
        print("File reading error:", error)

    return students



def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "E"



def calculate_division(percentage):
    if percentage >= 60:
        return "First"
    elif percentage >= 45:
        return "Second"
    else:
        return "Third"



def display_student(student):
    print("\n========== STUDENT RESULT ==========")
    print("Student ID:", student.get("student_id", "N/A"))
    print("Student Name:", student.get("name", "N/A"))
    print("Gender:", student.get("gender", "N/A"))

    for subject in SUBJECTS:
        print(f"{subject} Marks:", student.get(subject, "N/A"))

    print("Total:", student.get("total", "N/A"))
    print("Percentage:", student.get("percentage", "N/A"))
    print("Grade:", student.get("grade", "N/A"))
    print("Division:", student.get("division", "N/A"))
    print("Result:", student.get("result", "N/A"))
    print("====================================")



def save_student(student):
    try:
        with open(FILE_NAME, "a", encoding="utf-8") as file:
            file.write(f"Student ID: {student['student_id']}\n")
            file.write(f"Student Name: {student['name']}\n")
            file.write(f"Gender: {student['gender']}\n")

            for subject in SUBJECTS:
                file.write(f"{subject}: {student[subject]}\n")

            file.write(f"Total: {student['total']}\n")
            file.write(f"Percentage: {student['percentage']}\n")
            file.write(f"Grade: {student['grade']}\n")
            file.write(f"Division: {student['division']}\n")
            file.write(f"Result: {student['result']}\n")
            file.write("-----------------------------------\n")

        print("\nResult Saved Successfully!")

    except OSError as error:
        print("File saving error:", error)


# 8. Add Student Result
def get_student_result():
    print("\n--- Add Student Result ---")

    student_id = get_integer(
        "Enter Student ID: ",
        minimum=1
    )


    students = read_all_students()

    for old_student in students:
        if old_student.get("student_id") == student_id:
            print("\nStudent ID already exists!")
            print("Please use a different Student ID.")
            print("System closed.")
            return "DUPLICATE"

    student_Name = input("Enter Student Name: ").strip()

    while not student_Name:
        print("Name cannot be empty!")
        student_Name = input("Enter Student Name: ").strip()

    # Automatic Gender Prediction
    print("Detecting gender...")
    gender = detect_gender(student_Name)
    print("Gender:", gender)

    marks = {}

    for subject in SUBJECTS:
        marks[subject] = get_integer(
            f"Enter {subject} Marks (0-100): ",
            minimum=0,
            maximum=100
        )

    total = sum(marks.values())
    percentage = total / len(SUBJECTS)
    grade = calculate_grade(percentage)
    division = calculate_division(percentage)

    if any(mark < 33 for mark in marks.values()):
        result = "Fail"
    else:
        result = "Pass"

    student = {
        "student_id": student_id,
        "name": student_Name,
        "gender": gender,
        **marks,
        "total": f"{total}/500",
        "percentage": f"{percentage:.2f}%",
        "grade": grade,
        "division": division,
        "result": result
    }

    display_student(student)
    save_student(student)

    return student


# 9. Search Student by ID (Only Name)
def search_student():
    print("\n--- Search Student ---")

    search_id = get_integer(
        "Enter Student ID to Search: ",    
        minimum=1
    )

    students = read_all_students()

    for student in students:
        if student.get("student_id") == search_id:
            print("Student Name:", student.get("name", "N/A"))
            return

    print("Student ID not found!")


# 10. View All Students
def view_all_students():
    print("\n--- All Saved Students ---")

    students = read_all_students()

    if not students:
        print("No student records found.")
        return

    for student in students:
        display_student(student)


# 11. Main Menu
def main():
    while True:
        print("\n====== STUDENT MANAGEMENT SYSTEM ======")
        print("1. Add Student Result")
        print("2. Search Student by ID")
        print("3. View All Saved Students")
        print("4. Exit")

        choice = get_integer(
            "Enter your choice (1-4): ",
            minimum=1,
            maximum=4
        )

        if choice == 1:
            result = get_student_result()

            if result == "DUPLICATE":
                break

        elif choice == 2:
            search_student()

        elif choice == 3:
            view_all_students()

        elif choice == 4:
            print("Thank you for using Student Management System! ")
            break


if __name__ == "__main__":
    main()


