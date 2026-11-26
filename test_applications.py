from backend.database.connection import create_connection

from backend.database.operations import (
    apply_for_placement,
    get_student_applications,
    get_drive_applications,
    get_all_placement_drives
)


# Step 1: Enter student email
student_email = input("Enter student email: ")

connection = create_connection()
cursor = connection.cursor()

cursor.execute(
    "SELECT user_id, full_name FROM users WHERE email = %s AND role = 'student'",
    (student_email,)
)

student = cursor.fetchone()

cursor.close()
connection.close()

if student is None:
    print("Student account not found.")

else:
    user_id = student[0]

    print(f"\nStudent: {student[1]}")
    print(f"User ID: {user_id}")

    # Step 2: Display available drives
    drives = get_all_placement_drives()

    print("\nAvailable Placement Drives:")
    print(
        drives[
            ["drive_id", "company_name", "drive_name"]
        ].to_string(index=False)
    )

    # Step 3: Select a drive
    drive_id = int(input("\nEnter drive ID: "))

    # Step 4: Submit application
    success, message = apply_for_placement(
        user_id,
        drive_id
    )

    print("\nApplication Result:")
    print(message)

    # Step 5: Display student's applications
    print("\nStudent Applications:")

    applications = get_student_applications(user_id)
    print(applications)

    # Step 6: Display all applicants for this drive
    print("\nApplications Received for This Drive:")

    drive_applications = get_drive_applications(drive_id)
    print(drive_applications)