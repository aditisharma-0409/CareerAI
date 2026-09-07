"""
CareerAI Authentication Module
"""

import bcrypt

from backend.database.connection import create_connection


# ==========================================
# Hash Password
# ==========================================

def hash_password(password):
    """
    Convert plain password into a secure hash.
    """

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


# ==========================================
# Verify Password
# ==========================================

def verify_password(password, password_hash):
    """
    Check whether entered password matches
    the stored password hash.
    """

    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hash_bytes
    )


# ==========================================
# Register Student
# ==========================================

def register_student(full_name, email, password):
    """
    Create a new student account.
    """

    connection = create_connection()

    if connection is None:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:

        # Check whether email already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return False, "An account with this email already exists."

        password_hash = hash_password(password)

        query = """
        INSERT INTO users
        (full_name, email, password_hash, role)
        VALUES (%s, %s, %s, 'student')
        """

        cursor.execute(
            query,
            (
                full_name,
                email,
                password_hash
            )
        )

        connection.commit()

        return True, "Student account created successfully."

    except Exception as error:

        connection.rollback()

        return False, str(error)

    finally:

        cursor.close()
        connection.close()


# ==========================================
# Login User
# ==========================================

def login_user(email, password):
    """
    Authenticate a student or TPO user.
    """

    connection = create_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        query = """
        SELECT
            user_id,
            full_name,
            email,
            password_hash,
            role
        FROM users
        WHERE email = %s
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        password_correct = verify_password(
            password,
            user["password_hash"]
        )

        if not password_correct:
            return None

        return {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }

    except Exception as error:

        print("Login Error:", error)

        return None

    finally:

        cursor.close()
        connection.close()