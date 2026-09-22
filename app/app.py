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
    get_student_records,
    save_resume,
    get_student_resumes,
    get_resume_by_user
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
        "CareerAI Placement Management System"
    )

    st.write(
        "Monitor student placement predictions, "
        "resume activity and overall placement performance."
    )

    st.markdown("---")

    # ------------------------------------------------------
    # Placement Statistics
    # ------------------------------------------------------

    total_predictions, placed_students, not_placed_students = (
        get_dashboard_stats()
    )

    # Calculate placement percentage
    if total_predictions > 0:

        placement_percentage = (
            placed_students / total_predictions
        ) * 100

    else:

        placement_percentage = 0

    # ------------------------------------------------------
    # Main Statistics
    # ------------------------------------------------------

    st.subheader("📊 Placement Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👨‍🎓 Total Predictions",
            total_predictions
        )

    with col2:

        st.metric(
            "🟢 Likely Placed",
            placed_students
        )

    with col3:

        st.metric(
            "🔴 Likely Not Placed",
            not_placed_students
        )

    with col4:

        st.metric(
            "📈 Placement Rate",
            f"{placement_percentage:.2f}%"
        )

    st.markdown("---")

    # ------------------------------------------------------
    # Placement Summary
    # ------------------------------------------------------

    st.subheader("📌 Placement Summary")

    if total_predictions > 0:

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Likely Placed Students:** "
                f"{placed_students}"
            )

            st.progress(
                min(
                    placed_students / total_predictions,
                    1.0
                )
            )

        with col2:

            st.write(
                f"**Likely Not Placed Students:** "
                f"{not_placed_students}"
            )

            st.progress(
                min(
                    not_placed_students / total_predictions,
                    1.0
                )
            )

    else:

        st.info(
            "📭 No placement predictions are available yet."
        )

    st.markdown("---")

    # ------------------------------------------------------
    # Student Monitoring
    # ------------------------------------------------------

    st.subheader("👨‍🎓 Student Monitoring")

    st.write(
        """
        The Admin Portal allows administrators to monitor
        student placement predictions, review student
        records and analyze uploaded resumes.
        """
    )

    st.markdown("---")

    # ------------------------------------------------------
    # Admin Functions
    # ------------------------------------------------------

    st.subheader("🛠 Admin Functions")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "👨‍🎓 **Student Records**\n\n"
            "View and monitor registered student "
            "information and placement records."
        )

    with col2:

        st.info(
            "📊 **Placement Statistics**\n\n"
            "Analyze placement prediction results "
            "and overall placement performance."
        )

    with col3:

        st.info(
            "📄 **Resume Analysis**\n\n"
            "Review student resumes, detected skills, "
            "missing skills and resume readiness."
        )

    st.markdown("---")

    # ------------------------------------------------------
    # Admin Quick Overview
    # ------------------------------------------------------

    st.subheader("⚡ Quick Overview")

    col1, col2 = st.columns(2)

    with col1:

        if total_predictions > 0:

            st.success(
                f"🟢 {placed_students} student(s) are "
                f"currently predicted as likely placed."
            )

        else:

            st.info(
                "No placement predictions available."
            )

    with col2:

        if total_predictions > 0:

            st.warning(
                f"🟡 {not_placed_students} student(s) are "
                f"currently predicted as likely not placed."
            )

        else:

            st.info(
                "No placement predictions available."
            )

    st.markdown("---")

    # ------------------------------------------------------
    # Admin Guidance
    # ------------------------------------------------------

    st.subheader("💡 Admin Guidance")

    st.write(
        """
        Use the Admin Portal to:

        • Monitor student placement predictions  
        • Review placement statistics  
        • View registered student records  
        • Analyze student resumes  
        • Identify skill gaps  
        • Monitor overall placement readiness
        """
    )



# ==========================================================
# PLACEMENT PREDICTION
# ==========================================================

elif menu == "🎓 Placement Prediction":

    st.title("🎓 Placement Prediction")

    st.write(
        "Enter the student's academic and skill details below."
    )

    st.markdown("---")

    # ------------------------------------------------------
    # Student Information
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Academic and Skill Information
    # ------------------------------------------------------

    st.subheader("📚 Academic & Skill Information")

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
            value=1,
            step=1
        )

        projects = st.number_input(
            "Projects",
            min_value=0,
            value=2,
            step=1
        )

        workshops = st.number_input(
            "Workshops / Certifications",
            min_value=0,
            value=2,
            step=1
        )

        aptitude = st.number_input(
            "Aptitude Test Score",
            min_value=0,
            max_value=100,
            value=80,
            step=1
        )

    with col2:

        softskills = st.number_input(
            "Soft Skills Rating",
            min_value=0,
            max_value=10,
            value=8,
            step=1
        )

        extracurricular = st.selectbox(
            "Extracurricular Activities",
            [
                "No",
                "Yes"
            ]
        )

        placement_training = st.selectbox(
            "Placement Training",
            [
                "No",
                "Yes"
            ]
        )

        ssc = st.number_input(
            "SSC Marks",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=0.1
        )

        hsc = st.number_input(
            "HSC Marks",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=0.1
        )

    st.markdown("---")

    # ------------------------------------------------------
    # Prediction Button
    # ------------------------------------------------------

    predict = st.button(
        "🚀 Predict Placement",
        width="stretch"
    )

    # ------------------------------------------------------
    # Prediction
    # ------------------------------------------------------

    if predict:

        # ----------------------------------------------
        # Validate Student Name
        # ----------------------------------------------

        if student_name.strip() == "":

            st.warning(
                "⚠️ Please enter the student's name."
            )

            st.stop()

        # ----------------------------------------------
        # Convert Yes / No values to numbers
        # ----------------------------------------------

        extracurricular_value = (
            1
            if extracurricular == "Yes"
            else 0
        )

        placement_training_value = (
            1
            if placement_training == "Yes"
            else 0
        )

        # ----------------------------------------------
        # Create Input DataFrame
        # ----------------------------------------------

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
                hsc
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
                "HSC_Marks"
            ]
        )

        # ----------------------------------------------
        # Make Prediction
        # ----------------------------------------------

        prediction = model.predict(
            student
        )

        probability = model.predict_proba(
            student
        )

        confidence = (
            probability.max() * 100
        )

        # ----------------------------------------------
        # Prediction Result
        # ----------------------------------------------

        prediction_result = (
            "Placed"
            if prediction[0] == 1
            else "Not Placed"
        )

        # ----------------------------------------------
        # Save Prediction
        # ----------------------------------------------

        save_prediction(
            st.session_state.user["user_id"],
            student_name,
            job_role,
            prediction_result,
            float(confidence)
        )

        # ----------------------------------------------
        # Display Result
        # ----------------------------------------------

        st.markdown("---")

        st.subheader(
            "📊 Prediction Result"
        )

        if prediction[0] == 1:

            st.success(
                "🎉 Student is Likely to be Placed"
            )

        else:

            st.error(
                "❌ Student is Likely to be Not Placed"
            )

        st.metric(
            label="Prediction Confidence",
            value=f"{confidence:.2f}%"
        )

        # ----------------------------------------------
        # Student Summary
        # ----------------------------------------------

        st.markdown("---")

        st.subheader(
            "📋 Student Summary"
        )

        summary = pd.DataFrame(
            {
                "Feature": [
                    "Student Name",
                    "Target Job Role",
                    "CGPA",
                    "Internships",
                    "Projects",
                    "Workshops / Certifications",
                    "Aptitude Test Score",
                    "Soft Skills Rating",
                    "Extracurricular Activities",
                    "Placement Training",
                    "SSC Marks",
                    "HSC Marks"
                ],
                "Value": [
                    student_name,
                    job_role,
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
            }
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------
        # Career Suggestions
        # ----------------------------------------------

        st.markdown("---")

        st.subheader(
            "💡 Career Suggestions"
        )

        suggestions = []

        if cgpa < 7.5:

            suggestions.append(
                "📚 Improve your CGPA by focusing on academics."
            )

        if internships < 2:

            suggestions.append(
                "🏢 Try to complete at least 2 internships."
            )

        if projects < 3:

            suggestions.append(
                "💻 Build more real-world projects."
            )

        if aptitude < 70:

            suggestions.append(
                "🧠 Practice aptitude and logical reasoning regularly."
            )

        if softskills < 7:

            suggestions.append(
                "🎤 Improve communication and presentation skills."
            )

        if placement_training == "No":

            suggestions.append(
                "🎯 Join placement preparation or coding training."
            )

        if len(suggestions) == 0:

            st.success(
                "🎉 Excellent Profile! Keep maintaining your performance."
            )

        else:

            for item in suggestions:

                st.write(item)

        st.markdown("---")
# -----------------------------------------------------------
# Student Resume Analyzer
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
    # ---------------------------------------
    # Prevent Duplicate Resume Saving
    # ---------------------------------------

    if "last_uploaded_resume" not in st.session_state:
        st.session_state.last_uploaded_resume = None

    if uploaded_file is not None:

        st.success("✅ Resume Uploaded Successfully!")

        # ---------------------------------------
        # Create Upload Folder
        # ---------------------------------------

        upload_folder = "uploads"

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        # ---------------------------------------
        # Save Resume File
        # ---------------------------------------

        file_path = os.path.join(
            upload_folder,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ---------------------------------------
        # Extract Resume Text
        # ---------------------------------------

        resume_text = extract_resume_text(file_path)

        st.subheader("📄 Extracted Resume Text")

        if resume_text:

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )

            # ---------------------------------------
            # Detect Skills
            # ---------------------------------------

            skills = extract_skills(resume_text)

            st.subheader("🛠 Detected Skills")

            if len(skills) > 0:

                for skill in skills:
                    st.success(f"✅ {skill}")

            else:

                st.warning(
                    "No known skills were detected."
                )

            # ---------------------------------------
            # Missing Skills
            # ---------------------------------------

            missing_skills = recommend_skills(
                skills,
                job_role
            )

            st.subheader(
                f"📚 Missing Skills for {job_role}"
            )

            if len(missing_skills) > 0:

                for skill in missing_skills:

                    st.error(
                        f"❌ {skill}"
                    )

                    recommendation = get_learning_path(
                        skill
                    )

                    st.info(
                        f"📖 Recommendation: {recommendation}"
                    )

            else:

                st.success(
                    "🎉 Excellent! You already have "
                    "all the required skills for this role."
                )

            # ---------------------------------------
            # Resume Score
            # ---------------------------------------

            total_skills = len(skills)
            missing_count = len(missing_skills)

            if total_skills + missing_count > 0:

                resume_score = (
                    total_skills
                    /
                    (total_skills + missing_count)
                ) * 100

            else:

                resume_score = 0

            st.markdown("---")

            st.subheader("📊 Resume Readiness")

            st.metric(
                "Resume Score",
                f"{resume_score:.2f}/100"
            )

            # ---------------------------------------
            # Resume Status
            # ---------------------------------------

            if resume_score >= 70:

                resume_status = "Resume Ready"

                st.success(
                    "🟢 Resume is Ready for the selected job role."
                )

            else:

                resume_status = "Needs Improvement"

                st.warning(
                    "🟡 Resume needs improvement for the selected job role."
                )

            # ---------------------------------------
            # Save Resume Information
            # ---------------------------------------

            user_id = st.session_state.user["user_id"]

            resume_key = (
                str(user_id)
                + "_"
                + uploaded_file.name
            )

            if (
                st.session_state.last_uploaded_resume
                != resume_key
            ):

                save_resume(
                    user_id,
                    uploaded_file.name,
                    file_path,
                    job_role,
                    float(resume_score),
                    resume_status,
                    skills,
                    missing_skills
                )

                st.session_state.last_uploaded_resume = resume_key

                st.success(
                    "💾 Resume analysis saved successfully!"
                )
        else:

            st.error(
                "❌ Unable to read the resume."
            )
# -----------------------------------------------------------
# Prediction History
# -----------------------------------------------------------

elif menu == "📊 My Prediction History":

    st.title("📊 My Prediction History")

    user_id = st.session_state.user["user_id"]

    history = get_prediction_history(user_id)

    if history.empty:

        st.info(
            "📭 You have not made any predictions yet."
        )

    else:

        st.success(
            f"Total Predictions: {len(history)}"
        )

        # --------------------------------------------------
        # Format Confidence
        # --------------------------------------------------

        if "Confidence (%)" in history.columns:

            history["Confidence (%)"] = pd.to_numeric(
                history["Confidence (%)"],
                errors="coerce"
            )

            history["Confidence (%)"] = history[
                "Confidence (%)"
            ].apply(
                lambda x:
                f"{x:.2f}%"
                if pd.notna(x)
                else "N/A"
            )

        # --------------------------------------------------
        # Display Prediction History
        # --------------------------------------------------

        st.dataframe(
            history,
            width="stretch",
            hide_index=True
        )
# ==========================================================
# STUDENT RECORDS
# ==========================================================

elif menu == "👨‍🎓 Student Records":

    st.title("👨‍🎓 Student Records")

    st.write(
        "View registered students and their placement "
        "prediction information."
    )

    st.markdown("---")

    # ------------------------------------------------------
    # Fetch Student Records
    # ------------------------------------------------------

    records = get_student_records()

    if records.empty:

        st.info(
            "📭 No student records found."
        )

    else:

        # --------------------------------------------------
        # Overview
        # --------------------------------------------------

        st.subheader("📊 Student Overview")

        total_students = len(records)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "👨‍🎓 Total Records",
                total_students
            )

        with col2:

            placed_count = (
                records["Prediction"]
                .astype(str)
                .str.lower()
                .eq("placed")
                .sum()
            )

            st.metric(
                "🟢 Likely Placed",
                int(placed_count)
            )

        with col3:

            not_placed_count = (
                records["Prediction"]
                .astype(str)
                .str.lower()
                .eq("not placed")
                .sum()
            )

            st.metric(
                "🔴 Likely Not Placed",
                int(not_placed_count)
            )

        st.markdown("---")

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        st.subheader("🔎 Search Students")

        search_text = st.text_input(
            "Search by student name or email",
            placeholder="Enter student name or email..."
        )

        filtered_records = records.copy()

        if search_text:

            search_text = search_text.strip().lower()

            name_match = (
                filtered_records["Student Name"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    na=False
                )
            )

            email_match = (
                filtered_records["Email"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_text,
                    na=False
                )
            )

            filtered_records = filtered_records[
                name_match | email_match
            ]

        # --------------------------------------------------
        # Filters
        # --------------------------------------------------

        st.subheader("🎯 Filters")

        col1, col2 = st.columns(2)

        with col1:

            prediction_filter = st.selectbox(
                "Placement Prediction",
                [
                    "All",
                    "Placed",
                    "Not Placed"
                ]
            )

        with col2:

            job_roles = [
                "All"
            ]

            if "Target Job Role" in records.columns:

                available_roles = (
                    records["Target Job Role"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                available_roles.sort()

                job_roles.extend(
                    available_roles
                )

            job_role_filter = st.selectbox(
                "Target Job Role",
                job_roles
            )

        # --------------------------------------------------
        # Apply Prediction Filter
        # --------------------------------------------------

        if prediction_filter != "All":

            filtered_records = filtered_records[
                filtered_records["Prediction"]
                .astype(str)
                .str.lower()
                ==
                prediction_filter.lower()
            ]

        # --------------------------------------------------
        # Apply Job Role Filter
        # --------------------------------------------------

        if job_role_filter != "All":

            filtered_records = filtered_records[
                filtered_records["Target Job Role"]
                .astype(str)
                ==
                job_role_filter
            ]

        st.markdown("---")

        # --------------------------------------------------
        # Filter Result
        # --------------------------------------------------

        st.write(
            f"**Students found:** "
            f"{len(filtered_records)}"
        )

        # --------------------------------------------------
        # Student Table
        # --------------------------------------------------

        if filtered_records.empty:

            st.warning(
                "No students found matching the selected filters."
            )

        else:

            st.subheader("👨‍🎓 Student List")

            # Show only important columns
            display_columns = [
                "User ID",
                "Student Name",
                "Email",
                "Target Job Role",
                "Prediction",
                "Confidence (%)",
                "Date & Time"
            ]

            available_columns = [
                column
                for column in display_columns
                if column in filtered_records.columns
            ]

            student_table = filtered_records[
                available_columns
            ].copy()

            st.dataframe(
                student_table,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # Reset Filters
        # --------------------------------------------------

        st.markdown("---")

        st.caption(
            "💡 Resume details and individual resume analysis "
            "are available separately under Resume Analysis."
        )
# -----------------------------------------------------------
# Admin - Resume Analysis
# -----------------------------------------------------------

elif menu == "📄 Resume Analysis":

    st.title("📄 Student Resume Analysis")

    st.write(
        "View and analyze resumes uploaded by students."
    )

    # ---------------------------------------
    # Fetch Resume Records
    # ---------------------------------------

    resume_df = get_student_resumes()

    if resume_df.empty:

        st.info(
            "📭 No student resumes have been uploaded yet."
        )

    else:

        # ---------------------------------------
        # Search Student
        # ---------------------------------------

        st.subheader("🔎 Search Students")

        search_text = st.text_input(
            "Search by student name or email",
            placeholder="Enter student name or email..."
        )

        # ---------------------------------------
        # Filter Records
        # ---------------------------------------

        filtered_df = resume_df.copy()

        if search_text:

            search_text = search_text.lower()

            filtered_df = filtered_df[
                filtered_df["Student Name"]
                .str.lower()
                .str.contains(
                    search_text,
                    na=False
                )
                |
                filtered_df["Email"]
                .str.lower()
                .str.contains(
                    search_text,
                    na=False
                )
            ]

        # ---------------------------------------
        # Student Count
        # ---------------------------------------

        st.write(
            f"**Students found:** {len(filtered_df)}"
        )

        if filtered_df.empty:

            st.warning(
                "No students found matching your search."
            )

        else:

            # ---------------------------------------
            # Student Table
            # ---------------------------------------

            st.subheader("👨‍🎓 Student Resumes")

            display_df = filtered_df[
                [
                    "Resume ID",
                    "Student Name",
                    "Email",
                    "Target Job Role",
                    "Resume Score",
                    "Resume Status",
                    "Uploaded At"
                ]
            ].copy()

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            # ---------------------------------------
            # Select Student for Detailed Analysis
            # ---------------------------------------

            st.subheader(
                "📋 View Detailed Resume Analysis"
            )

            student_options = (
                filtered_df["Resume ID"]
                .astype(str)
                + " - "
                + filtered_df["Student Name"]
                + " - "
                + filtered_df["Email"]
            ).tolist()

            selected_student = st.selectbox(
                "Select Resume",
                student_options
            )

            selected_index = student_options.index(
                selected_student
            )

            selected_resume = filtered_df.iloc[
                selected_index
            ]

            st.markdown("---")

            # ---------------------------------------
            # Student Information
            # ---------------------------------------

            st.subheader("👤 Student Information")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Student Name:** "
                    f"{selected_resume['Student Name']}"
                )

                st.write(
                    f"**Email:** "
                    f"{selected_resume['Email']}"
                )

                st.write(
                    f"**User ID:** "
                    f"{selected_resume['User ID']}"
                )

            with col2:

                st.write(
                    f"**Target Job Role:** "
                    f"{selected_resume['Target Job Role']}"
                )

                st.write(
                    f"**Resume File:** "
                    f"{selected_resume['File Name']}"
                )

                st.write(
                    f"**Uploaded At:** "
                    f"{selected_resume['Uploaded At']}"
                )

            st.markdown("---")

            # ---------------------------------------
            # Resume Score & Status
            # ---------------------------------------

            st.subheader("📊 Resume Readiness")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Resume Score",
                    f"{float(selected_resume['Resume Score']):.2f}/100"
                )

            with col2:

                if (
                    selected_resume["Resume Status"]
                    == "Resume Ready"
                ):

                    st.success(
                        "🟢 Resume Ready"
                    )

                else:

                    st.warning(
                        "🟡 Needs Improvement"
                    )

            st.markdown("---")

            # ---------------------------------------
            # Detected Skills
            # ---------------------------------------

            st.subheader("🛠 Detected Skills")

            detected_skills = selected_resume[
                "Detected Skills"
            ]

            if (
                isinstance(detected_skills, str)
                and detected_skills.strip()
            ):

                skills = [
                    skill.strip()
                    for skill in detected_skills.split(",")
                    if skill.strip()
                ]

                for skill in skills:

                    st.success(
                        f"✅ {skill}"
                    )

            else:

                st.warning(
                    "No detected skills available."
                )

            # ---------------------------------------
            # Missing Skills
            # ---------------------------------------

            st.subheader("📚 Missing Skills")

            missing_skills = selected_resume[
                "Missing Skills"
            ]

            if (
                isinstance(missing_skills, str)
                and missing_skills.strip()
            ):

                skills = [
                    skill.strip()
                    for skill in missing_skills.split(",")
                    if skill.strip()
                ]

                for skill in skills:

                    st.error(
                        f"❌ {skill}"
                    )

            else:

                st.success(
                    "🎉 No missing skills identified."
                )

            st.markdown("---")

            # ---------------------------------------
            # Download Resume
            # ---------------------------------------

            st.subheader("📄 Resume File")

            resume_data = get_resume_by_user(
                int(selected_resume["User ID"])
            )

            if resume_data:

                resume_file_path = resume_data[2]

                if os.path.exists(resume_file_path):

                    with open(
                        resume_file_path,
                        "rb"
                    ) as file:

                        resume_bytes = file.read()

                    st.download_button(
                        label="⬇️ Download Resume",
                        data=resume_bytes,
                        file_name=selected_resume["File Name"],
                        mime="application/pdf"
                    )

                else:

                    st.warning(
                        "⚠️ Resume file could not be found."
                    )

            else:

                st.warning(
                    "⚠️ Resume information not found."
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