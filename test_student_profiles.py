
from backend.database.operations import (
    save_student_profile,
    get_student_profile,
    get_all_student_profiles
)

# Test with an existing student account
user_id = 3

test_profile = {
    "phone": "9876543210",
    "city": "Jalandhar",
    "state": "Punjab",
    "university": "DAV University",
    "course": "B.Tech",
    "branch": "CSE-AI",
    "graduation_year": 2027,
    "cgpa": 9.0,
    "tenth_percentage": 94.0,
    "twelfth_percentage": 99.0,
    "active_backlogs": 0,
    "internships": 2,
    "projects": 3,
    "technical_skills": "Python, SQL, Machine Learning",
    "certifications": "Data Science",
    "preferred_job_role": "Data Scientist"
}

# Save profile
save_student_profile(user_id, test_profile)

print("Profile saved successfully!")

# Retrieve profile
profile = get_student_profile(user_id)

print("\nStudent Profile:")
print(profile)

# Retrieve all student profiles
students = get_all_student_profiles()

print("\nAll Student Records:")
print(students)
