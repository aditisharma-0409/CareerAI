"""
Database Operations
"""

import pandas as pd
from backend.database.connection import create_connection


def get_students_dataframe():
    """
    Fetch all students and return a Pandas DataFrame.
    """

    connection = create_connection()

    query = "SELECT * FROM students"

    df = pd.read_sql(query, connection)

    connection.close()

    return df

# ==========================================
# Save Prediction History
# ==========================================

def save_prediction(user_id, student_name, job_role, prediction, confidence):
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO prediction_history
    (user_id, student_name, job_role, prediction, confidence)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        student_name,
        job_role,
        prediction,
        confidence
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
# ==========================================
# Get Prediction History
# ==========================================

def get_prediction_history(user_id=None):
    """
    Fetch prediction history from MySQL.

    If user_id is provided:
    → Fetch only that student's predictions.

    If user_id is not provided:
    → Fetch all predictions (for Admin).
    """

    connection = create_connection()
    cursor = connection.cursor()

    if user_id is not None:

        query = """
        SELECT
            student_name,
            job_role,
            prediction,
            confidence,
            created_at
        FROM prediction_history
        WHERE user_id = %s
        ORDER BY created_at DESC
        """

        cursor.execute(query, (user_id,))

    else:

        query = """
        SELECT
            student_name,
            job_role,
            prediction,
            confidence,
            created_at
        FROM prediction_history
        ORDER BY created_at DESC
        """

        cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "Student Name",
        "Job Role",
        "Prediction",
        "Confidence (%)",
        "Date & Time"
    ]

    df = pd.DataFrame(rows, columns=columns)

    cursor.close()
    connection.close()

    return df
# ==========================================
# Dashboard Statistics
# ==========================================

def get_dashboard_stats():
    """
    Return dashboard statistics.
    """

    connection = create_connection()

    cursor = connection.cursor()

    # Total Predictions
    cursor.execute("SELECT COUNT(*) FROM prediction_history")
    total_predictions = cursor.fetchone()[0]

    # Placed Students
    cursor.execute(
        "SELECT COUNT(*) FROM prediction_history WHERE prediction='Placed'"
    )
    placed_students = cursor.fetchone()[0]

    # Not Placed Students
    cursor.execute(
        "SELECT COUNT(*) FROM prediction_history WHERE prediction='Not Placed'"
    )
    not_placed_students = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return (
        total_predictions,
        placed_students,
        not_placed_students
    )

# ==========================================
# Admin - Student Records
# ==========================================

def get_student_records():
    """
    Fetch student records for Admin.
    """

    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        u.user_id,
        u.full_name,
        u.email,
        u.role,
        p.job_role,
        p.prediction,
        p.confidence,
        p.created_at
    FROM users u
    LEFT JOIN prediction_history p
        ON u.user_id = p.user_id
    WHERE u.role = 'student'
    ORDER BY p.created_at DESC
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "User ID",
        "Student Name",
        "Email",
        "Role",
        "Target Job Role",
        "Prediction",
        "Confidence (%)",
        "Date & Time"
    ]

    df = pd.DataFrame(rows, columns=columns)

    cursor.close()
    connection.close()

    return df

# ==========================================
# Resume Operations
# ==========================================

def save_resume(
    user_id,
    file_name,
    file_path,
    target_job_role,
    resume_score,
    resume_status,
    detected_skills,
    missing_skills
):
    """
    Save a student's resume analysis in MySQL.
    """

    connection = create_connection()
    cursor = connection.cursor()

    # Convert skill lists into text
    detected_skills_text = ", ".join(detected_skills)
    missing_skills_text = ", ".join(missing_skills)

    query = """
    INSERT INTO resumes
    (
        user_id,
        file_name,
        file_path,
        target_job_role,
        resume_score,
        resume_status,
        detected_skills,
        missing_skills
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        file_name,
        file_path,
        target_job_role,
        resume_score,
        resume_status,
        detected_skills_text,
        missing_skills_text
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

def get_student_resumes():
    """
    Fetch all student resumes for Admin.
    """

    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        r.resume_id,
        u.user_id,
        u.full_name,
        u.email,
        r.file_name,
        r.target_job_role,
        r.resume_score,
        r.resume_status,
        r.detected_skills,
        r.missing_skills,
        r.uploaded_at
    FROM resumes r
    JOIN users u
        ON r.user_id = u.user_id
    WHERE u.role = 'student'
    ORDER BY r.uploaded_at DESC
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "Resume ID",
        "User ID",
        "Student Name",
        "Email",
        "File Name",
        "Target Job Role",
        "Resume Score",
        "Resume Status",
        "Detected Skills",
        "Missing Skills",
        "Uploaded At"
    ]

    df = pd.DataFrame(rows, columns=columns)

    cursor.close()
    connection.close()

    return df

def get_resume_by_user(user_id):
    """
    Fetch the latest resume of a particular student.
    """

    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        resume_id,
        file_name,
        file_path,
        target_job_role,
        resume_score,
        resume_status,
        detected_skills,
        missing_skills,
        uploaded_at
    FROM resumes
    WHERE user_id = %s
    ORDER BY uploaded_at DESC
    LIMIT 1
    """

    cursor.execute(query, (int(user_id),))

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row