"""
Resume sharing / consent / dispatch operations for CareerAI.

One row per (student, drive) in `resume_shares`.

consent_status : Pending | Approved | Rejected | Revoked
consent_source : Admin Request | Student Application
sent_status    : Not Sent | Sent
"""

import pandas as pd

import backend.database.connection as _connection_module


def get_connection():
    """
    Find the function in connection.py that returns a MySQL connection.
    If yours has a different name, add it to the list below.
    """
    for name in (
        "get_connection",
        "get_db_connection",
        "connect_db",
        "create_connection",
        "connect_to_database",
        "connect",
        "get_db",
        "db_connection",
    ):
        function = getattr(_connection_module, name, None)
        if callable(function):
            return function()

    raise ImportError(
        "Could not find a connection function in backend/database/connection.py. "
        "Add its name to the list in resume_sharing.get_connection()."
    )


def _execute(query, params=(), fetch=False):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def init_resume_sharing_table():
    """Create the table if it does not exist (safe to call on every start)."""
    _execute(
        """
        CREATE TABLE IF NOT EXISTS resume_shares (
            share_id        INT AUTO_INCREMENT PRIMARY KEY,
            user_id         INT NOT NULL,
            drive_id        INT NOT NULL,
            consent_status  VARCHAR(20) NOT NULL DEFAULT 'Pending',
            consent_source  VARCHAR(30) NOT NULL DEFAULT 'Admin Request',
            requested_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            responded_at    DATETIME NULL,
            sent_status     VARCHAR(20) NOT NULL DEFAULT 'Not Sent',
            sent_at         DATETIME NULL,
            UNIQUE KEY uq_student_drive (user_id, drive_id)
        )
        """
    )


# ---------------------------------------------------------------
# Admin: request consent
# ---------------------------------------------------------------
def request_resume_share(user_id, drive_id):
    rows = _execute(
        "SELECT share_id, consent_status FROM resume_shares "
        "WHERE user_id=%s AND drive_id=%s",
        (user_id, drive_id),
        fetch=True,
    )

    if rows:
        status = rows[0]["consent_status"]
        if status in ("Pending", "Approved"):
            return False, f"Already {status.lower()}."
        _execute(
            "UPDATE resume_shares SET consent_status='Pending', "
            "consent_source='Admin Request', requested_at=NOW(), "
            "responded_at=NULL, sent_status='Not Sent', sent_at=NULL "
            "WHERE share_id=%s",
            (rows[0]["share_id"],),
        )
        return True, "Request sent again."

    _execute(
        "INSERT INTO resume_shares (user_id, drive_id) VALUES (%s, %s)",
        (user_id, drive_id),
    )
    return True, "Request created."


# ---------------------------------------------------------------
# Student: consent given while applying
# ---------------------------------------------------------------
def record_student_consent(user_id, drive_id):
    _execute(
        """
        INSERT INTO resume_shares
            (user_id, drive_id, consent_status, consent_source, responded_at)
        VALUES (%s, %s, 'Approved', 'Student Application', NOW())
        ON DUPLICATE KEY UPDATE
            consent_status = IF(sent_status = 'Sent', consent_status, 'Approved'),
            responded_at   = IF(sent_status = 'Sent', responded_at, NOW())
        """,
        (user_id, drive_id),
    )


# ---------------------------------------------------------------
# Student: respond to a request
# ---------------------------------------------------------------
def respond_to_share(share_id, user_id, new_status):
    if new_status not in ("Approved", "Rejected", "Revoked"):
        return False, "Invalid response."

    rows = _execute(
        "SELECT consent_status, sent_status FROM resume_shares "
        "WHERE share_id=%s AND user_id=%s",
        (share_id, user_id),
        fetch=True,
    )
    if not rows:
        return False, "Request not found."

    row = rows[0]
    if new_status == "Revoked" and row["sent_status"] == "Sent":
        return False, "This resume has already been sent and cannot be revoked."

    _execute(
        "UPDATE resume_shares SET consent_status=%s, responded_at=NOW() "
        "WHERE share_id=%s AND user_id=%s",
        (new_status, share_id, user_id),
    )
    return True, f"Response saved: {new_status}."


# ---------------------------------------------------------------
# Queries
# ---------------------------------------------------------------
def get_shares(drive_id=None, user_id=None):
    query = "SELECT * FROM resume_shares WHERE 1=1"
    params = []
    if drive_id is not None:
        query += " AND drive_id=%s"
        params.append(int(drive_id))
    if user_id is not None:
        query += " AND user_id=%s"
        params.append(int(user_id))
    query += " ORDER BY requested_at DESC"

    rows = _execute(query, tuple(params), fetch=True)
    return pd.DataFrame(rows)


def mark_shares_sent(share_ids):
    for share_id in share_ids:
        _execute(
            "UPDATE resume_shares SET sent_status='Sent', sent_at=NOW() "
            "WHERE share_id=%s AND consent_status='Approved'",
            (int(share_id),),
        )