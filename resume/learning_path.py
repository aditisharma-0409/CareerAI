# ==========================================
# Learning Recommendation Module
# ==========================================

LEARNING_PATH = {

    "Python": "Practice Python fundamentals and solve coding problems daily.",

    "SQL": "Learn SQL queries, joins, aggregation and database design.",

    "Machine Learning": "Study supervised and unsupervised learning and build ML projects.",

    "Deep Learning": "Learn Neural Networks, TensorFlow and PyTorch.",

    "Git": "Learn Git basics, branching, merging and GitHub.",

    "GitHub": "Create repositories, push code and collaborate using GitHub.",

    "Power BI": "Practice dashboard creation and data visualization.",

    "Tableau": "Build interactive dashboards using Tableau.",

    "Excel": "Master formulas, pivot tables and charts.",

    "Communication": "Improve communication through presentations and mock interviews.",

    "Problem Solving": "Practice DSA and logical reasoning regularly.",

    "React": "Build frontend applications using React.",

    "Node.js": "Learn backend development with Node.js.",

    "HTML": "Learn webpage structure using HTML.",

    "CSS": "Practice responsive web design using CSS.",

    "JavaScript": "Learn JavaScript fundamentals and DOM manipulation."
}


def get_learning_path(skill):

    return LEARNING_PATH.get(
        skill,
        "Explore online courses and practice projects."
    )