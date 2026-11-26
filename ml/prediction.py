"""
Prediction Module
"""

import pandas as pd


def predict_student(model):
    """
    Predict placement status for a new student.
    """

    print("\n========== ENTER STUDENT DETAILS ==========\n")

    cgpa = float(input("CGPA: "))
    internships = int(input("Internships: "))
    projects = int(input("Projects: "))
    workshops = int(input("Workshops/Certifications: "))
    aptitude = int(input("Aptitude Test Score: "))
    softskills = int(input("Soft Skills Rating: "))
    extracurricular = int(input("Extracurricular Activities (0=No,1=Yes): "))
    training = int(input("Placement Training (0=No,1=Yes): "))
    ssc = float(input("SSC Marks: "))
    hsc = float(input("HSC Marks: "))

    student = pd.DataFrame([[
        cgpa,
        internships,
        projects,
        workshops,
        aptitude,
        softskills,
        extracurricular,
        training,
        ssc,
        hsc
    ]], columns=[
        "CGPA",
        "Internships",
        "Projects",
        "Workshops/Certifications",
        "AptitudeTestScore",
        "SoftSkillsRating",
        "ExtracurricularActivities",
        "PlacementTraining",
        "SSC_Marks",
        "HSC_Marks"
    ])

    prediction = model.predict(student)

    print("\n========== RESULT ==========")

    if prediction[0] == 1:
        print("🎉 Prediction: Placed")
    else:
        print("❌ Prediction: Not Placed")