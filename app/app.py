# ==========================================================
# CareerAI - AI Powered Placement Prediction System
# Developed by: Aditi Sharma
# ==========================================================

# -----------------------------
# Import Libraries
# -----------------------------

import streamlit as st
import pandas as pd
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from resume.resume_parser import extract_resume_text
from resume.skill_extractor import extract_skills
from resume.recommendations import recommend_skills
from resume.learning_path import get_learning_path
from backend.database.operations import (
    save_prediction,
    get_prediction_history,
    get_dashboard_stats,
    get_student_records
)
from backend.auth.authentication import (
    login_user,
    register_student
)

# -----------------------------
# Login Session
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "show_registration" not in st.session_state:
    st.session_state.show_registration = False

# -----------------------------
# Streamlit Page Configuration
# -----------------------------

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Load Machine Learning Model
# -----------------------------

MODEL_PATH = os.path.join(
    "saved_models",
    "careerai_model.pkl"
)

if os.path.exists(MODEL_PATH):

    model = joblib.load(MODEL_PATH)

else:

    st.error("❌ Trained Model Not Found!")

    st.stop()

# ==========================================================
# LOGIN / REGISTRATION PAGE
# ==========================================================

if not st.session_state.logged_in:

    st.title("🎓 CareerAI")

    st.subheader("AI Powered Placement Prediction System")

    st.markdown("---")

    # ======================================================
    # STUDENT REGISTRATION
    # ======================================================

    if st.session_state.show_registration:

        st.subheader("📝 Create Student Account")

        st.markdown(
            "Create an account to access the CareerAI Student Portal."
        )

        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email address"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        register_button = st.button(
            "📝 Create Account",
            use_container_width=True
        )

        if register_button:

            if (
                full_name.strip() == ""
                or email.strip() == ""
                or password.strip() == ""
                or confirm_password.strip() == ""
            ):
                st.warning(
                    "⚠️ Please fill in all fields."
                )

            elif password != confirm_password:
                st.error(
                    "❌ Passwords do not match."
                )

            elif len(password) < 6:
                st.error(
                    "❌ Password must contain at least 6 characters."
                )

            else:

                success, message = register_student(
                    full_name.strip(),
                    email.strip(),
                    password
                )

                if success:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "You can now login using your email and password."
                    )

                    st.session_state.show_registration = False

                else:

                    st.error(
                        f"❌ {message}"
                    )

        st.markdown("---")

        if st.button(
            "⬅️ Back to Login",
            use_container_width=True
        ):
            st.session_state.show_registration = False
            st.rerun()

    # ======================================================
    # LOGIN
    # ======================================================

    else:

        st.subheader("🔐 Login")

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        login_button = st.button(
            "🔑 Login",
            use_container_width=True
        )

        if login_button:

            if (
                email.strip() == ""
                or password.strip() == ""
            ):
                st.warning(
                    "⚠️ Please enter both email and password."
                )

            else:

                user = login_user(
                    email.strip(),
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )

        st.markdown("---")

        st.subheader("👨‍🎓 New Student?")

        if st.button(
            "📝 Create Student Account",
            use_container_width=True
        ):
            st.session_state.show_registration = True
            st.rerun()

    st.stop()



# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🎓 CareerAI")
st.sidebar.markdown("---")

user = st.session_state.user

user_role = user["role"]
user_name = user["full_name"]


# ==========================================================
# STUDENT NAVIGATION
# ==========================================================

if user_role == "student":

    st.sidebar.success(
        f"👨‍🎓 Welcome, {user_name}"
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Student Dashboard",
            "🎓 Placement Prediction",
            "📄 Resume Analyzer",
            "📊 My Prediction History",
            "👨‍💻 About"
        ]
    )


# ==========================================================
# ADMIN NAVIGATION
# ==========================================================

elif user_role == "admin":

    st.sidebar.success(
        f"👤 Welcome, {user_name}"
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Admin Dashboard",
            "📊 Placement Statistics",
            "👨‍🎓 Student Records",
            "📄 Resume Analysis",
            "👨‍💻 About"
        ]
    )


# ==========================================================
# TECHNOLOGY
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.subheader("Technology Used")

st.sidebar.write("🐍 Python")
st.sidebar.write("🤖 Machine Learning")
st.sidebar.write("📊 Scikit-Learn")
st.sidebar.write("🗄️ MySQL")
st.sidebar.write("🌐 Streamlit")
st.sidebar.write("📑 Pandas")


# ==========================================================
# LOGOUT
# ==========================================================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.show_registration = False

    st.rerun()
# ==========================================================
# STUDENT DASHBOARD
# ==========================================================

if menu == "🏠 Student Dashboard":

    st.title("👨‍🎓 Student Dashboard")

    st.subheader(
        f"Welcome, {user_name}! 👋"
    )

    st.markdown("---")

    st.write(
        """
        Welcome to your CareerAI Student Portal.

        Here you can check your placement prediction,
        analyze your resume, improve your skills and
        track your career progress.
        """
    )

    st.markdown("---")

    st.subheader("🚀 CareerAI Services")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "🎓 **Placement Prediction**\n\n"
            "Check your predicted placement status "
            "using your academic and skill profile."
        )

        st.info(
            "📄 **Resume Analyzer**\n\n"
            "Analyze your resume and identify important "
            "skills for your target job role."
        )

    with col2:

        st.info(
            "💡 **Career Suggestions**\n\n"
            "Get suggestions for improving your "
            "skills and career profile."
        )

        st.info(
            "📊 **Prediction History**\n\n"
            "View your previous placement predictions."
        )

    st.markdown("---")

    st.success(
        "💡 Keep improving your skills and building "
        "real-world projects!"
    )

# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

elif menu == "🏠 Admin Dashboard":

    st.title("👤 Admin Dashboard")

    st.subheader(
        "CareerAI Placement Management"
    )

    st.markdown("---")

    total_predictions, placed_students, not_placed_students = (
        get_dashboard_stats()
    )

    st.subheader("📊 Placement Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Predictions",
            total_predictions
        )

    with col2:

        st.metric(
            "Likely Placed",
            placed_students
        )

    with col3:

        st.metric(
            "Likely Not Placed",
            not_placed_students
        )

    st.markdown("---")

    st.subheader("👨‍🎓 Student Monitoring")

    st.write(
        """
        As an administrator, you can monitor student
        placement predictions, analyze student profiles
        and view overall placement statistics.
        """
    )

    st.markdown("---")

    st.subheader("📌 Admin Functions")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "👨‍🎓 **Student Records**\n\n"
            "View registered student information."
        )

    with col2:

        st.info(
            "📊 **Placement Statistics**\n\n"
            "Analyze overall placement prediction results."
        )
# -----------------------------------------------------------
# Placement Prediction Page
# -----------------------------------------------------------

elif menu == "🎓 Placement Prediction":
    st.title("🎓 Placement Prediction")

    st.markdown(
        "Enter the student's academic and skill details below."
    )

    st.markdown("---")



    # ------------------------------------
    # Student Information
    # ------------------------------------

    st.subheader("👤 Student Information")

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your full name"
    )

    job_role = st.selectbox(
        "Target Job Role",
        [
            "Data Scientist",
            "AI Engineer",
            "Data Analyst",
            "Software Developer",
            "Web Developer"
        ]
    )

    st.markdown("---")

    # ------------------------------------
    # Student Input Form
    # ------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=8.0,
            step=0.1
        )

        internships = st.number_input(
            "Internships",
            min_value=0,
            value=1
        )

        projects = st.number_input(
            "Projects",
            min_value=0,
            value=2
        )

        workshops = st.number_input(
            "Workshops / Certifications",
            min_value=0,
            value=2
        )

        aptitude = st.number_input(
            "Aptitude Test Score",
            min_value=0,
            max_value=100,
            value=80
        )

    with col2:
        softskills = st.number_input(
            "Soft Skills Rating",
            min_value=0,
            max_value=10,
            value=8
        )

        extracurricular = st.selectbox(
            "Extracurricular Activities",
            ["No", "Yes"]
        )

        placement_training = st.selectbox(
            "Placement Training",
            ["No", "Yes"]
        )

        ssc = st.number_input(
            "SSC Marks",
            min_value=0.0,
            max_value=100.0,
            value=85.0
        )

        hsc = st.number_input(
            "HSC Marks",
            min_value=0.0,
            max_value=100.0,
            value=85.0
        )

    st.markdown("---")

    predict = st.button(
        "🚀 Predict Placement",
        use_container_width=True
    )

    # ------------------------------------
    # Prediction
    # ------------------------------------

    if predict:
        if student_name.strip() == "":
            st.warning("⚠ Please enter the student's name.")
            st.stop()
        extracurricular_value = 1 if extracurricular == "Yes" else 0
        placement_training_value = 1 if placement_training == "Yes" else 0

        student = pd.DataFrame([[
            cgpa,
            internships,
            projects,
            workshops,
            aptitude,
            softskills,
            extracurricular_value,
            placement_training_value,
            ssc,
            hsc
        ]], columns=[
            "CGPA",
            "Internships",
            "Projects",
            "Workshops/Certifications",
            "AptitudeTestScore",
            "SoftSkillsRating",
            "ExtracurricularActivities",
            "PlacementTraining",
            "SSC_Marks",
            "HSC_Marks"
        ])

        prediction = model.predict(student)
        probability = model.predict_proba(student)
        confidence = probability.max() * 100

        # ------------------------------------
        # Save Prediction in Database
        # ------------------------------------

        prediction_result = (
            "Placed"
            if prediction[0] == 1
            else "Not Placed"
        )

        save_prediction(
            student_name,
            job_role,
            prediction_result,
            float(confidence)
        )

        st.markdown("---")
        st.subheader("📊 Prediction Result")

        if prediction[0] == 1:
            st.success("🎉 Student is Likely to be Placed")
        else:
            st.error("❌ Student is Likely to be Not Placed")

        st.metric(
            label="Prediction Confidence",
            value=f"{confidence:.2f}%"
        )

        st.markdown("---")

        # ------------------------------------
        # Student Summary
        # ------------------------------------

        st.subheader("📋 Student Summary")

        summary = pd.DataFrame({
            "Feature": [
                "CGPA",
                "Internships",
                "Projects",
                "Workshops",
                "Aptitude Score",
                "Soft Skills",
                "Extracurricular Activities",
                "Placement Training",
                "SSC Marks",
                "HSC Marks"
            ],
            "Value": [
                cgpa,
                internships,
                projects,
                workshops,
                aptitude,
                softskills,
                extracurricular,
                placement_training,
                ssc,
                hsc
            ]
        })

        st.table(summary)
        st.markdown("---")

        # ------------------------------------
        # Career Suggestions
        # ------------------------------------

        st.subheader("💡 Career Suggestions")

        suggestions = []

        if cgpa < 7.5:
            suggestions.append("📚 Improve your CGPA by focusing on academics.")

        if internships < 2:
            suggestions.append("🏢 Try to complete at least 2 internships.")

        if projects < 3:
            suggestions.append("💻 Build more real-world projects.")

        if aptitude < 70:
            suggestions.append("🧠 Practice aptitude and logical reasoning regularly.")

        if softskills < 7:
            suggestions.append("🎤 Improve communication and presentation skills.")

        if placement_training == "No":
            suggestions.append("🎯 Join placement preparation or coding training.")

        if len(suggestions) == 0:
            st.success("🎉 Excellent Profile! Keep maintaining your performance.")
        else:
            for item in suggestions:
                st.write(item)

        st.markdown("---")

# -----------------------------------------------------------
# Resume Analyzer
# -----------------------------------------------------------

elif menu == "📄 Resume Analyzer":
    st.title("📄 Resume Analyzer")
    st.subheader("🎯 Select Your Target Job Role")

    job_role = st.selectbox(
        "Choose Job Role",
        [
            "Data Scientist",
            "AI Engineer",
            "Data Analyst",
            "Software Developer",
            "Web Developer"
        ]
    )

    st.markdown("---")



    uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("✅ Resume Uploaded Successfully!")

        temp_path = os.path.join("app", uploaded_file.name)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        resume_text = extract_resume_text(temp_path)

        st.subheader("📄 Extracted Resume Text")

        if resume_text:

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )

        else:

            st.error("Unable to read the resume.")

    # ---------------------------------------
    # Detect Skills
    # ---------------------------------------

        skills = extract_skills(resume_text)

        st.subheader("🛠 Detected Skills")

        if len(skills) > 0:

            for skill in skills:
                st.success(f"✅ {skill}")

        else:

            st.warning("No known skills were detected.")

        # ---------------------------------------
        # Missing Skills
        # ---------------------------------------

        missing_skills = recommend_skills(skills, job_role)

        st.subheader(f"📚 Missing Skills for {job_role}")

        if len(missing_skills) > 0:

            for skill in missing_skills:

                st.error(f"❌ {skill}")

                recommendation = get_learning_path(skill)

                st.info(f"📖 Recommendation: {recommendation}")

        else:

            st.success("🎉 Excellent! You already have all the required skills for this role.")
# -----------------------------------------------------------
# Prediction History
# -----------------------------------------------------------

elif menu == "📊 My Prediction History":

    st.title("📊 My Prediction History")

    user_id = st.session_state.user["user_id"]

    history = get_prediction_history(user_id)

    if history.empty:

        st.info("📭 You have not made any predictions yet.")

    else:

        st.success(
            f"Total Predictions: {len(history)}"
        )

        st.dataframe(
            history,
            width="stretch"
        )

# -----------------------------------------------------------
# Admin Student Records
# -----------------------------------------------------------

elif menu == "👨‍🎓 Student Records":

    st.title("👨‍🎓 Student Records")

    st.markdown(
        "View registered students and their placement prediction information."
    )

    st.markdown("---")

    records = get_student_records()

    if records.empty:

        st.info("📭 No student records found.")

    else:

        st.success(
            f"Total Student Records: {len(records)}"
        )

        st.dataframe(
            records,
            width="stretch"
        )

# -----------------------------------------------------------
# About
# -----------------------------------------------------------

elif menu == "👨‍💻 About":

    st.title("👨‍💻 About CareerAI")

    st.markdown(
        """
### CareerAI

CareerAI is an AI Powered Placement Prediction System.

### Features

- Placement Prediction
- Resume Analyzer
- Machine Learning Model
- Streamlit Dashboard
- MySQL Database

### Technology

- Python
- Pandas
- Scikit-Learn
- Streamlit
- MySQL

### Developer

Aditi Sharma
"""
    )