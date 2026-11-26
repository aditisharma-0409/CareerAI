# 🎓 CareerAI

## AI Powered Placement Prediction System

CareerAI is an Artificial Intelligence based Placement Prediction System developed to help students evaluate their placement readiness.

The system predicts whether a student is likely to be placed based on academic performance and skill-related information. It also analyzes resumes, detects technical skills, identifies missing skills based on the selected job role, and provides career improvement suggestions.

---

# 🚀 Features

- 🎓 Placement Prediction using Machine Learning
- 📄 Resume Analyzer
- 🛠 Skill Detection from Resume
- 🎯 Job Role Selection
- 📚 Missing Skill Detection
- 💡 Career Recommendations
- 📊 Prediction History
- 🗄 MySQL Database Integration
- 📈 Dashboard Overview

---

# 🛠 Technologies Used

### Programming Language
- Python

### Machine Learning
- Scikit-learn
- Random Forest Classifier

### Frontend
- Streamlit

### Database
- MySQL

### Libraries
- Pandas
- NumPy
- Joblib
- PyMuPDF
- mysql-connector-python

---

# 📂 Project Structure

```
CareerAI_Project/
│
├── app/
│   └── app.py
│
├── backend/
│   ├── database
│
├── data/
│
├── ml/
│
├── resume/
│
├── saved_models/
│   └── careerai_model.pkl
│
├── README.md
├── requirements.txt
├── .gitignore
└── main.py
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/aditisharma040905-glitch/CareerAI.git
```

Go to the project folder

```bash
cd CareerAI_Project
```

Create a virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install all required libraries

```bash
pip install -r requirements.txt
```

---

# 🗄 Database Setup

Create a MySQL database.

```sql
CREATE DATABASE careerai;
```

Update your database configuration in

```
backend/database/connection.py
```

with your MySQL username and password.

Example

```python
host="localhost"
user="root"
password="your_password"
database="careerai"
```

---

# ▶ Running the Project

Run the Streamlit application

```bash
streamlit run app/app.py
```

The application will open automatically in your browser.

---

# 📊 Machine Learning Model

Model Used:

- Logistic Regression 

Input Features

- CGPA
- Internships
- Projects
- Workshops / Certifications
- Aptitude Test Score
- Soft Skills Rating
- Extracurricular Activities
- Placement Training
- SSC Marks
- HSC Marks

Output

- Placed
- Not Placed

---

# 📄 Resume Analyzer

The Resume Analyzer can

- Extract text from PDF resumes
- Detect technical skills
- Compare skills with the selected job role
- Identify missing skills
- Recommend learning areas

---

# 📸 Application Modules

- 🏠 Home Dashboard
- 🎓 Placement Prediction
- 📄 Resume Analyzer
- 📊 Prediction History
- 👨‍💻 About

---

# 🔮 Future Scope

- Resume Score Prediction
- Job Recommendation System
- Interview Question Generator
- AI Chatbot for Career Guidance
- Cloud Deployment

---

# 👩‍💻 Developer

**Aditi Sharma**

B.Tech Computer Science (Artificial Intelligence)

CareerAI was developed as a Machine Learning project to assist students in evaluating placement readiness and improving employability.

---

# ⭐ If you like this project

Please consider giving the repository a ⭐ on GitHub.