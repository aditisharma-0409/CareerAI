# ==========================================
# Skill Extractor
# ==========================================

def extract_skills(resume_text):
    """
    Extracts known skills from resume text.
    """

    skills_database = [

        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "MySQL",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Artificial Intelligence",
        "Power BI",
        "Excel",
        "Tableau",
        "Git",
        "GitHub",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Flask",
        "Django",
        "TensorFlow",
        "PyTorch",
        "Communication",
        "Leadership",
        "Problem Solving",
        "Teamwork"
    ]

    found_skills = []

    resume_text = resume_text.lower()

    for skill in skills_database:

        if skill.lower() in resume_text:

            found_skills.append(skill)

    return found_skills