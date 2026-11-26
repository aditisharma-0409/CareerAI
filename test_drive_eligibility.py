
from backend.database.operations import (
    get_all_placement_drives,
    get_drive_eligibility_results
)

# Display available placement drives
drives = get_all_placement_drives()

print("\nAvailable Placement Drives:")
print(drives[["drive_id", "company_name", "drive_name"]])

if not drives.empty:

    drive_id = int(
        input("\nEnter the TCS sample drive ID: ")
    )

    results = get_drive_eligibility_results(drive_id)

    print("\nEligibility Results:")
    print(
        results[
            [
                "student_name",
                "email",
                "branch",
                "cgpa",
                "eligibility_status",
                "eligibility_reason"
            ]
        ].to_string(index=False)
    )

    print("\nEligibility Summary:")
    print(results["eligibility_status"].value_counts())

else:
    print("No placement drives found.")
