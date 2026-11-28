# ==========================================================
# CareerAI - AI Powered Placement Management & Prediction Platform
# DAV University, Jalandhar
# Developed by: Aditi Sharma
# ==========================================================

import datetime
import os
import sys

import joblib
import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from resume.resume_parser import extract_resume_text
from resume.skill_extractor import extract_skills
from resume.recommendations import recommend_skills
from resume.learning_path import get_learning_path
from backend.email_service import (
    send_resumes_to_company,
    send_placement_drive_notifications,
)
from backend.database.operations import (
    save_prediction,
    get_prediction_history,
    save_resume,
    get_student_resumes,
    get_resume_by_user,
    get_student_records,
    create_notification,
    get_student_notifications,
    save_student_profile,
    get_student_profile,
    get_all_student_profiles,
    add_company,
    get_all_companies,
    update_company,
    add_placement_drive,
    get_all_placement_drives,
    get_drive_eligible_branches,
    update_placement_drive_status,
    get_drive_eligibility_results,
    apply_for_placement,
    get_student_applications,
    get_drive_applications,
    update_application_status,
    get_resume_for_sharing,
    get_notified_students_for_drive,
    log_drive_email_notification,
)
from backend.auth.authentication import (
    login_user,
    register_student,
)

# -----------------------------
# Session State Initialization
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"


# -----------------------------
# Streamlit Page Configuration
# -----------------------------

st.set_page_config(
    page_title="CareerAI | DAV University Placement Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>
        /* Hide Streamlit top header bar and Deploy button */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        .stAppDeployButton, [data-testid="stToolbar"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# MODERN EMERALD TEAL & SLATE APPLICATION THEME
# ==========================================================

st.markdown(
    """
<style>
:root {
    --teal-dark: #0B4F4A;
    --teal-primary: #0F766E;
    --teal-hover: #115E59;
    --teal-soft: #F0FDFA;
    --teal-border: #CCFBF1;
    --amber-soft: #FEF3C7;
    --amber-text: #B45309;
    --canvas: #F4F7F6;
    --surface: #FFFFFF;
    --border: #E2E8F0;
    --text-main: #0F172A;
    --text-muted: #64748B;
}

/* Hide default Streamlit sidebar */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Main canvas */
.stApp {
    background-color: var(--canvas);
    color: var(--text-main);
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 1.25rem;
    padding-bottom: 2.5rem;
    max-width: 1400px;
}

/* Floating Top App Bar */
.app-topbar {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

.app-topbar-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.app-logo-badge {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--teal-dark), var(--teal-primary));
    color: #FFFFFF !important;
    font-weight: 800;
    font-size: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 0.6px;
}

.app-brand-name {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-main) !important;
    margin: 0;
}

.app-brand-sub {
    font-size: 12px;
    color: var(--text-muted) !important;
    margin: 2px 0 0 0;
}

.app-user-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: #F8FAFC;
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 14px 6px 6px;
}

.app-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: var(--teal-soft);
    border: 1px solid var(--teal-border);
    color: var(--teal-primary) !important;
    font-weight: 700;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.app-user-name {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-main) !important;
    margin: 0;
    line-height: 1.2;
}

.app-user-role {
    font-size: 11px;
    color: var(--teal-primary) !important;
    font-weight: 600;
    margin: 0;
    line-height: 1.2;
}

/* Dashboard Hero Welcome Card */
.hero-card {
    background: linear-gradient(125deg, #0B4F4A 0%, #0F766E 65%, #14B8A6 100%);
    border-radius: 16px;
    padding: 26px 30px;
    color: #FFFFFF;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(15, 118, 110, 0.16);
}

.hero-kicker {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    background-color: rgba(255, 255, 255, 0.16);
    color: #FFFFFF !important;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF !important;
    margin: 0;
}

.hero-sub {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.88) !important;
    margin: 6px 0 0 0;
}

/* Custom Elevated KPI Cards */
.kpi-card {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    border-top: 3px solid var(--teal-primary);
    margin-bottom: 12px;
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin: 0 0 6px 0;
}

.kpi-value {
    font-size: 26px;
    font-weight: 750;
    color: var(--text-main);
    margin: 0;
    line-height: 1.2;
}

.kpi-sub {
    font-size: 12px;
    color: var(--teal-primary);
    font-weight: 500;
    margin: 6px 0 0 0;
}

/* Headings */
h1, h2, h3 {
    color: var(--text-main) !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

p, label {
    color: #475569;
}

/* Default Streamlit Metric (used on sub-pages) */
div[data-testid="stMetric"] {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--teal-primary);
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}

div[data-testid="stMetricLabel"] p {
    color: var(--text-muted) !important;
    font-size: 13px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: var(--text-main) !important;
    font-weight: 700;
}

/* Containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--surface);
    border-color: var(--border);
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

/* PRIMARY BUTTONS (Emerald Teal background, crisp WHITE text) */
.stButton > button[kind="primary"],
.stFormSubmitButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    min-height: 40px;
    font-weight: 600;
    font-size: 14px;
    border: 1px solid var(--teal-primary) !important;
    background-color: var(--teal-primary) !important;
    color: #FFFFFF !important;
    transition: all 0.15s ease;
}

.stButton > button[kind="primary"] *,
.stFormSubmitButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background-color: var(--teal-hover) !important;
    border-color: var(--teal-hover) !important;
    color: #FFFFFF !important;
}

/* SECONDARY BUTTONS (White background, crisp SLATE text) */
.stButton > button[kind="secondary"] {
    border-radius: 9px;
    min-height: 40px;
    font-weight: 500;
    font-size: 14px;
    border: 1px solid var(--border) !important;
    background-color: var(--surface) !important;
    color: var(--text-main) !important;
    transition: all 0.15s ease;
}

.stButton > button[kind="secondary"] * {
    color: var(--text-main) !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--teal-primary) !important;
    background-color: var(--teal-soft) !important;
    color: var(--teal-dark) !important;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 8px;
    border-color: #CBD5E1;
    background-color: #FFFFFF;
    color: var(--text-main);
}

/* DataFrames */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    background-color: #FFFFFF;
}

/* Dividers */
hr {
    border-color: var(--border);
}

/* Split-Screen Login Hero Panel */
.login-hero {
    background: linear-gradient(145deg, #0B4F4A 0%, #0F766E 60%, #115E59 100%);
    border-radius: 16px;
    padding: 40px 36px;
    color: #FFFFFF;
    box-shadow: 0 12px 30px rgba(11, 79, 74, 0.2);
}

.login-pill {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    background-color: rgba(255, 255, 255, 0.16);
    color: #FFFFFF !important;
    padding: 5px 12px;
    border-radius: 20px;
    margin-bottom: 18px;
}

.login-hero-title {
    font-size: 30px;
    font-weight: 750;
    color: #FFFFFF !important;
    line-height: 1.2;
    margin: 0 0 12px 0;
}

.login-hero-desc {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.88) !important;
    line-height: 1.6;
    margin-bottom: 24px;
}

.login-feature-item {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    font-size: 13px;
    color: #FFFFFF !important;
}

/* Drive Opportunity Cards */
.drive-card {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--teal-primary);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.drive-card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 6px;
}

.drive-company {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--teal-primary);
    margin: 0;
}

.drive-role {
    font-size: 17px;
    font-weight: 700;
    color: var(--text-main);
    margin: 2px 0 6px 0;
}

.pkg-badge {
    background-color: var(--teal-soft);
    color: var(--teal-dark);
    border: 1px solid var(--teal-border);
    font-size: 12px;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 20px;
    white-space: nowrap;
}

.drive-meta {
    font-size: 13px;
    color: var(--text-muted);
    margin: 0;
}

/* Notification Cards */
.notif-card {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--teal-primary);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}

.notif-card.type-important,
.notif-card.type-interview { border-left-color: #D97706; }

.notif-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.notif-pill {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    padding: 2px 9px;
    border-radius: 12px;
    background-color: var(--teal-soft);
    color: var(--teal-dark);
}

.notif-time {
    font-size: 11px;
    color: #94A3B8;
}

.notif-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-main);
    margin: 0 0 4px 0;
}

.notif-msg {
    font-size: 13px;
    color: #475569;
    margin: 0;
    line-height: 1.45;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Load Machine Learning Model
# -----------------------------

MODEL_PATH = os.path.join("saved_models", "careerai_model.pkl")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.error("Trained placement prediction model not found at saved_models/careerai_model.pkl.")
    st.stop()


# ==========================================================
# LOGIN / REGISTRATION PAGE (MODERN SPLIT-SCREEN SAAS)
# ==========================================================

if not st.session_state.logged_in:

    st.write("")
    spacer_l, col_hero, col_form, spacer_r = st.columns([0.3, 1.15, 1.05, 0.3], gap="large")

    with col_hero:
        st.markdown(
            """
            <div class="login-hero">
                <span class="login-pill">DAV University, Jalandhar</span>
                <div class="login-hero-title">CareerAI Placement Management Portal</div>
                <div class="login-hero-desc">
                    An intelligent campus recruitment platform connecting students, the Training &amp;
                    Placement Cell, and recruiting HR teams in one unified workspace.
                </div>
                <div class="login-feature-item">
                    <strong>AI Placement Readiness:</strong> Predict placement probability and identify missing resume skills.
                </div>
                <div class="login-feature-item">
                    <strong>Smart Eligibility Engine:</strong> Automatically match student profiles with company drive criteria.
                </div>
                <div class="login-feature-item">
                    <strong>Direct HR &amp; Student Alerts:</strong> Email official drive announcements and share PDF resumes directly.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_form:
        if st.session_state.show_registration:
            with st.container(border=True):
                st.markdown("### Create Student Account")
                st.caption("Register with your university email to access placement drives and career tools.")

                full_name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email Address", placeholder="Enter your email address")
                password = st.text_input("Password", type="password", placeholder="Create a password (min. 6 characters)")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

                st.write("")
                register_button = st.button("Create Account", type="primary", use_container_width=True)

                if register_button:
                    if (
                        full_name.strip() == ""
                        or email.strip() == ""
                        or password.strip() == ""
                        or confirm_password.strip() == ""
                    ):
                        st.warning("Please fill in all fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must contain at least 6 characters.")
                    else:
                        success, message = register_student(full_name.strip(), email.strip(), password)
                        if success:
                            st.success("Account created successfully. You can now sign in.")
                            st.session_state.show_registration = False
                        else:
                            st.error(message)

                st.divider()
                if st.button("Back to Sign In", type="secondary", use_container_width=True):
                    st.session_state.show_registration = False
                    st.rerun()
        else:
            with st.container(border=True):
                st.markdown("### Sign In to CareerAI")
                st.caption("Access your Student or Placement Admin dashboard.")

                email = st.text_input("Email Address", placeholder="Enter your registered email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")

                st.write("")
                login_button = st.button("Sign In", type="primary", use_container_width=True)

                if login_button:
                    if email.strip() == "" or password.strip() == "":
                        st.warning("Please enter both email and password.")
                    else:
                        user = login_user(email.strip(), password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.active_page = "Dashboard"
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")

                with st.expander("Forgot Password?"):
                    reset_email = st.text_input(
                        "Enter your registered email",
                        placeholder="student@davuniversity.org",
                        key="forgot_password_email",
                    )
                    if st.button("Request Password Reset", type="secondary", use_container_width=True):
                        if not reset_email.strip() or "@" not in reset_email:
                            st.warning("Please enter a valid registered email address.")
                        else:
                            st.info(
                                "Password reset assistance is handled by the DAV University "
                                "Training & Placement Cell. Please contact the Placement Admin "
                                f"with your registered email ({reset_email.strip()})."
                            )

                st.divider()
                if st.button("Create Student Account", type="secondary", use_container_width=True):
                    st.session_state.show_registration = True
                    st.rerun()

    st.stop()


# ==========================================================
# FLOATING TOP BAR & HORIZONTAL NAVIGATION
# ==========================================================

user = st.session_state.user
user_role = user["role"]
user_name = user["full_name"]
role_label = "Placement Admin" if user_role == "admin" else "Student Portal"
initials = "".join([part[0].upper() for part in user_name.split()[:2]]) or "U"

st.markdown(
    f"""
    <div class="app-topbar">
        <div class="app-topbar-left">
            <div class="app-logo-badge">CA</div>
            <div>
                <p class="app-brand-name">CareerAI — DAV University, Jalandhar</p>
                <p class="app-brand-sub">Training &amp; Placement Management Portal</p>
            </div>
        </div>
        <div class="app-user-chip">
            <div class="app-avatar">{initials}</div>
            <div>
                <p class="app-user-name">{user_name}</p>
                <p class="app-user-role">{role_label}</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if user_role == "student":
    nav_items = [
        "Dashboard",
        "My Profile",
        "Placement Readiness",
        "Placement Drives",
        "My Applications",
        "Notifications",
    ]
else:
    nav_items = [
        "Dashboard",
        "Companies",
        "Placement Drives",
        "Eligibility & HR Sharing",
        "Applications",
        "Resume Analysis",
        "Notifications",
    ]

if st.session_state.active_page not in nav_items:
    st.session_state.active_page = "Dashboard"

nav_cols = st.columns(len(nav_items) + 1)
for idx, item in enumerate(nav_items):
    is_active = st.session_state.active_page == item
    if nav_cols[idx].button(
        item,
        key=f"nav_{user_role}_{item}",
        type="primary" if is_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.active_page = item
        st.rerun()

if nav_cols[-1].button("Sign Out", key="top_sign_out", type="secondary", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.show_registration = False
    st.session_state.active_page = "Dashboard"
    st.rerun()

st.markdown("<hr style='margin-top: 8px; margin-bottom: 20px;'>", unsafe_allow_html=True)

menu = st.session_state.active_page


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

if menu == "Dashboard" and user_role == "admin":

    students_df = get_all_student_profiles()
    companies_df = get_all_companies()
    drives_df = get_all_placement_drives()
    resumes_df = get_student_resumes()

    total_students = len(students_df)
    total_companies = len(companies_df)
    active_drives_df = (
        drives_df[drives_df["drive_status"] == "Open"].copy()
        if not drives_df.empty
        else pd.DataFrame()
    )
    active_drives_count = len(active_drives_df)
    uploaded_resumes_count = len(resumes_df)

    total_applications = 0
    shortlisted_or_selected = 0
    if not drives_df.empty:
        for drive_id in drives_df["drive_id"].tolist():
            apps = get_drive_applications(int(drive_id))
            total_applications += len(apps)
            shortlisted_or_selected += sum(
                1 for a in apps if a["application_status"] in ("Shortlisted", "Selected")
            )

    st.markdown(
        f"""
        <div class="hero-card">
            <span class="hero-kicker">Training &amp; Placement Cell — Admin Workspace</span>
            <div class="hero-title">Welcome, {user_name}</div>
            <div class="hero-sub">
                Currently managing <strong>{active_drives_count} active placement drive(s)</strong> across
                <strong>{total_companies} registered companies</strong> and <strong>{total_students} students</strong>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Registered Students</p>
                <p class="kpi-value">{total_students}</p>
                <p class="kpi-sub">Active student accounts</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Recruiting Companies</p>
                <p class="kpi-value">{total_companies}</p>
                <p class="kpi-sub">Partner organizations</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Active Placement Drives</p>
                <p class="kpi-value">{active_drives_count}</p>
                <p class="kpi-sub">Currently open for applications</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    k4, k5, k6 = st.columns(3)
    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Total Applications</p>
                <p class="kpi-value">{total_applications}</p>
                <p class="kpi-sub">Across all drives</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Shortlisted / Selected</p>
                <p class="kpi-value">{shortlisted_or_selected}</p>
                <p class="kpi-sub">Progressed candidates</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k6:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Uploaded Resumes</p>
                <p class="kpi-value">{uploaded_resumes_count}</p>
                <p class="kpi-sub">Analyzed &amp; ready for HR</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Active & Upcoming Placement Drives")

    if drives_df.empty:
        st.info("No placement drives have been created yet. Use Placement Drives above to add one.")
    else:
        display_drives = drives_df[
            [
                "company_name",
                "drive_name",
                "job_role",
                "job_location",
                "package_min_lpa",
                "package_max_lpa",
                "application_deadline",
                "drive_status",
            ]
        ].rename(
            columns={
                "company_name": "Company",
                "drive_name": "Drive Name",
                "job_role": "Job Role",
                "job_location": "Location",
                "package_min_lpa": "Min LPA",
                "package_max_lpa": "Max LPA",
                "application_deadline": "Deadline",
                "drive_status": "Status",
            }
        )
        st.dataframe(display_drives, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Quick Admin Actions")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("#### Company & Drive Setup")
            st.write("Register recruiting companies, store HR contacts, and configure drive-specific eligibility criteria.")
            if st.button("Manage Placement Drives", type="secondary", use_container_width=True):
                st.session_state.active_page = "Placement Drives"
                st.rerun()
    with c2:
        with st.container(border=True):
            st.markdown("#### Eligibility & HR Sharing")
            st.write("Filter eligible students automatically and share selected PDF resumes directly with company HR.")
            if st.button("Open Eligibility Engine", type="secondary", use_container_width=True):
                st.session_state.active_page = "Eligibility & HR Sharing"
                st.rerun()
    with c3:
        with st.container(border=True):
            st.markdown("#### Student Email Alerts")
            st.write("Send official DAV University placement drive announcements to eligible students' emails.")
            if st.button("Send Placement Alerts", type="primary", use_container_width=True):
                st.session_state.active_page = "Notifications"
                st.rerun()


# ==========================================================
# COMPANY MANAGEMENT (ADMIN)
# ==========================================================

elif menu == "Companies" and user_role == "admin":

    st.title("Company Management")
    st.caption("Maintain recruiting company records and HR contact details.")

    companies_df = get_all_companies()

    total_companies = len(companies_df)
    active_companies = (
        len(companies_df[companies_df["company_status"] == "Active"])
        if not companies_df.empty
        else 0
    )
    inactive_companies = total_companies - active_companies

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Companies", total_companies)
    col2.metric("Active Companies", active_companies)
    col3.metric("Inactive Companies", inactive_companies)

    st.divider()
    st.subheader("Add New Company")

    with st.form("add_company_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company Name *")
            industry = st.text_input("Industry")
            website = st.text_input("Company Website")
            location = st.text_input("Job Location")

        with col2:
            contact_person = st.text_input("HR Contact Person")
            contact_email = st.text_input("HR Contact Email")
            contact_phone = st.text_input("HR Contact Phone")

        company_description = st.text_area(
            "Company Description",
            placeholder="Enter a short description of the company...",
        )

        add_button = st.form_submit_button("Save Company", use_container_width=True)

        if add_button:
            if not company_name.strip():
                st.error("Company Name is required.")
            elif contact_email and "@" not in contact_email:
                st.error("Please enter a valid contact email.")
            else:
                company_data = {
                    "company_name": company_name.strip(),
                    "industry": industry.strip(),
                    "website": website.strip(),
                    "location": location.strip(),
                    "contact_person": contact_person.strip(),
                    "contact_email": contact_email.strip(),
                    "contact_phone": contact_phone.strip(),
                    "company_description": company_description.strip(),
                    "created_by": st.session_state.user["user_id"],
                }

                try:
                    company_id = add_company(company_data)
                    st.success(f"Company added successfully (ID: {company_id}).")
                    st.rerun()
                except Exception as e:
                    st.error(f"Unable to add company: {e}")

    st.divider()
    st.subheader("Registered Companies")

    if companies_df.empty:
        st.info("No companies have been added yet.")
    else:
        search_company = st.text_input(
            "Search Company",
            placeholder="Search by company name or industry...",
        )

        filtered_companies = companies_df.copy()

        if search_company:
            mask = (
                filtered_companies["company_name"].fillna("").str.contains(search_company, case=False)
                | filtered_companies["industry"].fillna("").str.contains(search_company, case=False)
            )
            filtered_companies = filtered_companies[mask]

        display_columns = [
            "company_id",
            "company_name",
            "industry",
            "location",
            "contact_email",
            "contact_phone",
            "company_status",
        ]

        st.dataframe(
            filtered_companies[display_columns],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.subheader("Edit Company Details")

    if companies_df.empty:
        st.info("Add a company first to edit its details.")
    else:
        def company_value(value):
            if pd.isna(value):
                return ""
            return str(value)

        company_options = {
            int(row["company_id"]): f'{row["company_name"]} (ID: {row["company_id"]})'
            for _, row in companies_df.iterrows()
        }

        selected_company_id = st.selectbox(
            "Select Company",
            options=list(company_options.keys()),
            format_func=lambda x: company_options[x],
        )

        selected_company = companies_df[
            companies_df["company_id"] == selected_company_id
        ].iloc[0]

        with st.form("edit_company_form"):
            col1, col2 = st.columns(2)

            with col1:
                edit_name = st.text_input("Company Name *", value=company_value(selected_company["company_name"]))
                edit_industry = st.text_input("Industry", value=company_value(selected_company["industry"]))
                edit_website = st.text_input("Website", value=company_value(selected_company["website"]))
                edit_location = st.text_input("Location", value=company_value(selected_company["location"]))

            with col2:
                edit_contact_person = st.text_input("HR Contact Person", value=company_value(selected_company["contact_person"]))
                edit_contact_email = st.text_input("HR Contact Email", value=company_value(selected_company["contact_email"]))
                edit_contact_phone = st.text_input("HR Contact Phone", value=company_value(selected_company["contact_phone"]))
                current_status = company_value(selected_company["company_status"])
                edit_status = st.selectbox(
                    "Company Status",
                    ["Active", "Inactive"],
                    index=0 if current_status == "Active" else 1,
                )

            edit_description = st.text_area(
                "Company Description",
                value=company_value(selected_company["company_description"]),
            )

            update_button = st.form_submit_button("Update Company", use_container_width=True)

            if update_button:
                if not edit_name.strip():
                    st.error("Company Name is required.")
                elif edit_contact_email and "@" not in edit_contact_email:
                    st.error("Please enter a valid contact email.")
                else:
                    updated_data = {
                        "company_name": edit_name.strip(),
                        "industry": edit_industry.strip(),
                        "website": edit_website.strip(),
                        "location": edit_location.strip(),
                        "contact_person": edit_contact_person.strip(),
                        "contact_email": edit_contact_email.strip(),
                        "contact_phone": edit_contact_phone.strip(),
                        "company_description": edit_description.strip(),
                        "company_status": edit_status,
                    }

                    try:
                        update_company(selected_company_id, updated_data)
                        st.success("Company updated successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Unable to update company: {e}")


# ==========================================================
# PLACEMENT DRIVE MANAGEMENT (ADMIN)
# ==========================================================

elif menu == "Placement Drives" and user_role == "admin":

    st.title("Placement Drive Management")
    st.caption("Create and manage company recruitment drives and eligibility rules.")

    companies_df = get_all_companies()

    if companies_df.empty:
        st.warning("No companies are registered yet. Please add a company first.")
    else:
        active_companies = companies_df[companies_df["company_status"] == "Active"].copy()

        if active_companies.empty:
            st.warning("There are no active companies. Activate a company before creating a drive.")
        else:
            company_options = {
                int(row["company_id"]): row["company_name"]
                for _, row in active_companies.iterrows()
            }

            st.subheader("Create New Placement Drive")

            with st.form("create_placement_drive_form"):
                selected_company_id = st.selectbox(
                    "Select Company *",
                    options=list(company_options.keys()),
                    format_func=lambda x: company_options[x],
                )

                drive_name = st.text_input(
                    "Drive Name *",
                    placeholder="Example: Graduate Recruitment 2027",
                )

                col1, col2 = st.columns(2)

                with col1:
                    job_role = st.text_input("Job Role *", placeholder="Example: Data Analyst")
                    job_location = st.text_input("Job Location", placeholder="Example: Mohali")
                    employment_type = st.selectbox(
                        "Employment Type",
                        ["Full-time", "Internship", "Contract", "Other"],
                    )

                with col2:
                    package_min = st.number_input("Minimum Package (LPA)", min_value=0.0, value=0.0, step=0.5)
                    package_max = st.number_input("Maximum Package (LPA)", min_value=0.0, value=0.0, step=0.5)
                    graduation_year = st.number_input(
                        "Eligible Graduation Year",
                        min_value=2020,
                        max_value=2100,
                        value=2027,
                        step=1,
                    )

                job_description = st.text_area(
                    "Job Description",
                    placeholder="Describe the responsibilities and job requirements...",
                )

                st.divider()
                st.subheader("Eligibility Criteria")

                col1, col2 = st.columns(2)

                with col1:
                    min_cgpa = st.number_input("Minimum CGPA", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
                    min_tenth = st.number_input("Minimum 10th Percentage", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
                    min_twelfth = st.number_input("Minimum 12th Percentage", min_value=0.0, max_value=100.0, value=0.0, step=1.0)

                with col2:
                    max_backlogs = st.number_input("Maximum Active Backlogs", min_value=0, value=0, step=1)
                    min_internships = st.number_input("Minimum Internships", min_value=0, value=0, step=1)
                    drive_status = st.selectbox("Initial Drive Status", ["Draft", "Open"])

                eligible_branches = st.multiselect(
                    "Eligible Branches *",
                    [
                        "CSE",
                        "CSE-AI",
                        "Computer Science",
                        "Information Technology",
                        "IT",
                        "ECE",
                        "EEE",
                        "Mechanical",
                        "Civil",
                        "BCA",
                        "MCA",
                        "Other",
                    ],
                    placeholder="Select one or more branches",
                )

                st.divider()
                st.subheader("Important Dates")

                col1, col2 = st.columns(2)
                with col1:
                    application_deadline = st.date_input("Application Deadline", value=None)
                with col2:
                    drive_date = st.date_input("Placement Drive Date", value=None)

                submit_drive = st.form_submit_button("Create Placement Drive", use_container_width=True)

                if submit_drive:
                    if not drive_name.strip():
                        st.error("Drive name is required.")
                    elif not job_role.strip():
                        st.error("Job role is required.")
                    elif not eligible_branches:
                        st.error("Please select at least one eligible branch.")
                    elif package_max > 0 and package_min > package_max:
                        st.error("Maximum package cannot be lower than minimum package.")
                    elif (
                        application_deadline is not None
                        and drive_date is not None
                        and application_deadline > drive_date
                    ):
                        st.error("Application deadline cannot be after the drive date.")
                    else:
                        drive_data = {
                            "company_id": selected_company_id,
                            "drive_name": drive_name.strip(),
                            "job_role": job_role.strip(),
                            "job_description": job_description.strip(),
                            "job_location": job_location.strip(),
                            "employment_type": employment_type,
                            "package_min_lpa": package_min,
                            "package_max_lpa": package_max,
                            "min_cgpa": min_cgpa,
                            "min_tenth_percentage": min_tenth,
                            "min_twelfth_percentage": min_twelfth,
                            "max_active_backlogs": max_backlogs,
                            "min_internships": min_internships,
                            "graduation_year": graduation_year,
                            "application_deadline": application_deadline,
                            "drive_date": drive_date,
                            "drive_status": drive_status,
                            "branches": eligible_branches,
                            "created_by": st.session_state.user["user_id"],
                        }

                        try:
                            drive_id = add_placement_drive(drive_data)
                            st.success(f"Placement drive created successfully (Drive ID: {drive_id}).")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Unable to create placement drive: {e}")

    st.divider()
    st.subheader("Registered Placement Drives")

    drives_df = get_all_placement_drives()

    if drives_df.empty:
        st.info("No placement drives have been created yet.")
    else:
        st.dataframe(
            drives_df[
                [
                    "drive_id",
                    "company_name",
                    "drive_name",
                    "job_role",
                    "job_location",
                    "package_min_lpa",
                    "package_max_lpa",
                    "graduation_year",
                    "drive_status",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Drive Eligibility & Status")

        drive_options = {
            int(row["drive_id"]): f'{row["drive_name"]} - {row["company_name"]}'
            for _, row in drives_df.iterrows()
        }

        selected_drive_id = st.selectbox(
            "Select Drive",
            options=list(drive_options.keys()),
            format_func=lambda x: drive_options[x],
            key="view_drive_eligibility",
        )

        selected_branches = get_drive_eligible_branches(selected_drive_id)
        st.write("**Eligible Branches:**", ", ".join(selected_branches) if selected_branches else "None")

        selected_drive = drives_df[drives_df["drive_id"] == selected_drive_id].iloc[0]
        status_options = ["Draft", "Open", "Closed", "Completed"]
        current_status = selected_drive["drive_status"]

        new_status = st.selectbox(
            "Drive Status",
            status_options,
            index=status_options.index(current_status) if current_status in status_options else 0,
            key="update_drive_status",
        )

        if st.button("Update Drive Status", type="primary"):
            try:
                update_placement_drive_status(selected_drive_id, new_status)
                st.success("Drive status updated successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"Unable to update drive status: {e}")


# ==========================================================
# STUDENT ELIGIBILITY & HR RESUME SHARING (ADMIN)
# ==========================================================

elif menu == "Eligibility & HR Sharing" and user_role == "admin":

    st.title("Student Eligibility & HR Resume Sharing")
    st.caption("Evaluate student eligibility per placement drive and share selected PDF resumes with company HR.")
    st.divider()

    drives_df = get_all_placement_drives()

    if drives_df.empty:
        st.info("No placement drives are available. Please create a placement drive first.")
    else:
        drive_options = {
            int(row["drive_id"]): f'{row["company_name"]} - {row["drive_name"]}'
            for _, row in drives_df.iterrows()
        }

        selected_drive_id = st.selectbox(
            "Select Placement Drive",
            options=list(drive_options.keys()),
            format_func=lambda x: drive_options[x],
            key="eligibility_drive_selection",
        )

        st.divider()

        try:
            results_df = get_drive_eligibility_results(selected_drive_id)

            if results_df.empty:
                st.info("No registered student records found.")
            else:
                eligible_count = (results_df["eligibility_status"] == "Eligible").sum()
                ineligible_count = (results_df["eligibility_status"] == "Ineligible").sum()
                incomplete_count = (results_df["eligibility_status"] == "Incomplete Profile").sum()

                st.subheader("Eligibility Overview")

                col1, col2, col3 = st.columns(3)
                col1.metric("Eligible Students", int(eligible_count))
                col2.metric("Ineligible Students", int(ineligible_count))
                col3.metric("Incomplete Profiles", int(incomplete_count))

                st.divider()
                st.subheader("Student Eligibility Results")

                status_filter = st.selectbox(
                    "Filter by Eligibility Status",
                    ["All", "Eligible", "Ineligible", "Incomplete Profile"],
                    key="eligibility_status_filter",
                )

                filtered_df = results_df.copy()
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df["eligibility_status"] == status_filter]

                display_columns = [
                    "student_name",
                    "email",
                    "branch",
                    "cgpa",
                    "eligibility_status",
                    "eligibility_reason",
                ]

                st.dataframe(filtered_df[display_columns], use_container_width=True, hide_index=True)

                st.divider()
                st.subheader("Eligible Student Details")

                eligible_students = results_df[results_df["eligibility_status"] == "Eligible"].copy()

                if eligible_students.empty:
                    st.warning("No eligible students found for this drive.")
                else:
                    st.success(f"{len(eligible_students)} student(s) meet the placement criteria.")
                    st.dataframe(
                        eligible_students[
                            ["student_name", "email", "phone", "branch", "cgpa", "graduation_year"]
                        ],
                        use_container_width=True,
                        hide_index=True,
                    )

                st.divider()
                st.subheader("Eligible Students' Resumes")

                selected_resume_ids = []
                latest_resumes = pd.DataFrame()

                if eligible_students.empty:
                    st.info("There are no eligible students for this drive, so resume sharing is unavailable.")
                else:
                    resumes_df = get_student_resumes()

                    if resumes_df.empty:
                        st.warning("No student resumes have been uploaded.")
                    else:
                        eligible_user_ids = eligible_students["user_id"].astype(int).tolist()
                        matching_resumes = resumes_df[resumes_df["User ID"].isin(eligible_user_ids)].copy()

                        if matching_resumes.empty:
                            st.warning("None of the eligible students has uploaded a resume.")
                        else:
                            latest_resumes = (
                                matching_resumes
                                .sort_values("Uploaded At", ascending=False)
                                .drop_duplicates(subset=["User ID"], keep="first")
                            )
                            st.dataframe(
                                latest_resumes[
                                    [
                                        "User ID",
                                        "Student Name",
                                        "Email",
                                        "File Name",
                                        "Target Job Role",
                                        "Resume Score",
                                        "Uploaded At",
                                    ]
                                ],
                                use_container_width=True,
                                hide_index=True,
                            )

                            resume_options = {
                                (
                                    f'{row["Student Name"]} | '
                                    f'{row["File Name"]} | '
                                    f'Resume ID: {int(row["Resume ID"])}'
                                ): int(row["Resume ID"])
                                for _, row in latest_resumes.iterrows()
                            }

                            selected_resume_labels = st.multiselect(
                                "Select students whose resumes you want to share",
                                options=list(resume_options.keys()),
                                key=f"selected_resumes_{selected_drive_id}",
                            )
                            selected_resume_ids = [resume_options[label] for label in selected_resume_labels]

                            if selected_resume_ids:
                                st.success(f"{len(selected_resume_ids)} resume(s) selected.")

                st.caption(
                    "Eligibility is determined using the information available "
                    "in student profiles and the criteria configured for this drive."
                )

                st.divider()
                st.subheader("Send Selected Resumes to Company HR")

                hr_email = st.text_input(
                    "Company HR Email Address",
                    placeholder="hr@company.com",
                    key=f"hr_email_{selected_drive_id}",
                )

                if st.button("Send Selected Resumes", type="primary", key=f"send_resumes_{selected_drive_id}"):
                    if not selected_resume_ids:
                        st.warning("Please select at least one student resume.")
                    elif not hr_email.strip():
                        st.warning("Please enter the company HR email address.")
                    else:
                        resume_files = []
                        missing_resume_ids = []

                        for resume_id in selected_resume_ids:
                            selected_rows = latest_resumes[
                                latest_resumes["Resume ID"].astype(int) == int(resume_id)
                            ]
                            if selected_rows.empty:
                                missing_resume_ids.append(resume_id)
                                continue

                            selected_row = selected_rows.iloc[0]
                            resume = get_resume_for_sharing(int(resume_id), int(selected_row["User ID"]))
                            if resume:
                                resume_files.append(resume)
                            else:
                                missing_resume_ids.append(resume_id)

                        if missing_resume_ids:
                            st.error(
                                "Some selected resume records could not be found. "
                                "Please refresh the page and select the resumes again."
                            )
                        elif len(resume_files) != len(selected_resume_ids):
                            st.error("The selected resume list could not be verified. No email was sent.")
                        else:
                            success, message = send_resumes_to_company(hr_email.strip(), resume_files)
                            if success:
                                st.success(message)
                                st.write("**Email Delivery Summary**")
                                st.write("Recipient:", hr_email.strip())
                                st.write("Total resumes sent:", len(resume_files))
                                st.write("**Attached Student Resumes:**")
                                for resume in resume_files:
                                    st.write(f"- {resume['student_name']} ({resume['file_name']})")
                            else:
                                st.error(message)

        except Exception as e:
            st.error(f"Unable to calculate student eligibility: {e}")


# ==========================================================
# APPLICATION MANAGEMENT (ADMIN)
# ==========================================================

elif menu == "Applications" and user_role == "admin":

    st.title("Application Management")
    st.caption("Review student applications and update recruitment status.")
    st.divider()

    drives_df = get_all_placement_drives()

    if drives_df.empty:
        st.info("No placement drives have been created yet.")
    else:
        drive_options = {
            int(row["drive_id"]): f'{row["company_name"]} - {row["drive_name"]}'
            for _, row in drives_df.iterrows()
        }

        selected_drive_id = st.selectbox(
            "Select Placement Drive",
            options=list(drive_options.keys()),
            format_func=lambda x: drive_options[x],
            key="admin_application_drive",
        )

        st.divider()
        st.subheader("Applications Received")

        applications = get_drive_applications(selected_drive_id)

        if not applications:
            st.info("No students have applied for this placement drive yet.")
        else:
            total = len(applications)
            shortlisted = sum(1 for app in applications if app["application_status"] == "Shortlisted")
            selected = sum(1 for app in applications if app["application_status"] == "Selected")
            rejected = sum(1 for app in applications if app["application_status"] == "Rejected")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Applicants", total)
            col2.metric("Shortlisted", shortlisted)
            col3.metric("Selected", selected)
            col4.metric("Rejected", rejected)

            st.divider()
            st.subheader("Student Applicants")

            applications_df = pd.DataFrame(applications)
            st.dataframe(applications_df, hide_index=True, use_container_width=True)

            st.divider()
            st.subheader("Update Application Status")

            application_options = {
                int(app["application_id"]): (
                    f'{app["student_name"]} | {app["email"]} | {app["application_status"]}'
                )
                for app in applications
            }

            selected_application_id = st.selectbox(
                "Select Student Application",
                options=list(application_options.keys()),
                format_func=lambda x: application_options[x],
                key="admin_selected_application",
            )

            selected_application = next(
                app for app in applications if int(app["application_id"]) == selected_application_id
            )

            st.write(f'**Student:** {selected_application["student_name"]}')
            st.write(f'**Email:** {selected_application["email"]}')
            st.write(f'**Current Status:** {selected_application["application_status"]}')

            status_options = ["Under Review", "Shortlisted", "Rejected", "Selected"]
            new_status = st.selectbox(
                "Choose New Application Status",
                options=status_options,
                key=f"new_status_{selected_application_id}",
            )

            if st.button("Update Application Status", type="primary", use_container_width=True):
                success, message = update_application_status(selected_application_id, new_status)
                if success:
                    st.success(message)
                    st.info("The student's application status has been updated.")
                else:
                    st.error(message)


# ==========================================================
# RESUME ANALYSIS (ADMIN)
# ==========================================================

elif menu == "Resume Analysis" and user_role == "admin":

    st.title("Student Resume Analysis")
    st.caption("View and review resumes uploaded by students.")

    resume_df = get_student_resumes()

    if resume_df.empty:
        st.info("No student resumes have been uploaded yet.")
    else:
        st.subheader("Search Students")
        search_text = st.text_input(
            "Search by student name or email",
            placeholder="Enter student name or email...",
        )

        filtered_df = resume_df.copy()
        if search_text:
            search_lower = search_text.lower()
            filtered_df = filtered_df[
                filtered_df["Student Name"].str.lower().str.contains(search_lower, na=False)
                | filtered_df["Email"].str.lower().str.contains(search_lower, na=False)
            ]

        st.write(f"**Students found:** {len(filtered_df)}")

        if filtered_df.empty:
            st.warning("No students found matching your search.")
        else:
            st.subheader("Student Resumes")

            display_df = filtered_df[
                [
                    "Resume ID",
                    "Student Name",
                    "Email",
                    "Target Job Role",
                    "Resume Score",
                    "Resume Status",
                    "Uploaded At",
                ]
            ].copy()

            st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.divider()
            st.subheader("Detailed Resume Analysis")

            student_options = (
                filtered_df["Resume ID"].astype(str)
                + " - "
                + filtered_df["Student Name"]
                + " - "
                + filtered_df["Email"]
            ).tolist()

            selected_student = st.selectbox("Select Resume", student_options)
            selected_index = student_options.index(selected_student)
            selected_resume = filtered_df.iloc[selected_index]

            st.divider()
            st.subheader("Student Information")

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Student Name:** {selected_resume['Student Name']}")
                st.write(f"**Email:** {selected_resume['Email']}")
                st.write(f"**User ID:** {selected_resume['User ID']}")
            with col2:
                st.write(f"**Target Job Role:** {selected_resume['Target Job Role']}")
                st.write(f"**Resume File:** {selected_resume['File Name']}")
                st.write(f"**Uploaded At:** {selected_resume['Uploaded At']}")

            st.divider()
            st.subheader("Resume Readiness")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Resume Score", f"{float(selected_resume['Resume Score']):.2f}/100")
            with col2:
                if selected_resume["Resume Status"] == "Resume Ready":
                    st.success("Resume Ready")
                else:
                    st.warning("Needs Improvement")

            st.divider()
            st.subheader("Detected Skills")

            detected_skills = selected_resume["Detected Skills"]
            if isinstance(detected_skills, str) and detected_skills.strip():
                skills = [s.strip() for s in detected_skills.split(",") if s.strip()]
                for skill in skills:
                    st.success(skill)
            else:
                st.warning("No detected skills available.")

            st.subheader("Missing Skills")
            missing_skills = selected_resume["Missing Skills"]
            if isinstance(missing_skills, str) and missing_skills.strip():
                skills = [s.strip() for s in missing_skills.split(",") if s.strip()]
                for skill in skills:
                    st.error(skill)
            else:
                st.success("No missing skills identified.")

            st.divider()
            st.subheader("Resume File")

            resume_data = get_resume_by_user(int(selected_resume["User ID"]))
            if resume_data:
                resume_file_path = resume_data[2]
                if os.path.exists(resume_file_path):
                    with open(resume_file_path, "rb") as file:
                        resume_bytes = file.read()

                    st.download_button(
                        label="Download Resume (PDF)",
                        data=resume_bytes,
                        file_name=selected_resume["File Name"],
                        mime="application/pdf",
                    )
                else:
                    st.warning("Resume file could not be found on disk.")
            else:
                st.warning("Resume information not found.")


# ==========================================================
# PLACEMENT NOTIFICATIONS (ADMIN)
# ==========================================================

elif menu == "Notifications" and user_role == "admin":

    st.title("Placement Notifications")
    st.caption(
        "Send official DAV University placement drive announcements to eligible students' "
        "registered email addresses, or send individual in-app updates."
    )
    st.divider()

    tab_email, tab_inapp = st.tabs(
        ["Placement Drive Email Announcements", "Individual In-App Notification"]
    )

    with tab_email:
        drives_df = get_all_placement_drives()

        if drives_df.empty:
            st.info("No placement drives are available. Create a placement drive first.")
        else:
            drive_options = {
                int(row["drive_id"]): (
                    f'{row["company_name"]} — {row["drive_name"]} ({row["job_role"]}) [{row["drive_status"]}]'
                )
                for _, row in drives_df.iterrows()
            }

            selected_drive_id = st.selectbox(
                "Select Placement Drive",
                options=list(drive_options.keys()),
                format_func=lambda x: drive_options[x],
                key="notif_drive_selection",
            )

            selected_drive = drives_df[drives_df["drive_id"] == selected_drive_id].iloc[0]
            eligible_branches = get_drive_eligible_branches(selected_drive_id)

            try:
                results_df = get_drive_eligibility_results(selected_drive_id)
                notified_map = get_notified_students_for_drive(selected_drive_id)

                if results_df.empty:
                    st.info("No registered students found in the database.")
                else:
                    total_students = len(results_df)
                    eligible_df = results_df[
                        results_df["eligibility_status"] == "Eligible"
                    ].copy()
                    ineligible_count = total_students - len(eligible_df)

                    already_notified_count = sum(
                        1 for uid in eligible_df["user_id"].tolist()
                        if int(uid) in notified_map
                    )

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Students", total_students)
                    col2.metric("Eligible Students", len(eligible_df))
                    col3.metric("Ineligible / Incomplete", ineligible_count)
                    col4.metric("Already Notified", already_notified_count)

                    st.divider()

                    if eligible_df.empty:
                        st.warning(
                            "No eligible students match this drive's criteria. "
                            "Notifications can only be sent to eligible students."
                        )
                    else:
                        eligible_df["Notification Status"] = eligible_df["user_id"].apply(
                            lambda uid: (
                                f"Sent ({notified_map[int(uid)]['sent_count']}x)"
                                if int(uid) in notified_map
                                else "Not Notified"
                            )
                        )
                        eligible_df["Last Notified"] = eligible_df["user_id"].apply(
                            lambda uid: (
                                str(notified_map[int(uid)]["last_sent_at"])[:16]
                                if int(uid) in notified_map
                                else "—"
                            )
                        )

                        st.subheader("Eligible Students")
                        st.dataframe(
                            eligible_df[
                                [
                                    "student_name",
                                    "email",
                                    "branch",
                                    "cgpa",
                                    "Notification Status",
                                    "Last Notified",
                                ]
                            ].rename(
                                columns={
                                    "student_name": "Student Name",
                                    "email": "Registered Email",
                                    "branch": "Branch",
                                    "cgpa": "CGPA",
                                }
                            ),
                            use_container_width=True,
                            hide_index=True,
                        )

                        st.divider()
                        st.subheader("Select Recipients")

                        allow_resend = st.checkbox(
                            "Include students who were already notified (Intentional Resend)",
                            value=False,
                            key=f"allow_resend_{selected_drive_id}",
                        )

                        if allow_resend:
                            selectable_df = eligible_df.copy()
                        else:
                            selectable_df = eligible_df[
                                ~eligible_df["user_id"].astype(int).isin(notified_map.keys())
                            ].copy()

                        if selectable_df.empty:
                            st.info(
                                "All eligible students have already been notified for this drive. "
                                "Check the box above if you want to intentionally resend."
                            )
                        else:
                            recipient_lookup = {}
                            for _, row in selectable_df.iterrows():
                                uid = int(row["user_id"])
                                status_tag = (
                                    f" [Sent {notified_map[uid]['sent_count']}x]"
                                    if uid in notified_map
                                    else ""
                                )
                                label = f"{row['student_name']} ({row['email']}){status_tag}"
                                recipient_lookup[label] = {
                                    "user_id": uid,
                                    "student_name": str(row["student_name"]),
                                    "email": str(row["email"]),
                                }

                            all_labels = list(recipient_lookup.keys())

                            select_all = st.checkbox(
                                f"Select all {len(all_labels)} eligible recipient(s)",
                                value=True,
                                key=f"select_all_eligible_{selected_drive_id}_{allow_resend}",
                            )

                            if select_all:
                                selected_labels = all_labels
                            else:
                                selected_labels = st.multiselect(
                                    "Choose specific eligible students",
                                    options=all_labels,
                                    key=f"multiselect_eligible_{selected_drive_id}_{allow_resend}",
                                )

                            selected_recipients = [
                                recipient_lookup[lbl] for lbl in selected_labels
                            ]

                            st.caption(
                                f"Selected recipients: **{len(selected_recipients)}** of "
                                f"**{len(eligible_df)}** eligible student(s)."
                            )

                            pkg_min = selected_drive["package_min_lpa"]
                            pkg_max = selected_drive["package_max_lpa"]
                            if pkg_max and float(pkg_max) > 0:
                                package_text = f"{pkg_min} - {pkg_max} LPA"
                            else:
                                package_text = "As per company norms"

                            criteria_parts = []
                            if selected_drive["min_cgpa"] and float(selected_drive["min_cgpa"]) > 0:
                                criteria_parts.append(f"Min CGPA: {selected_drive['min_cgpa']}")
                            if selected_drive["min_tenth_percentage"] and float(selected_drive["min_tenth_percentage"]) > 0:
                                criteria_parts.append(f"10th: {selected_drive['min_tenth_percentage']}%")
                            if selected_drive["min_twelfth_percentage"] and float(selected_drive["min_twelfth_percentage"]) > 0:
                                criteria_parts.append(f"12th: {selected_drive['min_twelfth_percentage']}%")
                            if selected_drive["max_active_backlogs"] is not None:
                                criteria_parts.append(f"Max Backlogs: {selected_drive['max_active_backlogs']}")
                            if eligible_branches:
                                criteria_parts.append(f"Branches: {', '.join(eligible_branches)}")
                            if selected_drive["graduation_year"]:
                                criteria_parts.append(f"Batch: {selected_drive['graduation_year']}")

                            criteria_text = " | ".join(criteria_parts) if criteria_parts else "As per drive details"

                            drive_details = {
                                "company_name": selected_drive["company_name"],
                                "drive_name": selected_drive["drive_name"],
                                "job_role": selected_drive["job_role"],
                                "package": package_text,
                                "location": selected_drive["job_location"] or "To be announced",
                                "eligibility_criteria": criteria_text,
                                "application_deadline": (
                                    str(selected_drive["application_deadline"])
                                    if selected_drive["application_deadline"]
                                    else "Apply as soon as possible"
                                ),
                            }

                            with st.expander("Preview Email Details"):
                                st.write(
                                    f"**Subject:** Placement Opportunity – "
                                    f"{drive_details['company_name']} | {drive_details['job_role']} | DAV University"
                                )
                                st.write(f"**Package:** {drive_details['package']}")
                                st.write(f"**Location:** {drive_details['location']}")
                                st.write(f"**Eligibility Criteria:** {drive_details['eligibility_criteria']}")
                                st.write(f"**Application Deadline:** {drive_details['application_deadline']}")

                            if st.button(
                                "Send Placement Notification Email",
                                type="primary",
                                use_container_width=True,
                                key=f"send_drive_notif_btn_{selected_drive_id}",
                            ):
                                if not selected_recipients:
                                    st.warning("Please select at least one eligible student.")
                                else:
                                    with st.spinner("Sending official placement notifications..."):
                                        result = send_placement_drive_notifications(
                                            selected_recipients,
                                            drive_details,
                                        )

                                    if result["error"]:
                                        st.error(result["error"])
                                    else:
                                        sent_list = result["sent"]
                                        failed_list = result["failed"]

                                        for student in sent_list:
                                            log_drive_email_notification(
                                                selected_drive_id,
                                                student["user_id"],
                                                student["email"],
                                                st.session_state.user["user_id"],
                                            )
                                            create_notification(
                                                student["user_id"],
                                                f"Placement Drive: {drive_details['company_name']} ({drive_details['job_role']})",
                                                (
                                                    f"You are eligible for {drive_details['company_name']} - "
                                                    f"{drive_details['job_role']} ({drive_details['package']}). "
                                                    f"Deadline: {drive_details['application_deadline']}. "
                                                    "Apply via Placement Drives."
                                                ),
                                                "placement",
                                            )

                                        st.success(
                                            f"Placement notification delivery complete: "
                                            f"{len(sent_list)} sent, {len(failed_list)} failed."
                                        )

                                        m1, m2, m3, m4 = st.columns(4)
                                        m1.metric("Eligible Students", len(eligible_df))
                                        m2.metric("Selected", len(selected_recipients))
                                        m3.metric("Emails Sent", len(sent_list))
                                        m4.metric("Failed", len(failed_list))

                                        if failed_list:
                                            st.error("Some emails could not be delivered:")
                                            for item in failed_list:
                                                st.write(
                                                    f"- {item['recipient']['student_name']} "
                                                    f"({item['recipient']['email']}): {item['reason']}"
                                                )

            except Exception as e:
                st.error(f"Unable to load eligibility and notification data: {e}")

    with tab_inapp:
        st.subheader("Send Individual In-App Notification")

        students = get_student_records()

        if students.empty:
            st.info("No students are available.")
        else:
            student_options = {
                f"{row['Student Name']} ({row['Email']})": row["User ID"]
                for _, row in students.iterrows()
            }

            selected_student = st.selectbox("Select Student", list(student_options.keys()))
            selected_user_id = student_options[selected_student]

            title = st.text_input("Notification Title", placeholder="Enter notification title")
            message = st.text_area("Notification Message", placeholder="Enter notification message", height=120)
            notification_type = st.selectbox(
                "Notification Type",
                ["general", "placement", "resume", "interview", "important"],
            )

            if st.button("Send Notification", type="primary", use_container_width=True):
                if not title.strip():
                    st.error("Please enter a notification title.")
                elif not message.strip():
                    st.error("Please enter a notification message.")
                else:
                    create_notification(
                        selected_user_id,
                        title.strip(),
                        message.strip(),
                        notification_type,
                    )
                    st.success(f"Notification sent successfully to {selected_student}.")


# ==========================================================
# STUDENT DASHBOARD
# ==========================================================

elif menu == "Dashboard" and user_role == "student":

    user_id = st.session_state.user["user_id"]

    profile = get_student_profile(user_id) or {}
    history = get_prediction_history(user_id)
    latest_resume = get_resume_by_user(user_id)
    applications = get_student_applications(user_id)
    notifications = get_student_notifications(user_id)
    drives_df = get_all_placement_drives()

    required_fields = [
        "phone",
        "university",
        "course",
        "branch",
        "graduation_year",
        "cgpa",
        "tenth_percentage",
        "twelfth_percentage",
    ]
    completed_fields = sum(
        1 for f in required_fields if profile.get(f) is not None and str(profile.get(f)).strip() != ""
    )
    completion = int((completed_fields / len(required_fields)) * 100)

    latest_prediction = "Not Run"
    if not history.empty:
        latest_prediction = str(history.iloc[0].get("Prediction", "Not Run"))

    resume_score_display = f"{float(latest_resume[4]):.0f}/100" if latest_resume else "Pending"

    open_drives = (
        drives_df[drives_df["drive_status"] == "Open"].copy()
        if not drives_df.empty
        else pd.DataFrame()
    )

    st.markdown(
        f"""
        <div class="hero-card">
            <span class="hero-kicker">DAV University, Jalandhar — Student Placement Portal</span>
            <div class="hero-title">Welcome back, {user_name}</div>
            <div class="hero-sub">
                Your profile is <strong>{completion}% complete</strong> and there are
                <strong>{len(open_drives)} open placement drive(s)</strong> available to explore.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Profile Completion</p>
                <p class="kpi-value">{completion}%</p>
                <p class="kpi-sub">Required for eligibility</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Placement Prediction</p>
                <p class="kpi-value">{latest_prediction}</p>
                <p class="kpi-sub">ML readiness estimate</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">Resume Readiness</p>
                <p class="kpi-value">{resume_score_display}</p>
                <p class="kpi-sub">Skill match score</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <p class="kpi-label">My Applications</p>
                <p class="kpi-value">{len(applications)}</p>
                <p class="kpi-sub">Submitted drives</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    left_col, right_col = st.columns([1.45, 1], gap="large")

    with left_col:
        st.subheader("Open Placement Opportunities")

        if open_drives.empty:
            st.info("No open placement drives at the moment. Check back soon.")
        else:
            for _, drive in open_drives.head(4).iterrows():
                pkg_min = drive["package_min_lpa"]
                pkg_max = drive["package_max_lpa"]
                if pkg_max and float(pkg_max) > 0:
                    pkg_text = f"{pkg_min} – {pkg_max} LPA"
                else:
                    pkg_text = "Package TBD"

                deadline = drive["application_deadline"] or "Open"
                location = drive["job_location"] or "Campus / TBD"
                emp_type = drive["employment_type"] or "Full-time"

                st.markdown(
                    f"""
                    <div class="drive-card">
                        <div class="drive-card-top">
                            <div>
                                <p class="drive-company">{drive['company_name']} &bull; {emp_type}</p>
                                <p class="drive-role">{drive['job_role']}</p>
                            </div>
                            <span class="pkg-badge">{pkg_text}</span>
                        </div>
                        <p class="drive-meta">
                            <strong>Location:</strong> {location} &nbsp;&nbsp;|&nbsp;&nbsp;
                            <strong>Deadline:</strong> {deadline}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            b1, b2 = st.columns(2)
            with b1:
                if st.button("Explore & Apply to Drives", type="primary", use_container_width=True):
                    st.session_state.active_page = "Placement Drives"
                    st.rerun()
            with b2:
                if st.button("Check Placement Readiness", type="secondary", use_container_width=True):
                    st.session_state.active_page = "Placement Readiness"
                    st.rerun()

    with right_col:
        st.subheader("Recent Notifications")

        if notifications.empty:
            st.info("You're all caught up — no notifications yet.")
        else:
            for _, notif in notifications.head(4).iterrows():
                n_type = str(notif["Type"]).strip().lower()
                created_str = str(notif["Created At"])[:16]

                st.markdown(
                    f"""
                    <div class="notif-card type-{n_type}">
                        <div class="notif-header">
                            <span class="notif-pill">{n_type}</span>
                            <span class="notif-time">{created_str}</span>
                        </div>
                        <p class="notif-title">{notif['Title']}</p>
                        <p class="notif-msg">{notif['Message']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("View All Notifications", type="secondary", use_container_width=True):
                st.session_state.active_page = "Notifications"
                st.rerun()


# ==========================================================
# PLACEMENT READINESS (COMBINED: PREDICTION + RESUME ANALYZER)
# ==========================================================

elif menu == "Placement Readiness" and user_role == "student":

    st.title("Placement Readiness")
    st.caption("Evaluate your placement probability and analyze your resume skills in one place.")
    st.divider()

    tab_predict, tab_resume = st.tabs(["Placement Prediction", "Resume Analyzer"])

    with tab_predict:
        st.subheader("Student Information")
        student_name = st.text_input("Student Name", value=user_name, placeholder="Enter your full name")
        job_role = st.selectbox(
            "Target Job Role",
            ["Data Scientist", "AI Engineer", "Data Analyst", "Software Developer", "Web Developer"],
            key="predict_job_role",
        )

        st.divider()
        st.subheader("Academic & Skill Information")

        col1, col2 = st.columns(2)
        with col1:
            cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
            internships = st.number_input("Internships", min_value=0, value=1, step=1)
            projects = st.number_input("Projects", min_value=0, value=2, step=1)
            workshops = st.number_input("Workshops / Certifications", min_value=0, value=2, step=1)
            aptitude = st.number_input("Aptitude Test Score", min_value=0, max_value=100, value=80, step=1)

        with col2:
            softskills = st.number_input("Soft Skills Rating", min_value=0, max_value=10, value=8, step=1)
            extracurricular = st.selectbox("Extracurricular Activities", ["No", "Yes"])
            placement_training = st.selectbox("Placement Training", ["No", "Yes"])
            ssc = st.number_input("SSC Marks", min_value=0.0, max_value=100.0, value=85.0, step=0.1)
            hsc = st.number_input("HSC Marks", min_value=0.0, max_value=100.0, value=85.0, step=0.1)

        st.divider()
        predict = st.button("Predict Placement", type="primary", use_container_width=True)

        if predict:
            if student_name.strip() == "":
                st.warning("Please enter the student's name.")
            else:
                extracurricular_value = 1 if extracurricular == "Yes" else 0
                placement_training_value = 1 if placement_training == "Yes" else 0

                student = pd.DataFrame(
                    [[
                        cgpa,
                        internships,
                        projects,
                        workshops,
                        aptitude,
                        softskills,
                        extracurricular_value,
                        placement_training_value,
                        ssc,
                        hsc,
                    ]],
                    columns=[
                        "CGPA",
                        "Internships",
                        "Projects",
                        "Workshops/Certifications",
                        "AptitudeTestScore",
                        "SoftSkillsRating",
                        "ExtracurricularActivities",
                        "PlacementTraining",
                        "SSC_Marks",
                        "HSC_Marks",
                    ],
                )

                prediction = model.predict(student)
                probability = model.predict_proba(student)
                confidence = probability.max() * 100
                prediction_result = "Placed" if prediction[0] == 1 else "Not Placed"

                save_prediction(
                    st.session_state.user["user_id"],
                    student_name,
                    job_role,
                    prediction_result,
                    float(confidence),
                )

                st.divider()
                st.subheader("Prediction Result")

                if prediction[0] == 1:
                    st.success("Student is Likely to be Placed")
                else:
                    st.error("Student is Likely to be Not Placed")

                st.metric(label="Prediction Confidence", value=f"{confidence:.2f}%")

                st.divider()
                st.subheader("Career Suggestions")

                suggestions = []
                if cgpa < 7.5:
                    suggestions.append("Improve your CGPA by focusing on core academic subjects.")
                if internships < 2:
                    suggestions.append("Try to complete at least 2 relevant internships.")
                if projects < 3:
                    suggestions.append("Build more real-world portfolio projects.")
                if aptitude < 70:
                    suggestions.append("Practice aptitude and logical reasoning regularly.")
                if softskills < 7:
                    suggestions.append("Strengthen communication and interview presentation skills.")
                if placement_training == "No":
                    suggestions.append("Join placement preparation or coding training sessions.")

                if not suggestions:
                    st.success("Excellent profile! Keep maintaining your performance.")
                else:
                    for item in suggestions:
                        st.write(f"- {item}")

    with tab_resume:
        st.subheader("Select Your Target Job Role")

        resume_job_role = st.selectbox(
            "Choose Job Role",
            ["Data Scientist", "AI Engineer", "Data Analyst", "Software Developer", "Web Developer"],
            key="resume_job_role",
        )

        st.divider()
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

        if "last_uploaded_resume" not in st.session_state:
            st.session_state.last_uploaded_resume = None

        if uploaded_file is not None:
            st.success("Resume uploaded successfully.")

            upload_folder = "uploads"
            os.makedirs(upload_folder, exist_ok=True)

            user_id = st.session_state.user["user_id"]
            safe_file_name = f"{user_id}_{uploaded_file.name}"
            file_path = os.path.join(upload_folder, safe_file_name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            resume_text = extract_resume_text(file_path)

            st.subheader("Extracted Resume Text")

            if resume_text:
                st.text_area("Resume Content", resume_text, height=300)

                skills = extract_skills(resume_text)
                st.subheader("Detected Skills")

                if skills:
                    for skill in skills:
                        st.success(skill)
                else:
                    st.warning("No known skills were detected.")

                missing_skills = recommend_skills(skills, resume_job_role)
                st.subheader(f"Missing Skills for {resume_job_role}")

                if missing_skills:
                    for skill in missing_skills:
                        st.error(skill)
                        recommendation = get_learning_path(skill)
                        st.info(f"Recommendation: {recommendation}")
                else:
                    st.success("You already have all the required skills for this role.")

                total_skills = len(skills)
                missing_count = len(missing_skills)
                resume_score = (
                    (total_skills / (total_skills + missing_count)) * 100
                    if (total_skills + missing_count) > 0
                    else 0
                )

                st.divider()
                st.subheader("Resume Readiness")
                st.metric("Resume Score", f"{resume_score:.2f}/100")

                if resume_score >= 70:
                    resume_status = "Resume Ready"
                    st.success("Resume is Ready for the selected job role.")
                else:
                    resume_status = "Needs Improvement"
                    st.warning("Resume needs improvement for the selected job role.")

                resume_key = f"{user_id}_{uploaded_file.name}"
                if st.session_state.last_uploaded_resume != resume_key:
                    save_resume(
                        user_id,
                        uploaded_file.name,
                        file_path,
                        resume_job_role,
                        float(resume_score),
                        resume_status,
                        skills,
                        missing_skills,
                    )
                    st.session_state.last_uploaded_resume = resume_key
                    st.success("Resume analysis saved successfully.")
            else:
                st.error("Unable to read the resume.")


# ==========================================================
# ELIGIBLE PLACEMENT DRIVES (STUDENT)
# ==========================================================

elif menu == "Placement Drives" and user_role == "student":

    st.title("Available Placement Drives")
    st.caption("Explore open placement opportunities and apply for suitable jobs.")
    st.divider()

    user_id = st.session_state.user["user_id"]
    drives_df = get_all_placement_drives()

    if drives_df.empty:
        st.info("No placement drives are available currently.")
    else:
        open_drives = drives_df[drives_df["drive_status"] == "Open"].copy()

        if open_drives.empty:
            st.info("There are currently no open placement drives. Please check again later.")
        else:
            drive_options = {
                int(row["drive_id"]): f'{row["company_name"]} - {row["drive_name"]}'
                for _, row in open_drives.iterrows()
            }

            selected_drive_id = st.selectbox(
                "Select a Placement Drive",
                options=list(drive_options.keys()),
                format_func=lambda x: drive_options[x],
                key="student_drive_selection",
            )

            selected_drive = open_drives[open_drives["drive_id"] == selected_drive_id].iloc[0]

            st.divider()
            st.subheader("Placement Opportunity")

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Company:** {selected_drive['company_name']}")
                st.write(f"**Job Role:** {selected_drive['job_role']}")
                st.write(f"**Location:** {selected_drive['job_location']}")
            with col2:
                st.write(
                    f"**Package:** {selected_drive['package_min_lpa']} - {selected_drive['package_max_lpa']} LPA"
                )
                st.write(f"**Employment Type:** {selected_drive['employment_type']}")
                st.write(f"**Application Deadline:** {selected_drive['application_deadline']}")

            if selected_drive["job_description"]:
                st.write("**Job Description:**")
                st.write(selected_drive["job_description"])

            st.divider()
            st.subheader("Eligibility Criteria")

            eligible_branches = get_drive_eligible_branches(selected_drive_id)
            st.write(f"**Eligible Branches:** {', '.join(eligible_branches) if eligible_branches else 'Not specified'}")
            st.write(f"**Minimum CGPA:** {selected_drive['min_cgpa']}")
            st.write(f"**Minimum 10th Marks:** {selected_drive['min_tenth_percentage']}%")
            st.write(f"**Minimum 12th Marks:** {selected_drive['min_twelfth_percentage']}%")
            st.write(f"**Maximum Active Backlogs:** {selected_drive['max_active_backlogs']}")
            st.write(f"**Minimum Internships:** {selected_drive['min_internships']}")
            st.write(f"**Required Graduation Year:** {selected_drive['graduation_year']}")

            st.divider()
            st.subheader("Your Eligibility")

            try:
                eligibility_df = get_drive_eligibility_results(selected_drive_id)
                student_result = eligibility_df[eligibility_df["user_id"] == user_id]

                if student_result.empty:
                    st.warning("Your student account was not found in the eligibility results.")
                else:
                    student_result = student_result.iloc[0]
                    eligibility_status = student_result["eligibility_status"]
                    eligibility_reason = student_result["eligibility_reason"]

                    if eligibility_status == "Eligible":
                        st.success("You are eligible to apply for this drive.")
                    elif eligibility_status == "Ineligible":
                        st.error("You do not meet this drive's eligibility criteria.")
                        st.write(f"**Reason:** {eligibility_reason}")
                    else:
                        st.warning("Your profile is incomplete. Update your profile before applying.")
                        st.write(f"**Missing Information:** {eligibility_reason}")

                    applications = get_student_applications(user_id)
                    already_applied = any(
                        int(application["drive_id"]) == int(selected_drive_id)
                        for application in applications
                    )

                    st.divider()
                    st.subheader("Apply for This Drive")

                    if already_applied:
                        st.info("You have already submitted an application for this placement drive.")
                    elif eligibility_status != "Eligible":
                        st.warning("You can apply after meeting all eligibility requirements and completing your profile.")
                    else:
                        if st.button(
                            "Submit Application",
                            type="primary",
                            use_container_width=True,
                            key=f"apply_drive_{selected_drive_id}",
                        ):
                            success, message = apply_for_placement(user_id, selected_drive_id)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

            except Exception as e:
                st.error(f"Unable to check eligibility: {e}")


# ==========================================================
# MY APPLICATIONS (STUDENT)
# ==========================================================

elif menu == "My Applications" and user_role == "student":

    st.title("My Applications")
    st.caption("Track the status of your placement applications.")
    st.divider()

    user_id = st.session_state.user["user_id"]
    applications = get_student_applications(user_id)

    if not applications:
        st.info("You have not applied for any placement drives yet.")
        st.write("Visit Placement Drives above to explore opportunities.")
    else:
        total_applications = len(applications)
        shortlisted = sum(1 for app in applications if app["application_status"] == "Shortlisted")
        selected = sum(1 for app in applications if app["application_status"] == "Selected")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Applications", total_applications)
        col2.metric("Shortlisted", shortlisted)
        col3.metric("Selected", selected)

        st.divider()
        st.subheader("Your Application History")

        for application in applications:
            with st.container(border=True):
                st.subheader(application["drive_name"])
                st.write(f"**Company:** {application['company_name']}")
                st.write(f"**Job Role:** {application['job_role']}")
                st.write(f"**Location:** {application['job_location']}")
                st.write(
                    f"**Package:** {application['package_min_lpa']} - {application['package_max_lpa']} LPA"
                )
                st.write(f"**Applied On:** {application['applied_at'].strftime('%d-%m-%Y')}")

                status = application["application_status"]
                if status in ("Selected", "Shortlisted"):
                    st.success(f"Status: {status}")
                elif status == "Rejected":
                    st.error("Status: Rejected")
                elif status == "Withdrawn":
                    st.warning("Status: Withdrawn")
                else:
                    st.info(f"Status: {status}")


# ==========================================================
# NOTIFICATIONS (STUDENT)
# ==========================================================

elif menu == "Notifications" and user_role == "student":

    st.title("Notifications")
    st.caption("View important updates and placement messages from DAV University.")
    st.divider()

    user_id = st.session_state.user["user_id"]
    notifications = get_student_notifications(user_id)

    if notifications.empty:
        st.info("You don't have any notifications yet.")
    else:
        st.success(f"Total Notifications: {len(notifications)}")

        for _, notification in notifications.iterrows():
            n_type = str(notification["Type"]).strip().lower()
            created_str = str(notification["Created At"])[:16]
            st.markdown(
                f"""
                <div class="notif-card type-{n_type}">
                    <div class="notif-header">
                        <span class="notif-pill">{n_type}</span>
                        <span class="notif-time">{created_str}</span>
                    </div>
                    <p class="notif-title">{notification['Title']}</p>
                    <p class="notif-msg">{notification['Message']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==========================================================
# STUDENT PROFILE
# ==========================================================

elif menu == "My Profile" and user_role == "student":

    st.title("My Student Profile")
    st.caption("Complete your personal, academic, and placement information to qualify for placement drives.")
    st.divider()

    user_id = st.session_state.user["user_id"]
    profile = get_student_profile(user_id) or {}

    required_fields = [
        "phone",
        "university",
        "course",
        "branch",
        "graduation_year",
        "cgpa",
        "tenth_percentage",
        "twelfth_percentage",
    ]

    completed_fields = sum(
        1
        for field in required_fields
        if profile.get(field) is not None and str(profile.get(field)).strip() != ""
    )

    completion = int((completed_fields / len(required_fields)) * 100)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Profile Completion", f"{completion}%")
    with col2:
        st.progress(completion / 100)

    st.divider()

    with st.form("student_profile_form"):
        st.subheader("1. Personal Information")
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Full Name", value=st.session_state.user["full_name"], disabled=True)
            st.text_input("Email Address", value=st.session_state.user["email"], disabled=True)
            phone = st.text_input("Phone Number", value=profile.get("phone") or "", max_chars=20)
            alternate_phone = st.text_input("Alternate Phone Number", value=profile.get("alternate_phone") or "", max_chars=20)

            gender_options = ["", "Male", "Female", "Other"]
            current_gender = profile.get("gender") or ""
            gender = st.selectbox(
                "Gender",
                gender_options,
                index=gender_options.index(current_gender) if current_gender in gender_options else 0,
            )

        with col2:
            date_of_birth = st.date_input(
                "Date of Birth",
                value=profile.get("date_of_birth"),
                min_value=datetime.date(1950, 1, 1),
                max_value=datetime.date.today(),
            )
            address = st.text_area("Address", value=profile.get("address") or "")
            city = st.text_input("City", value=profile.get("city") or "")
            state = st.text_input("State", value=profile.get("state") or "")
            pincode = st.text_input("PIN Code", value=profile.get("pincode") or "", max_chars=10)

        st.divider()
        st.subheader("2. Academic Information")
        col1, col2 = st.columns(2)

        with col1:
            university = st.text_input("University", value=profile.get("university") or "DAV University, Jalandhar")
            course = st.text_input("Course", value=profile.get("course") or "")
            branch = st.text_input("Branch / Specialization", value=profile.get("branch") or "")
            graduation_year = st.text_input(
                "Graduation Year",
                value=str(profile["graduation_year"]) if profile.get("graduation_year") is not None else "",
            )

        with col2:
            cgpa = st.text_input("CGPA (out of 10)", value=str(profile["cgpa"]) if profile.get("cgpa") is not None else "")
            tenth_percentage = st.text_input(
                "10th Percentage",
                value=str(profile["tenth_percentage"]) if profile.get("tenth_percentage") is not None else "",
            )
            twelfth_percentage = st.text_input(
                "12th Percentage",
                value=str(profile["twelfth_percentage"]) if profile.get("twelfth_percentage") is not None else "",
            )
            active_backlogs = st.text_input("Active Backlogs", value=str(profile.get("active_backlogs") or 0))

        st.divider()
        st.subheader("3. Placement Information")
        col1, col2 = st.columns(2)

        role_options = [
            "",
            "Data Scientist",
            "Data Analyst",
            "AI Engineer",
            "Software Developer",
            "Web Developer",
            "Other",
        ]

        with col1:
            internships = st.text_input("Number of Internships", value=str(profile.get("internships") or 0))
            projects = st.text_input("Number of Projects", value=str(profile.get("projects") or 0))
            preferred_job_role = st.selectbox(
                "Preferred Job Role",
                role_options,
                index=role_options.index(profile.get("preferred_job_role"))
                if profile.get("preferred_job_role") in role_options
                else 0,
            )

        with col2:
            aptitude_score = st.text_input(
                "Aptitude Score",
                value=str(profile["aptitude_score"]) if profile.get("aptitude_score") is not None else "",
            )
            soft_skills_rating = st.text_input(
                "Soft Skills Rating (out of 5)",
                value=str(profile["soft_skills_rating"]) if profile.get("soft_skills_rating") is not None else "",
            )

            yes_no_options = ["", "Yes", "No"]
            extracurricular_activities = st.selectbox(
                "Extracurricular Activities",
                yes_no_options,
                index=yes_no_options.index(profile.get("extracurricular_activities") or "")
                if (profile.get("extracurricular_activities") or "") in yes_no_options
                else 0,
            )
            placement_training = st.selectbox(
                "Placement Training Completed",
                yes_no_options,
                index=yes_no_options.index(profile.get("placement_training") or "")
                if (profile.get("placement_training") or "") in yes_no_options
                else 0,
            )

        technical_skills = st.text_area(
            "Technical Skills",
            value=profile.get("technical_skills") or "",
            placeholder="Example: Python, SQL, Machine Learning",
        )
        certifications = st.text_area(
            "Certifications",
            value=profile.get("certifications") or "",
            placeholder="Enter your certifications",
        )

        st.divider()
        submitted = st.form_submit_button("Save / Update Profile", use_container_width=True)

    if submitted:
        try:
            if not phone.strip():
                raise ValueError("Phone number is required.")
            if not phone.strip().replace("+", "").isdigit():
                raise ValueError("Enter a valid phone number.")

            def optional_float(value, field_name):
                if not value.strip():
                    return None
                number = float(value)
                if number < 0:
                    raise ValueError(f"{field_name} cannot be negative.")
                return number

            def optional_int(value, field_name):
                if not value.strip():
                    return 0
                number = int(value)
                if number < 0:
                    raise ValueError(f"{field_name} cannot be negative.")
                return number

            parsed_cgpa = optional_float(cgpa, "CGPA")
            parsed_tenth = optional_float(tenth_percentage, "10th percentage")
            parsed_twelfth = optional_float(twelfth_percentage, "12th percentage")
            parsed_aptitude = optional_float(aptitude_score, "Aptitude score")
            parsed_soft_skills = optional_float(soft_skills_rating, "Soft skills rating")

            if parsed_cgpa is not None and parsed_cgpa > 10:
                raise ValueError("CGPA must be between 0 and 10.")

            for value, label in [
                (parsed_tenth, "10th percentage"),
                (parsed_twelfth, "12th percentage"),
                (parsed_aptitude, "Aptitude score"),
            ]:
                if value is not None and value > 100:
                    raise ValueError(f"{label} must be between 0 and 100.")

            if parsed_soft_skills is not None and parsed_soft_skills > 5:
                raise ValueError("Soft skills rating must be between 0 and 5.")

            parsed_year = optional_int(graduation_year, "Graduation year") if graduation_year.strip() else None
            if parsed_year is not None and parsed_year < 2000:
                raise ValueError("Enter a valid graduation year.")

            profile_data = {
                "phone": phone.strip(),
                "alternate_phone": alternate_phone.strip() or None,
                "date_of_birth": date_of_birth,
                "gender": gender or None,
                "address": address.strip() or None,
                "city": city.strip() or None,
                "state": state.strip() or None,
                "pincode": pincode.strip() or None,
                "university": university.strip() or None,
                "course": course.strip() or None,
                "branch": branch.strip() or None,
                "graduation_year": parsed_year,
                "cgpa": parsed_cgpa,
                "tenth_percentage": parsed_tenth,
                "twelfth_percentage": parsed_twelfth,
                "active_backlogs": optional_int(active_backlogs, "Active backlogs"),
                "internships": optional_int(internships, "Internships"),
                "projects": optional_int(projects, "Projects"),
                "technical_skills": technical_skills.strip() or None,
                "certifications": certifications.strip() or None,
                "preferred_job_role": preferred_job_role or None,
                "aptitude_score": parsed_aptitude,
                "soft_skills_rating": parsed_soft_skills,
                "extracurricular_activities": extracurricular_activities or None,
                "placement_training": placement_training or None,
            }

            save_student_profile(user_id, profile_data)
            st.success("Your student profile has been saved successfully.")
            st.rerun()

        except ValueError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Unable to save your profile: {error}")