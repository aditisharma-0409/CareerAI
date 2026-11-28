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
    Fetch all students for Admin along with their latest
    placement prediction if available.
    Uses two simple SELECT queries + Python selection to avoid
    TiDB JOIN/subquery parser error 1105.
    """
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                user_id,
                full_name,
                email,
                role
            FROM users
            WHERE role = 'student'
            ORDER BY user_id ASC
            """
        )
        students = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                job_role,
                prediction,
                confidence,
                created_at
            FROM prediction_history
            ORDER BY created_at DESC, id DESC
            """
        )
        predictions = cursor.fetchall()

        latest_by_user = {}
        for pred in predictions:
            uid = pred.get("user_id")
            if uid is not None and uid not in latest_by_user:
                latest_by_user[uid] = pred

        records = []
        for stu in students:
            latest = latest_by_user.get(stu["user_id"])
            records.append(
                {
                    "User ID": stu["user_id"],
                    "Student Name": stu["full_name"],
                    "Email": stu["email"],
                    "Role": stu["role"],
                    "Target Job Role": (
                        latest["job_role"]
                        if latest and latest.get("job_role")
                        else "Not available"
                    ),
                    "Prediction": (
                        latest["prediction"]
                        if latest and latest.get("prediction")
                        else "Not predicted yet"
                    ),
                    "Confidence (%)": (
                        latest["confidence"] if latest else None
                    ),
                    "Date & Time": (
                        latest["created_at"] if latest else None
                    ),
                }
            )

        columns = [
            "User ID",
            "Student Name",
            "Email",
            "Role",
            "Target Job Role",
            "Prediction",
            "Confidence (%)",
            "Date & Time",
        ]
        return pd.DataFrame(records, columns=columns)

    finally:
        cursor.close()
        connection.close()
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

def get_resume_for_sharing(resume_id, user_id):
    """
    Fetch a specific student's resume for authorized sharing.
    """

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT
                r.resume_id,
                r.user_id,
                u.full_name AS student_name,
                u.email AS student_email,
                r.file_name,
                r.file_path
            FROM resumes r
            JOIN users u
                ON r.user_id = u.user_id
            WHERE r.resume_id = %s
              AND r.user_id = %s
              AND u.role = 'student'
            LIMIT 1
        """

        cursor.execute(query, (resume_id, user_id))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ==========================================================
# NOTIFICATIONS
# ==========================================================

def create_notification(
    user_id,
    title,
    message,
    notification_type="general"
):
    """
    Create a notification for a student.
    """

    connection = create_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO notifications
    (
        user_id,
        title,
        message,
        notification_type
    )
    VALUES (%s, %s, %s, %s)
    """

    values = (
        user_id,
        title,
        message,
        notification_type
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_student_notifications(user_id):
    """
    Fetch notifications for a particular student.
    """

    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        notification_id,
        title,
        message,
        notification_type,
        is_read,
        created_at
    FROM notifications
    WHERE user_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(query, (int(user_id),))

    rows = cursor.fetchall()

    columns = [
        "Notification ID",
        "Title",
        "Message",
        "Type",
        "Is Read",
        "Created At"
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    cursor.close()
    connection.close()

    return df



# ==========================================================
# STUDENT PROFILE MANAGEMENT
# ==========================================================

STUDENT_PROFILE_FIELDS = [
    "phone",
    "alternate_phone",
    "date_of_birth",
    "gender",
    "address",
    "city",
    "state",
    "pincode",
    "university",
    "course",
    "branch",
    "graduation_year",
    "cgpa",
    "tenth_percentage",
    "twelfth_percentage",
    "active_backlogs",
    "internships",
    "projects",
    "technical_skills",
    "certifications",
    "preferred_job_role",
    "aptitude_score",
    "soft_skills_rating",
    "extracurricular_activities",
    "placement_training"
]


def save_student_profile(user_id, profile_data):
    """
    Create or update a student's profile.

    If the profile already exists, update it.
    Otherwise, create a new profile.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        columns = ", ".join(STUDENT_PROFILE_FIELDS)

        placeholders = ", ".join(
            ["%s"] * len(STUDENT_PROFILE_FIELDS)
        )

        update_query = ", ".join(
            f"{field} = VALUES({field})"
            for field in STUDENT_PROFILE_FIELDS
        )

        query = f"""
        INSERT INTO student_profiles
        (user_id, {columns})
        VALUES (%s, {placeholders})
        ON DUPLICATE KEY UPDATE
        {update_query}
        """

        values = [user_id]

        for field in STUDENT_PROFILE_FIELDS:
            value = profile_data.get(field)

            # Apply defaults for count fields
            if field in [
                "active_backlogs",
                "internships",
                "projects"
            ] and value is None:
                value = 0

            values.append(value)

        cursor.execute(query, tuple(values))
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()



def get_student_profile(user_id):
    """
    Fetch a student's profile using their user ID.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            u.user_id,
            u.full_name,
            u.email,
            p.*
        FROM users u
        LEFT JOIN student_profiles p
            ON u.user_id = p.user_id
        WHERE u.user_id = %s
          AND u.role = 'student'
        """

        cursor.execute(query, (user_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        profile = dict(zip(columns, row))

        return profile

    finally:
        cursor.close()
        connection.close()

def get_all_student_profiles():
    """
    Fetch all student accounts and their profile details
    for the Admin Student Records section.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            u.user_id AS `User ID`,
            u.full_name AS `Student Name`,
            u.email AS `Email`,
            p.phone AS `Phone Number`,
            p.alternate_phone AS `Alternate Phone`,
            p.city AS `City`,
            p.state AS `State`,
            p.university AS `University`,
            p.course AS `Course`,
            p.branch AS `Branch`,
            p.graduation_year AS `Graduation Year`,
            p.cgpa AS `CGPA`,
            p.tenth_percentage AS `10th Percentage`,
            p.twelfth_percentage AS `12th Percentage`,
            p.active_backlogs AS `Active Backlogs`,
            p.internships AS `Internships`,
            p.projects AS `Projects`,
            p.technical_skills AS `Technical Skills`,
            p.certifications AS `Certifications`,
            p.preferred_job_role AS `Preferred Job Role`,

            CASE
                WHEN p.profile_id IS NULL
                THEN 'Incomplete'
                ELSE 'Profile Created'
            END AS `Profile Status`

        FROM users u

        LEFT JOIN student_profiles p
            ON u.user_id = p.user_id

        WHERE u.role = 'student'

        ORDER BY u.full_name ASC
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        df = pd.DataFrame(rows, columns=columns)

        return df

    finally:
        cursor.close()
        connection.close()


# ==========================================================
# COMPANY MANAGEMENT
# ==========================================================

def add_company(company_data):
    """
    Add a new company to the database.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO companies (
            company_name,
            industry,
            website,
            location,
            contact_person,
            contact_email,
            contact_phone,
            company_description,
            created_by
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            company_data.get("company_name"),
            company_data.get("industry"),
            company_data.get("website"),
            company_data.get("location"),
            company_data.get("contact_person"),
            company_data.get("contact_email"),
            company_data.get("contact_phone"),
            company_data.get("company_description"),
            company_data.get("created_by")
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_all_companies():
    """
    Retrieve all companies.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            company_id,
            company_name,
            industry,
            website,
            location,
            contact_person,
            contact_email,
            contact_phone,
            company_description,
            company_status,
            created_at
        FROM companies
        ORDER BY created_at DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        return pd.DataFrame(rows, columns=columns)

    finally:
        cursor.close()
        connection.close()


def update_company(company_id, company_data):
    """
    Update existing company information.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        UPDATE companies
        SET
            company_name = %s,
            industry = %s,
            website = %s,
            location = %s,
            contact_person = %s,
            contact_email = %s,
            contact_phone = %s,
            company_description = %s,
            company_status = %s
        WHERE company_id = %s
        """

        values = (
            company_data.get("company_name"),
            company_data.get("industry"),
            company_data.get("website"),
            company_data.get("location"),
            company_data.get("contact_person"),
            company_data.get("contact_email"),
            company_data.get("contact_phone"),
            company_data.get("company_description"),
            company_data.get("company_status", "Active"),
            company_id
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# ==========================================================
# PLACEMENT DRIVE MANAGEMENT
# ==========================================================

def add_placement_drive(drive_data):
    """
    Create a placement drive and save its eligible branches.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO placement_drives (
            company_id,
            drive_name,
            job_role,
            job_description,
            job_location,
            employment_type,
            package_min_lpa,
            package_max_lpa,
            min_cgpa,
            min_tenth_percentage,
            min_twelfth_percentage,
            max_active_backlogs,
            min_internships,
            graduation_year,
            application_deadline,
            drive_date,
            drive_status,
            created_by
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        values = (
            drive_data["company_id"],
            drive_data["drive_name"],
            drive_data["job_role"],
            drive_data.get("job_description"),
            drive_data.get("job_location"),
            drive_data.get("employment_type"),
            drive_data.get("package_min_lpa"),
            drive_data.get("package_max_lpa"),
            drive_data.get("min_cgpa", 0),
            drive_data.get("min_tenth_percentage", 0),
            drive_data.get("min_twelfth_percentage", 0),
            drive_data.get("max_active_backlogs", 0),
            drive_data.get("min_internships", 0),
            drive_data.get("graduation_year"),
            drive_data.get("application_deadline"),
            drive_data.get("drive_date"),
            drive_data.get("drive_status", "Draft"),
            drive_data.get("created_by")
        )

        cursor.execute(query, values)

        drive_id = cursor.lastrowid

        branches = drive_data.get("branches", [])

        if branches:
            branch_query = """
            INSERT INTO drive_eligible_branches
            (drive_id, branch)
            VALUES (%s, %s)
            """

            branch_values = [
                (drive_id, branch)
                for branch in branches
            ]

            cursor.executemany(branch_query, branch_values)

        connection.commit()

        return drive_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_all_placement_drives():
    """
    Retrieve all placement drives with company names.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT
            d.drive_id,
            d.company_id,
            c.company_name,
            d.drive_name,
            d.job_role,
            d.job_description,
            d.job_location,
            d.employment_type,
            d.package_min_lpa,
            d.package_max_lpa,
            d.min_cgpa,
            d.min_tenth_percentage,
            d.min_twelfth_percentage,
            d.max_active_backlogs,
            d.min_internships,
            d.graduation_year,
            d.application_deadline,
            d.drive_date,
            d.drive_status,
            d.created_at
        FROM placement_drives d
        INNER JOIN companies c
            ON d.company_id = c.company_id
        ORDER BY d.created_at DESC
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [
            column[0]
            for column in cursor.description
        ]

        return pd.DataFrame(rows, columns=columns)

    finally:
        cursor.close()
        connection.close()


def get_drive_eligible_branches(drive_id):
    """
    Retrieve eligible branches for a particular drive.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        SELECT branch
        FROM drive_eligible_branches
        WHERE drive_id = %s
        ORDER BY branch
        """

        cursor.execute(query, (drive_id,))

        return [row[0] for row in cursor.fetchall()]

    finally:
        cursor.close()
        connection.close()


def update_placement_drive_status(drive_id, status):
    """
    Update the status of a placement drive.
    """

    allowed_statuses = [
        "Draft",
        "Open",
        "Closed",
        "Completed"
    ]

    if status not in allowed_statuses:
        raise ValueError("Invalid placement drive status.")

    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        UPDATE placement_drives
        SET drive_status = %s
        WHERE drive_id = %s
        """

        cursor.execute(query, (status, drive_id))
        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

# ==========================================================
# AUTOMATIC STUDENT ELIGIBILITY ENGINE
# ==========================================================

def get_drive_eligibility_results(drive_id):
    """
    Compare student profiles against a placement drive's
    eligibility criteria.

    Returns a DataFrame containing Eligible, Ineligible,
    and Incomplete Profile students with reasons.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get placement drive criteria
        cursor.execute("""
            SELECT
                drive_id,
                min_cgpa,
                min_tenth_percentage,
                min_twelfth_percentage,
                max_active_backlogs,
                min_internships,
                graduation_year
            FROM placement_drives
            WHERE drive_id = %s
        """, (drive_id,))

        drive = cursor.fetchone()

        if drive is None:
            raise ValueError("Placement drive not found.")

        criteria_columns = [
            column[0] for column in cursor.description
        ]
        criteria = dict(zip(criteria_columns, drive))

        # Get eligible branches
        cursor.execute("""
            SELECT branch
            FROM drive_eligible_branches
            WHERE drive_id = %s
        """, (drive_id,))

        eligible_branches = {
            row[0].strip().casefold()
            for row in cursor.fetchall()
            if row[0]
        }

        # Get registered student profiles
        cursor.execute("""
            SELECT
                u.user_id,
                u.full_name AS student_name,
                u.email,
                p.phone,
                p.branch,
                p.cgpa,
                p.tenth_percentage,
                p.twelfth_percentage,
                p.active_backlogs,
                p.internships,
                p.graduation_year
            FROM users u
            LEFT JOIN student_profiles p
                ON u.user_id = p.user_id
            WHERE u.role = 'student'
            ORDER BY u.full_name
        """)

        students = cursor.fetchall()
        student_columns = [
            column[0] for column in cursor.description
        ]

        results = []

        for student in students:

            student = dict(zip(student_columns, student))

            failures = []
            missing = []

            # Branch check
            branch = student["branch"]

            if not branch:
                missing.append("Branch information missing")

            elif branch.strip().casefold() not in eligible_branches:
                failures.append(
                    f"Branch {branch} is not eligible"
                )

            # CGPA check
            cgpa = student["cgpa"]
            min_cgpa = float(criteria["min_cgpa"] or 0)

            if min_cgpa > 0:
                if cgpa is None:
                    missing.append("CGPA missing")
                elif float(cgpa) < min_cgpa:
                    failures.append(
                        f"CGPA below {min_cgpa}"
                    )

            # 10th percentage check
            tenth = student["tenth_percentage"]
            min_tenth = float(
                criteria["min_tenth_percentage"] or 0
            )

            if min_tenth > 0:
                if tenth is None:
                    missing.append("10th percentage missing")
                elif float(tenth) < min_tenth:
                    failures.append(
                        f"10th marks below {min_tenth}%"
                    )

            # 12th percentage check
            twelfth = student["twelfth_percentage"]
            min_twelfth = float(
                criteria["min_twelfth_percentage"] or 0
            )

            if min_twelfth > 0:
                if twelfth is None:
                    missing.append("12th percentage missing")
                elif float(twelfth) < min_twelfth:
                    failures.append(
                        f"12th marks below {min_twelfth}%"
                    )

            # Active backlogs check
            backlogs = student["active_backlogs"]
            max_backlogs = criteria["max_active_backlogs"]

            if max_backlogs is not None:
                if backlogs is None:
                    missing.append("Active backlog information missing")
                elif int(backlogs) > int(max_backlogs):
                    failures.append(
                        f"Active backlogs exceed {max_backlogs}"
                    )

            # Internship check
            internships = student["internships"]
            min_internships = int(
                criteria["min_internships"] or 0
            )

            if min_internships > 0:
                if internships is None:
                    missing.append("Internship information missing")
                elif int(internships) < min_internships:
                    failures.append(
                        f"Internships below {min_internships}"
                    )

            # Graduation year check
            graduation_year = student["graduation_year"]
            required_year = criteria["graduation_year"]

            if required_year is not None:
                if graduation_year is None:
                    missing.append("Graduation year missing")
                elif int(graduation_year) != int(required_year):
                    failures.append(
                        f"Graduation year must be {required_year}"
                    )

            # Final eligibility decision
            if failures:
                status = "Ineligible"
            elif missing:
                status = "Incomplete Profile"
            else:
                status = "Eligible"

            reasons = failures + missing

            student["eligibility_status"] = status
            student["eligibility_reason"] = (
                "; ".join(reasons)
                if reasons else "Meets all eligibility criteria"
            )

            results.append(student)

        return pd.DataFrame(results)

    finally:
        cursor.close()
        connection.close()
def apply_for_placement(user_id, drive_id):
    """
    Allow a student to apply for a placement drive.
    A student can apply only once per drive.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO applications (user_id, drive_id)
            VALUES (%s, %s)
        """, (user_id, drive_id))

        connection.commit()
        return True, "Application submitted successfully."

    except Exception as e:
        connection.rollback()

        if "Duplicate entry" in str(e):
            return False, "You have already applied for this drive."

        return False, str(e)

    finally:
        cursor.close()
        connection.close()


def get_student_applications(user_id):
    """
    Fetch all placement applications submitted by a student.
    """

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.application_id,
                a.drive_id,
                a.application_status,
                a.applied_at,
                a.updated_at,
                d.drive_name,
                d.job_role,
                d.job_location,
                d.package_min_lpa,
                d.package_max_lpa,
                c.company_name
            FROM applications a
            JOIN placement_drives d
                ON a.drive_id = d.drive_id
            JOIN companies c
                ON d.company_id = c.company_id
            WHERE a.user_id = %s
            ORDER BY a.applied_at DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_drive_applications(drive_id):
    """
    Fetch all student applications for an admin-selected drive.
    """

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.application_id,
                a.user_id,
                u.full_name AS student_name,
                u.email,
                p.phone,
                p.branch,
                p.cgpa,
                a.application_status,
                a.applied_at
            FROM applications a
            JOIN users u
                ON a.user_id = u.user_id
            LEFT JOIN student_profiles p
                ON a.user_id = p.user_id
            WHERE a.drive_id = %s
            ORDER BY a.applied_at DESC
        """, (drive_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def update_application_status(application_id, new_status):
    """
    Update application status and notify the student.
    Both operations are completed in one transaction.
    """

    allowed_statuses = [
        "Applied",
        "Under Review",
        "Shortlisted",
        "Rejected",
        "Selected",
        "Withdrawn"
    ]

    if new_status not in allowed_statuses:
        return False, "Invalid application status."

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get application and student information
        cursor.execute("""
            SELECT
                a.user_id,
                a.application_status,
                d.drive_name
            FROM applications a
            JOIN placement_drives d
                ON a.drive_id = d.drive_id
            WHERE a.application_id = %s
        """, (application_id,))

        application = cursor.fetchone()

        if application is None:
            return False, "Application not found."

        old_status = application["application_status"]

        if old_status == new_status:
            return False, "Application already has this status."

        # Update application status
        cursor.execute("""
            UPDATE applications
            SET application_status = %s
            WHERE application_id = %s
        """, (new_status, application_id))

        # Create student notification
        title = "Application Status Updated"

        message = (
            f'Your application for '
            f'{application["drive_name"]} '
            f'is now {new_status}.'
        )

        cursor.execute("""
            INSERT INTO notifications (
                user_id,
                title,
                message,
                notification_type
            )
            VALUES (%s, %s, %s, %s)
        """, (
            application["user_id"],
            title,
            message,
            "application"
        ))

        connection.commit()

        return True, "Application status updated and student notified."

    except Exception as e:
        connection.rollback()
        return False, str(e)

    finally:
        cursor.close()
        connection.close()

def request_resume_sharing(resume_id, user_id, company_id, admin_id):
    """
    Create a request for student consent before sharing a resume.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Verify that the resume belongs to this student
        cursor.execute("""
            SELECT resume_id
            FROM resumes
            WHERE resume_id = %s AND user_id = %s
        """, (resume_id, user_id))

        if cursor.fetchone() is None:
            return False, "Resume does not belong to this student."

        cursor.execute("""
            INSERT INTO resume_shares
            (resume_id, user_id, company_id, requested_by)
            VALUES (%s, %s, %s, %s)
        """, (resume_id, user_id, company_id, admin_id))

        connection.commit()

        return True, "Resume sharing request sent for student consent."

    except Exception as e:
        connection.rollback()
        return False, str(e)

    finally:
        cursor.close()
        connection.close()


def get_student_resume_share_requests(user_id):
    """
    Get all resume sharing requests for a student.
    """

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                rs.share_id,
                rs.resume_id,
                r.file_name,
                c.company_name,
                rs.consent_status,
                rs.requested_at,
                rs.responded_at
            FROM resume_shares rs
            JOIN resumes r ON rs.resume_id = r.resume_id
            JOIN companies c ON rs.company_id = c.company_id
            WHERE rs.user_id = %s
            ORDER BY rs.requested_at DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def respond_to_resume_share(share_id, user_id, decision):
    """
    Allow the student to approve, reject, or revoke sharing.
    """

    allowed_decisions = ["Approved", "Rejected", "Revoked"]

    if decision not in allowed_decisions:
        return False, "Invalid consent decision."

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT share_id
            FROM resume_shares
            WHERE share_id = %s AND user_id = %s
        """, (share_id, user_id))

        if cursor.fetchone() is None:
            return False, "Sharing request not found."

        cursor.execute("""
            UPDATE resume_shares
            SET consent_status = %s,
                responded_at = CURRENT_TIMESTAMP
            WHERE share_id = %s AND user_id = %s
        """, (decision, share_id, user_id))

        connection.commit()

        return True, f"Resume sharing request {decision.lower()} successfully."

    except Exception as e:
        connection.rollback()
        return False, str(e)

    finally:
        cursor.close()
        connection.close()

def get_all_resume_share_requests():
    """
    Get all resume sharing requests for admin review.
    """

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                rs.share_id,
                rs.resume_id,
                rs.user_id,
                u.full_name AS student_name,
                u.email AS student_email,
                c.company_name,
                r.file_name,
                r.target_job_role,
                rs.consent_status,
                rs.requested_at,
                rs.responded_at,
                rs.shared_at
            FROM resume_shares rs
            JOIN users u ON rs.user_id = u.user_id
            JOIN companies c ON rs.company_id = c.company_id
            JOIN resumes r ON rs.resume_id = r.resume_id
            ORDER BY rs.requested_at DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
# ==========================================================
# PLACEMENT DRIVE EMAIL NOTIFICATION TRACKING
# ==========================================================

def get_notified_students_for_drive(drive_id):
    """
    Return a dict mapping user_id -> {sent_count, last_sent_at}
    for students who have already received an email for this drive.
    """
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT
            user_id,
            sent_count,
            last_sent_at
        FROM drive_email_notifications
        WHERE drive_id = %s
        """
        cursor.execute(query, (int(drive_id),))
        rows = cursor.fetchall()

        return {
            int(row["user_id"]): {
                "sent_count": int(row["sent_count"]),
                "last_sent_at": row["last_sent_at"],
            }
            for row in rows
        }

    finally:
        cursor.close()
        connection.close()


def log_drive_email_notification(drive_id, user_id, email_sent_to, sent_by=None):
    """
    Record that a placement drive email was sent to a student.
    Increments sent_count if intentionally resent.
    """
    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO drive_email_notifications
            (drive_id, user_id, email_sent_to, sent_by, sent_count)
        VALUES (%s, %s, %s, %s, 1)
        ON DUPLICATE KEY UPDATE
            email_sent_to = VALUES(email_sent_to),
            sent_by = VALUES(sent_by),
            sent_count = sent_count + 1,
            last_sent_at = CURRENT_TIMESTAMP
        """
        cursor.execute(
            query,
            (int(drive_id), int(user_id), email_sent_to, sent_by),
        )
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()