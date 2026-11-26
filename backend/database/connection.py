import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def _get_setting(key, default=""):
    """
    Read a config value from Streamlit Cloud secrets first,
    then fall back to environment variables / .env for local runs.
    """
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, default).strip()


def create_connection():
    host = _get_setting("DB_HOST", "localhost")
    port = int(_get_setting("DB_PORT", "3306"))
    user = _get_setting("DB_USER", "root")
    password = _get_setting("DB_PASSWORD", "")
    database = _get_setting("DB_NAME", "careerai_db")

    config = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
    }

    # Enable SSL automatically when connecting to TiDB Cloud (port 4000 or non-localhost)
    if host not in ("localhost", "127.0.0.1"):
        config["ssl_disabled"] = False

    return mysql.connector.connect(**config)