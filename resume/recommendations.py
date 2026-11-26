# ==========================================
# CareerAI
# Job Role Skill Recommendation Module
# ==========================================

JOB_SKILLS = {

    "Data Scientist": [

        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "NumPy",
        "Power BI",
        "Tableau",
        "Git",
        "Communication"
    ],

    "AI Engineer": [

        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Git",
        "SQL",
        "Problem Solving"
    ],

    "Data Analyst": [

        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Statistics",
        "Communication"
    ],

    "Software Developer": [

        "Python",
        "Java",
        "C++",
        "SQL",
        "Git",
        "GitHub",
        "Problem Solving",
        "Communication"
    ],

    "Web Developer": [

        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Git",
        "GitHub"
    ]

}


def recommend_skills(found_skills, job_role):

    required_skills = JOB_SKILLS.get(job_role, [])

    missing_skills = []

    for skill in required_skills:

        if skill not in found_skills:

            missing_skills.append(skill)

    return missing_skills