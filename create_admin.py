from backend.database.connection import create_connection
from backend.auth.authentication import hash_password


# ==========================================
# Admin Account Details
# ==========================================

full_name = "Admin"
email = "admin@careerai.com"

password = input("Enter Admin password: ")


# ==========================================
# Create Password Hash
# ==========================================

password_hash = hash_password(password)


# ==========================================
# Save Admin Account
# ==========================================

connection = create_connection()

if connection is None:
    print("❌ Database connection failed.")
    exit()

cursor = connection.cursor()

try:

    query = """
    INSERT INTO users
    (full_name, email, password_hash, role)
    VALUES (%s, %s, %s, 'admin')
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

    print("✅ Admin account created successfully.")

except Exception as error:

    connection.rollback()

    print("❌ Error creating Admin account:")
    print(error)

finally:

    cursor.close()
    connection.close()