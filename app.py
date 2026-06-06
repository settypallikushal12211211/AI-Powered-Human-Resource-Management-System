import streamlit as st
import sqlite3
from datetime import date
from streamlit_mic_recorder import mic_recorder

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="AI HRMS",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------
# Session State
# ----------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "selected_candidate" not in st.session_state:
    st.session_state.selected_candidate = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "applications" not in st.session_state:
    st.session_state.applications = []

if "logged_in_email" not in st.session_state:
    st.session_state.logged_in_email = ""

if "show_delete_popup" not in st.session_state:
    st.session_state.show_delete_popup = False

if "delete_candidate" not in st.session_state:
    st.session_state.delete_candidate = None

if "employee_email" not in st.session_state:
    st.session_state.employee_email = ""

#-----------------------------------
#database
#------------------------------------
def create_database():

    conn = sqlite3.connect("recruitment.db")

    cursor = conn.cursor()

    # Applications Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        company TEXT,
        role TEXT,
        resume TEXT,
        status TEXT,
        resume_score INTEGER,
        interview_score INTEGER,
        final_score INTEGER,
        hr_email TEXT
    )
    """)

    # Applicants Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applicants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
    """)

    # Employees Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        employment_type TEXT,
        password TEXT
    )
    """)

    # AI Interview Table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_email TEXT,
        answer_1 TEXT,
        answer_2 TEXT,
        answer_3 TEXT,
        answer_4 TEXT,
        ai_score INTEGER,
        ai_feedback TEXT,
        status TEXT
    )
    """)

    # attendence

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_email TEXT,
        attendance_date TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_email TEXT,
        performance_score INTEGER,
        remarks TEXT
        )
        """)

    conn.commit()

    conn.close()


create_database()
# ----------------------------------
# Home Page
# ----------------------------------

def home_page():

    st.title(
        "🤖 AI Powered Human Resource Management System"
    )

    st.subheader(
        "Build the Future of HR Management with AI"
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📄 Resumes",
            "500+"
        )

    with col2:

        st.metric(
            "🎯 AI Accuracy",
            "92%"
        )

    with col3:

        st.metric(
            "💼 Active Jobs",
            "50+"
        )

    with col4:

        st.metric(
            "👥 Employees",
            "1000+"
        )

    st.markdown("---")

    st.subheader(
        "🚀 Platform Modules"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            "🤖 AI Resume Screening"
        )

        st.success(
            "🎤 AI Interview Assessment"
        )

        st.success(
            "🏆 Candidate Ranking"
        )

        st.success(
            "👨‍💼 HR Recruiter Portal"
        )

    with col2:

        st.success(
            "🏢 Management Admin Dashboard"
        )

        st.success(
            "📅 Attendance Management"
        )

        st.success(
            "💰 Payroll Management"
        )

        st.success(
            "⭐ Performance Tracking"
        )

    st.markdown("---")

    st.subheader(
        "👥 User Roles"
    )

    st.info(
        "Management Admin • Senior Manager • HR Recruiter • Employee • Applicant"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "👨‍🎓 Applicant Portal",
            use_container_width=True
        ):

            st.session_state.page = (
                "applicant_portal"
            )

            st.rerun()

    with col2:

        if st.button(
            "👨‍💼 Employee Portal",
            use_container_width=True
        ):

            st.session_state.page = (
                "employee_portal"
            )

            st.rerun()

    st.markdown("---")

    st.success(
        "AI Recommends • Human Decides"
    )

#-----------------------------------
#Applican portal
#-----------------------------------
def applicant_portal_page():

    st.title("👨‍🎓 Applicant Portal")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = "applicant_login"
            st.rerun()

    with col2:
        if st.button("📝 Create Account", use_container_width=True):
            st.session_state.page = "applicant_signup"
            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()
# ----------------------------------
# login page applicant
# ----------------------------------
def applicant_login_page():

    st.title("🔐 Applicant Login")

    st.markdown("---")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM applicants
            WHERE email = ?
            AND password = ?
            """,
            (
                email,
                password
            )
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            st.session_state.logged_in_email = email

            st.success(
                "Login Successful"
            )

            st.session_state.page = (
                "applicant_dashboard"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Email or Password"
            )

    if st.button("⬅ Back"):

        st.session_state.page = (
            "applicant_portal"
        )

        st.rerun()
# ----------------------------------
# signup page applicant
# ----------------------------------

def applicant_signup_page():

    st.title("📝 Create Applicant Account")

    st.markdown("---")

    first_name = st.text_input("First Name")

    last_name = st.text_input("Last Name")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    email = st.text_input("Email")

    phone = st.text_input("Phone Number")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if "@" not in email:

            st.error("Enter valid email")

        elif not phone.isdigit():

            st.error(
                "Phone number should contain only numbers"
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match"
            )

        else:

            conn = sqlite3.connect(
                "recruitment.db"
            )

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO applicants
                    (
                        first_name,
                        last_name,
                        gender,
                        email,
                        phone,
                        password
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        first_name,
                        last_name,
                        gender,
                        email,
                        phone,
                        password
                    )
                )

                conn.commit()

                st.success(
                    "Account Created Successfully"
                )

                st.session_state.page = (
                    "applicant_login"
                )

                st.rerun()

            except sqlite3.IntegrityError:

                st.error(
                    "Email already registered"
                )

            conn.close()

    if st.button("⬅ Back"):

        st.session_state.page = (
            "applicant_portal"
        )

        st.rerun()
# ----------------------------------
# Employee Portal Page
# ----------------------------------      

def employee_portal_page():

    st.title("👨‍💼 Employee Portal")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 Employee Login",
                     use_container_width=True):

            st.session_state.page = "employee_login"
            st.rerun()

    with col2:
        if st.button("📝 Create Employee Account",
                     use_container_width=True):

            st.session_state.page = "employee_signup"
            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()


# ----------------------------------
# Employee Login Page
# ----------------------------------
def employee_login_page():

    st.title("🔐 Employee Login")

    st.markdown("---")

    email = st.text_input(
        "Official Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM employees
            WHERE email = ?
            AND password = ?
            """,
            (
                email,
                password
            )
        )

        employee = cursor.fetchone()

        conn.close()

        if employee:

            st.session_state.employee_email = email

            st.success(
                "Login Successful"
            )

            role = employee[4]

            if role == "Management Admin":

                st.session_state.page = (
                    "admin_dashboard"
                )

            elif role == "Senior Manager":

                st.session_state.page = (
                    "manager_dashboard"
                )

            elif role == "HR Recruiter":

                st.session_state.page = (
                    "hr_dashboard"
                )

            else:

                st.session_state.page = (
                    "employee_dashboard"
                )

            st.rerun()

        else:

            st.error(
                "Invalid Email or Password"
            )

    if st.button("⬅ Back"):

        st.session_state.page = (
            "employee_portal"
        )

        st.rerun()


# ----------------------------------
# Employee Signup Page
# ----------------------------------
def employee_signup_page():

    st.title("📝 Create Employee Account")

    st.markdown("---")

    first_name = st.text_input("First Name")

    last_name = st.text_input("Last Name")

    email = st.text_input("Official Email")

    employment_type = st.selectbox(
        "Employment Type",
        [
            "Management Admin",
            "Senior Manager",
            "HR Recruiter",
            "Employee"
        ]
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Create Account"):

        if "@" not in email:

            st.error("Enter valid email")

        elif password != confirm_password:

            st.error("Passwords do not match")

        else:

            conn = sqlite3.connect(
                
                "recruitment.db"
        )

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO employees
                    (
                        first_name,
                        last_name,
                        email,
                        employment_type,
                        password
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                  (
                        first_name,
                        last_name,
                        email,
                        employment_type,
                        password
                )
            )

                conn.commit()

                st.success(
                    "Employee Account Created Successfully"
            )

                st.session_state.page = (
                    "employee_login"
            )

                st.rerun()

            except sqlite3.IntegrityError:

                st.error(
                    "Email already registered"
            )

            conn.close()

    if st.button("⬅ Back"):
        st.session_state.page = "employee_portal"
        st.rerun()


# ----------------------------------
# Jobs Page
# ----------------------------------

def jobs_page():

    st.title("💼 Available Jobs")

    jobs = [

        {
            "company": "Microsoft",
            "role": "Software Engineer",
            "location": "Hyderabad",
            "ctc": "8-12 LPA"
        },

        {
            "company": "Google",
            "role": "Data Analyst",
            "location": "Bangalore",
            "ctc": "10-15 LPA"
        },

        {
            "company": "Infosys",
            "role": "AI Engineer",
            "location": "Pune",
            "ctc": "6-8 LPA"
        }

    ]

    for job in jobs:

        st.markdown("---")

        st.subheader(f"🏢 {job['company']}")

        st.write(f"**Role:** {job['role']}")

        st.write(f"📍 Location: {job['location']}")

        st.write(f"💰 CTC: {job['ctc']}")

        if st.button(
            f"View Details - {job['company']}",
            key=job["company"]
        ):

            st.session_state.selected_job = job
            st.session_state.page = "job_details"
            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ----------------------------------
# Job Details Page
# ----------------------------------

def job_details_page():

    job = st.session_state.selected_job

    st.title(f"🏢 {job['company']}")

    st.subheader(job["role"])

    st.markdown("---")

    st.write(f"📍 Location: {job['location']}")

    st.write(f"💰 CTC: {job['ctc']}")

    st.markdown("---")

    st.subheader("Required Skills")

    st.write("✔ Python")
    st.write("✔ SQL")
    st.write("✔ Machine Learning")

    st.markdown("---")

    st.subheader("Job Description")

    st.write(
        "We are looking for passionate candidates who can work on modern AI and software solutions."
    )

    st.markdown("---")

    if st.button("🚀 Apply Now"):
       st.session_state.page = "questions"
       st.rerun()

    if st.button("⬅ Back to Jobs"):
        st.session_state.page = "jobs"
        st.rerun()

def screening_questions_page():

    st.title("📝 Screening Questions")

    st.markdown("---")

    relocate = st.radio(
        "Are you ready to relocate?",
        ["Yes", "No"]
    )

    bond = st.radio(
        "Are you ready for 1 year bond?",
        ["Yes", "No"]
    )

    resume_jd = st.radio(
        "Have you re-structured your resume according to the company's JD?",
        ["Yes", "No"]
    )

    ctc = st.text_input(
        "Last Drawn CTC (If not applicable enter NA)"
    )

    joining = st.selectbox(
        "How soon can you join the company?",
        [
            "Immediate Available",
            "0-15 Days",
            "15-45 Days",
            "More than 45 Days"
        ]
    )

    st.markdown("---")

    if st.button("Continue to Resume Upload"):

        st.session_state.answers = {
            "relocate": relocate,
            "bond": bond,
            "resume_jd": resume_jd,
            "ctc": ctc,
            "joining": joining
        }

        st.session_state.page = "resume_upload"
        st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "job_details"
        st.rerun()
#-----------------------------
#Upload resume
#-----------------------------
def resume_upload_page():

    st.title("📄 Upload Resume")

    st.markdown("---")

    name = st.text_input("Full Name")

    email = st.session_state.logged_in_email

    st.write(f"📧 Email : {email}")

    phone = st.text_input("Phone Number")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["txt"]
    )

    resume_text = ""

    if uploaded_file is not None:

        resume_text = uploaded_file.getvalue().decode("utf-8")

        st.subheader("📋 Resume Preview")

        st.text_area(
            "Resume Content",
            resume_text,
            height=250
        )

    st.markdown("---")

    if st.button("Submit Application"):

        if not name:

            st.error("Please enter name")

        elif not email:

            st.error("Please enter email")

        elif uploaded_file is None:

            st.error("Please upload resume")

        else:

            st.session_state.resume_text = resume_text

            st.session_state.applications.append(
                {
                    "name": name,
                    "email": email,
                    "role": st.session_state.selected_job["role"],
                    "company": st.session_state.selected_job["company"],
                    "resume": resume_text,
                    "status": "Under Review",
                    "score": 0
            

                }
            )

            # Save to SQLite

            conn = sqlite3.connect("recruitment.db")

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO applications
                (
                    name,
                    email,
                    company,
                    role,
                    resume,
                    status,
                    resume_score,
                    interview_score,
                    final_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    st.session_state.selected_job["company"],
                    st.session_state.selected_job["role"],
                    resume_text,
                    "Under Review",
                    0,
                    0,
                    0
                )
            )

            conn.commit()

            conn.close()

            st.session_state.page = "thank_you"

            st.rerun()

    if st.button("⬅ Back"):

        st.session_state.page = "questions"

        st.rerun()
#----------------------------------
#Analysis
#----------------------------------
def analysis_page():

    st.title("🤖 AI Candidate Analysis")

    st.markdown("---")

    resume = st.session_state.resume_text

    # Required Skills
    job_skills = [
        "Python",
        "SQL",
        "Machine Learning"
    ]

    matched_skills = []

    for skill in job_skills:

        if skill.lower() in resume.lower():

            matched_skills.append(skill)

    skills_score = (
        len(matched_skills)
        / len(job_skills)
    ) * 100

    # -----------------------------
    # Project Detection
    # -----------------------------

    project_keywords = [
        "project",
        "developed",
        "built",
        "created"
    ]

    project_count = 0

    for word in project_keywords:

        if word.lower() in resume.lower():

            project_count += 1

    projects_score = min(project_count * 25, 100)

    # -----------------------------
    # Experience Detection
    # -----------------------------

    experience_keywords = [
        "intern",
        "experience",
        "worked",
        "employment"
    ]

    experience_count = 0

    for word in experience_keywords:

        if word.lower() in resume.lower():

            experience_count += 1

    experience_score = min(experience_count * 25, 100)

    # -----------------------------
    # Certificate Detection
    # -----------------------------

    certificate_keywords = [
        "certificate",
        "certification",
        "coursera",
        "udemy",
        "google"
    ]

    certificate_count = 0

    for word in certificate_keywords:

        if word.lower() in resume.lower():

            certificate_count += 1

    certificates_score = min(
        certificate_count * 20,
        100
    )

    # -----------------------------
    # Questions Score
    # -----------------------------

    questions_score = 100

    # -----------------------------
    # Final Score
    # -----------------------------

    final_score = (
        (projects_score * 0.40)
        + (experience_score * 0.25)
        + (skills_score * 0.15)
        + (certificates_score * 0.10)
        + (questions_score * 0.10)
    )
    
    resume_score = round(final_score)

    conn = sqlite3.connect(
        "recruitment.db"
)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET resume_score = ?
        WHERE email = ?
        """,
    (
           resume_score,
           st.session_state.logged_in_email
    )
)

    conn.commit()

    conn.close()


    st.subheader("Final AI Score")

    st.success(f"{final_score:.0f}%")

    st.markdown("---")

    st.subheader("Matched Skills")

    if matched_skills:

        for skill in matched_skills:

            st.write(f"✅ {skill}")

    else:

        st.write("No matching skills found")

    st.markdown("---")

    st.write(f"📁 Projects Score : {projects_score}")

    st.write(f"💼 Experience Score : {experience_score}")

    st.write(f"🛠 Skills Score : {skills_score:.0f}")

    st.write(f"📜 Certificates Score : {certificates_score}")

    st.write(f"❓ Screening Questions Score : {questions_score}")

    st.markdown("---")

    st.subheader("Why Shortlisted")

    reasons = []

    if len(matched_skills) > 0:
        reasons.append(
            f"Matched {len(matched_skills)} required skills."
        )

    if projects_score > 0:
        reasons.append(
            "Relevant projects detected in resume."
        )

    if experience_score > 0:
        reasons.append(
            "Relevant experience detected."
        )

    if certificates_score > 0:
        reasons.append(
            "Certifications found."
        )

    reasons.append(
        "Screening questions completed."
    )

    st.success("\n\n".join(reasons))

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("✅ Shortlist"):

            st.success(
                "Candidate Shortlisted"
            )

    with col2:

        if st.button("⏳ Hold"):

            st.warning(
                "Candidate On Hold"
            )

    with col3:

        if st.button("❌ Reject"):

            st.error(
                "Candidate Rejected"
            )

    st.markdown("---")

    if st.button("⬅ Back to Home"):

        st.session_state.page = "home"

        st.rerun()

#----------------------------
#Management Admin Dashboard
#----------------------------
def admin_dashboard_page():

    st.title("🏢 Management Admin Dashboard")

    st.markdown("---")

    conn = sqlite3.connect(
        "recruitment.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applicants"
    )

    total_applicants = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM employees"
    )

    total_employees = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM interviews"
    )

    total_interviews = cursor.fetchone()[0]

    conn.close()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Applicants",
            total_applicants
        )

    with col2:

        st.metric(
            "Employees",
            total_employees
        )

    with col3:

        st.metric(
            "AI Interviews",
            total_interviews
        )

    st.markdown("---")

    st.subheader(
        "📈 Company Overview"
    )

    st.success(
        "AI Recruitment System Active"
    )

    st.info(
        "Employee Management Module Available"
    )

    st.info(
        "Attendance Module Available"
    )

    st.info(
        "Payroll Module Available"
    )

    st.markdown("---")

    if st.button(
        "👨‍💼 View Employees"
    ):

        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            first_name,
            last_name,
            email,
            employment_type
            FROM employees
            """
        )

        employees = cursor.fetchall()

        conn.close()

        st.dataframe(
            employees
        )

    if st.button(
        "🧑‍💻 View Applicants"
    ):

        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            first_name,
            last_name,
            email,
            phone
            FROM applicants
            """
        )

        applicants = cursor.fetchall()

        conn.close()

        st.dataframe(
            applicants
        )

    if st.button(
        "📅 View Attendance"
    ):
   
        
        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM attendance
            """
        )

        attendance = cursor.fetchall()

        conn.close()

        st.dataframe(
            attendance
        )

    st.markdown("---")

    st.subheader(
        "🗑 Delete Employee"
)

    employee_email = st.text_input(
        "Enter Employee Email"
)

    if st.button(
        "Delete Employee"
    ):

        conn = sqlite3.connect(
            "recruitment.db"
    )

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM employees
            WHERE email = ?
            """,
        (
                employee_email,
        )
    )

        conn.commit()

        conn.close()

        st.success(
            "Employee Deleted Successfully"
    )

    st.markdown("---")
    
    if st.button(
        "🚪 Logout"
    ):

        st.session_state.page = (
            "home"
        )

        st.rerun()
#----------------------------
#attendence page
#----------------------------
def attendance_page():

    st.title("📅 Attendance")

    st.markdown("---")

    st.write(
        "Today's Status"
    )

    status = st.selectbox(
        "Mark Attendance",
        [
            "Present",
            "Absent",
            "Late"
        ]
    )

    if st.button(
        "Save Attendance"
    ):

        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO attendance
            (
                employee_email,
                attendance_date,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                st.session_state.employee_email,
                str(date.today()),
                status
            )
        )

        conn.commit()

        conn.close()

        st.success(
            "Attendance Saved Successfully"
        )

    conn = sqlite3.connect(
        "recruitment.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        attendance_date,
        status
        FROM attendance
        WHERE employee_email = ?
        ORDER BY id DESC
        """,
        (
            st.session_state.employee_email,
        )
    )

    records = cursor.fetchall()

    conn.close()

    st.markdown("---")

    st.subheader(
        "📋 My Attendance History"
    )

    if len(records) > 0:

        st.dataframe(
            records
        )

    else:

        st.info(
            "No attendance records found."
        )

    st.markdown("---")

    if st.button(
        "⬅ Back"
    ):

        st.session_state.page = (
            "employee_dashboard"
        )

        st.rerun()

#-------------------------------
#payroll page
#-------------------------------

def payroll_page():

    st.title("💰 Payroll")

    st.markdown("---")

    st.write(
        "Basic Salary : ₹50,000"
    )

    st.write(
        "Bonus : ₹5,000"
    )

    st.success(
        "Net Salary : ₹55,000"
    )

    if st.button(
        "⬅ Back"
    ):

        st.session_state.page = (
            "employee_dashboard"
        )

        st.rerun()


#----------------------------
#Senior Manager Dashboard
#----------------------------
def manager_dashboard_page():

    st.title("📊 Senior Manager Dashboard")

    st.markdown("---")

    conn = sqlite3.connect(
        "recruitment.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM applications
        WHERE status='Selected'
        """
    )

    selected = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM applications
        WHERE status='Rejected'
        """
    )

    rejected = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM applications
        WHERE status='Under Review'
        """
    )

    review = cursor.fetchone()[0]

    conn.close()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Selected",
            selected
        )

    with col2:

        st.metric(
            "Rejected",
            rejected
        )

    with col3:

        st.metric(
            "Under Review",
            review
        )

    st.markdown("---")

    st.success(
        "Recruitment Analytics Dashboard"
    )

    if st.button(
        "🚪 Logout"
    ):

        st.session_state.page = "home"

        st.rerun()

#----------------------------
# Performance page
#----------------------------

def performance_page():

    st.title("⭐ Performance Tracking")

    st.markdown("---")

    st.write(
        "Performance Score : 85"
    )

    st.progress(85)

    st.success(
        "Rating : Excellent"
    )

    st.info(
        "Remarks : Consistent Performer"
    )

    if st.button(
        "⬅ Back"
    ):

        st.session_state.page = (
            "employee_dashboard"
        )

        st.rerun()

#----------------------------
#Employee Dashboard
#----------------------------
def employee_dashboard_page():

    st.title("👨‍💻 Employee Dashboard")

    st.markdown("---")

    st.subheader(
        "Welcome Employee"
    )

    st.success(
        f"Logged In : {st.session_state.employee_email}"
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📅 Attendance"
        ):

            st.session_state.page = (
                "attendance"
            )

            st.rerun()

    with col2:

        if st.button(
            "💰 Payroll"
        ):

            st.session_state.page = (
                "payroll"
            )

            st.rerun()

    with col3:

        if st.button(
            "⭐ Performance"
        ):

            st.session_state.page = (
                "performance"
            )

            st.rerun()

    st.markdown("---")

    st.subheader(
        "📊 Employee Summary"
    )

    st.metric(
        "Performance Score",
        "85%"
    )

    st.progress(85)

    st.success(
        "Performance Rating : Excellent"
    )

    st.info(
        "Attendance, Payroll and Performance data are available through the dashboard."
    )

    st.markdown("---")

    if st.button(
        "🚪 Logout"
    ):

        st.session_state.page = (
            "home"
        )

        st.rerun()
#----------------------------
#Hr dash board
#----------------------------
def hr_dashboard_page():

    st.title("👨‍💼 HR Dashboard")

    st.markdown("---")

    st.subheader("Applied Candidates")

    conn = sqlite3.connect("recruitment.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        name,
        email,
        company,
        role,
        resume,
        status,
        resume_score,
        interview_score,
        final_score
        FROM applications
        """
    )

    rows = cursor.fetchall()

    conn.close()

    applications = []

    for row in rows:

        applications.append(
            {
                "name": row[0],
                "email": row[1],
                "company": row[2],
                "role": row[3],
                "resume": row[4],
                "status": row[5],
                "resume_score": row[6],
                "interview_score": row[7],
                "final_score": row[8]
            }
        )

    applications = sorted(
        applications,
        key=lambda x: x["final_score"],
        reverse=True
    )

    if len(applications) == 0:

        st.info(
            "No applications received yet."
        )

    else:

        st.success(
            f"🏆 Top Ranked Candidate: {applications[0]['name']} ({applications[0]['final_score']}%)"
        )

        st.markdown("---")

        for i, app in enumerate(applications):

            st.write(
                f"👤 {app['name']} | {app['company']} | {app['role']} | 🎯 {app['final_score']}%"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    f"View Profile - {app['name']}",
                    key=f"profile_{i}"
                ):

                    st.session_state.selected_candidate = app

                    st.session_state.page = (
                        "candidate_profile"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    f"🗑 Delete - {app['name']}",
                    key=f"delete_{i}"
                ):

                    st.session_state.delete_candidate = app

                    st.session_state.show_delete_popup = True

                    st.rerun()

            st.markdown("---")

    if (
        "show_delete_popup" in st.session_state
        and st.session_state.show_delete_popup
    ):

        candidate = (
            st.session_state.delete_candidate
        )

        st.warning(
            f"⚠ Are you sure you want to delete {candidate['name']}?"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✅ Yes Delete"
            ):

                conn = sqlite3.connect(
                    "recruitment.db"
                )

                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM applications
                    WHERE email = ?
                    """,
                    (
                        candidate["email"],
                    )
                )

                cursor.execute(
                    """
                    DELETE FROM interviews
                    WHERE candidate_email = ?
                    """,
                    (
                        candidate["email"],
                    )
                )

                conn.commit()

                conn.close()

                st.session_state.show_delete_popup = False

                st.success(
                    "Candidate Deleted Successfully"
                )

                st.rerun()

        with col2:

            if st.button(
                "❌ Cancel"
            ):

                st.session_state.show_delete_popup = False

                st.rerun()

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.page = "home"

        st.rerun()

    if st.button("⬅ Back to Home"):

        st.session_state.page = "home"

        st.rerun()

#------------------------
#Candidate profile
#------------------------
def candidate_profile_page():

    candidate = st.session_state.selected_candidate

    st.title(f"👤 {candidate['name']}")

    st.markdown("---")

    st.write(f"🏢 Company : {candidate['company']}")

    st.write(f"💼 Applied Role : {candidate['role']}")

    st.write(f"📧 Email : {candidate['email']}")

    st.write(f"📊 Current Status : {candidate['status']}")

    st.write("📄 Resume Status : Uploaded")

    st.write("📝 Questions Status : Completed")

    st.markdown("---")

    st.subheader("Resume Preview")

    st.text_area(
        "Resume Content",
        candidate["resume"],
        height=250
    )

    st.markdown("---")

    st.subheader("Interview Pipeline")

    st.write("✅ Resume Screening")

    st.write("⏳ AI HR Interview")

    st.write("⏳ Technical Interview")

    st.write("⏳ Final Decision")

    status = st.selectbox(
        "Update Candidate Status",
        [
            "Under Review",
            "Resume Screening Passed",
            "AI Interview Unlocked",
            "Technical Interview Scheduled",
            "Selected",
            "Rejected"
        ]
    )

    if st.button("Update Status"):

        conn = sqlite3.connect(
            "recruitment.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE applications
            SET status = ?,
            hr_email = ?
            WHERE email = ?
            """,
            (
                status,
                st.session_state.employee_email,
                candidate["email"]
            )
        )

        conn.commit()

        conn.close()

        candidate["status"] = status

        st.success(
            f"Status Updated: {status}"
        )

        st.rerun()

    st.markdown("---")

    st.subheader("🤖 AI Interview Results")

    conn = sqlite3.connect(
        "recruitment.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        answer_1,
        answer_2,
        answer_3,
        answer_4,
        ai_score,
        ai_feedback
        FROM interviews
        WHERE candidate_email = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            candidate["email"],
        )
    )

    interview = cursor.fetchone()

    conn.close()

    if interview:

        st.write(
            f"🎯 AI Interview Score : {interview[4]}%"
        )

        st.success(
            interview[5]
        )

        st.markdown("---")

        st.subheader(
            "📊 Final Recommendation"
        )

        if interview[4] >= 75:

            st.success(
                "✅ Recommended For Technical Round"
            )
        if st.button(
            "🚀 Move To Technical Round"
         ):

            conn = sqlite3.connect(
                "recruitment.db"
            )

            cursor = conn.cursor()

            cursor.execute(
               """
               UPDATE applications
               SET status = ?
               WHERE email = ?
               """,
               (
                  "Technical Interview Scheduled",
                   candidate["email"]
                )
           )

            conn.commit()

            conn.close()

            st.success(
                "Candidate moved to Technical Round"
    )

            st.rerun()

        elif interview[4] >= 50:

            st.warning(
                "⏳ Hold For HR Review"
            )

        else:

            st.error(
                "❌ Not Recommended"
            )

        st.markdown("---")

        st.write(
            "1️⃣ Introduce Yourself"
        )

        st.info(
            interview[0]
        )

        st.write(
            "2️⃣ Analytical Question"
        )

        st.info(
            interview[1]
        )

        st.write(
            "3️⃣ Project Question"
        )

        st.info(
            interview[2]
        )

        st.write(
            "4️⃣ Why Should We Hire You?"
        )

        st.info(
            interview[3]
        )

    else:

        st.warning(
            "AI Interview not completed yet."
        )

    st.markdown("---")

    if st.button("🤖 View AI Analysis"):

        st.session_state.page = "analysis"

        st.rerun()

    if st.button("⬅ Back to Dashboard"):

        st.session_state.page = "hr_dashboard"

        st.rerun()
# ----------------------------------
# Thank you
# ----------------------------------
def thank_you_page():

    st.title("✅ Application Submitted")

    st.markdown("---")

    st.success(
        "Thank you for applying. Your application has been submitted successfully."
    )

    st.info(
        "Our recruitment team will review your profile and contact you if your profile matches the job requirements."
    )

    st.balloons()

    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

#-----------------------------------
#Applicant status dashboad page
#-----------------------------------

def applicant_dashboard_page():

    st.title("📋 My Applications")

    st.markdown("---")

    conn = sqlite3.connect(
        "recruitment.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
        company,
        role,
        status,
        final_score,
        hr_email
        FROM applications
        WHERE email = ?
        """,
        (
            st.session_state.logged_in_email,
        )
    )

    applications = cursor.fetchall()

    conn.close()

    if len(applications) == 0:

        st.info(
            "No applications found."
        )

    else:

        for i, app in enumerate(applications):

            st.write(
                f"🏢 Company : {app[0]}"
            )

            st.write(
                f"💼 Role : {app[1]}"
            )

            st.write(
                f"📊 Status : {app[2]}"
            )

            st.write(
                f"🎯 Score : {app[3]}%"
            )

            if app[2] == "AI Interview Unlocked":

                st.success(
                    "🤖 AI Interview Available"
                )

                if st.button(
                    "Start AI Interview",
                    key=f"interview_{i}"
                ):

                    st.session_state.page = (
                        "ai_interview"
                    )

                    st.rerun()

            elif app[2] == "Technical Interview Scheduled":

                st.success(
                    "🎉 Congratulations! You have cleared the AI HR Interview Round."
                )

                st.info(
                    f"Please contact HR at {app[4]} regarding the Technical Interview schedule."
                )

            st.markdown("---")

    if st.button("🚀 Apply New Job"):

        st.session_state.page = "jobs"

        st.rerun()

    if st.button("🚪 Logout"):

        st.session_state.logged_in_email = ""

        st.session_state.page = "home"

        st.rerun()

    if st.button("⬅ Back"):

        st.session_state.page = "home"

        st.rerun()

#---------------------------------
#Ai interview page
#---------------------------------
def ai_interview_page():

    st.title("🤖 AI HR Interview")

    st.success(
        "🎤 Voice Enabled AI Interview"
    )

    st.info(
        "Record your answers using the microphone and submit them for AI evaluation."
    )

    st.markdown("---")

    st.write(
        "1️⃣ Introduce Yourself"
    )
    
    st.warning(
       "⏱ Maximum Recording Time: 60 Seconds"
    )

    audio1 = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="q1_audio"
    )

    q1 = st.text_area(
        "Answer 1",
        height=120
    )

    st.markdown("---")

    st.write(
        "2️⃣ Analytical Question: A train travels 60 km in 1 hour. How long will it take to travel 180 km?"
    )

    st.warning(
       "⏱ Maximum Recording Time: 90 Seconds"
    )

    audio2 = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="q2_audio"
    )

    q2 = st.text_area(
        "Answer 2",
        height=120
    )

    st.markdown("---")

    st.write(
        "3️⃣ Explain your best project from your resume."
    )
    
    st.warning(
       "⏱ Maximum Recording Time: 60 Seconds"
    )

    audio3 = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="q3_audio"
    )

    q3 = st.text_area(
        "Answer 3",
        height=120
    )

    st.markdown("---")

    st.write(
        "4️⃣ Why should we hire you?"
    )
    st.warning(
       "⏱ Maximum Recording Time: 60 Seconds"
    )

    audio4 = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="q4_audio"
    )

    q4 = st.text_area(
        "Answer 4",
        height=120
    )

    st.markdown("---")

    if st.button(
        "🚀 Submit Interview"
    ):

        if (
            not q1
            or not q2
            or not q3
            or not q4
        ):

            st.error(
                "Please answer all questions."
            )

        else:

            communication_score = 0
            analytical_score = 0
            technical_score = 0
            confidence_score = 0

            if len(q1) > 50:

                communication_score = 25

            if (
                "3" in q2
                or "3 hour" in q2.lower()
            ):

                analytical_score = 25

            if len(q3) > 50:

                technical_score = 25

            if len(q4) > 50:

                confidence_score = 25

            ai_score = (
                communication_score
                + analytical_score
                + technical_score
                + confidence_score
            )

            if ai_score >= 75:

                ai_feedback = (
                    "Strong candidate. Recommended for Technical Round."
                )

            elif ai_score >= 50:

                ai_feedback = (
                    "Average performance. Needs HR review."
                )

            else:

                ai_feedback = (
                    "Below expected performance level."
                )

            conn = sqlite3.connect(
                "recruitment.db"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO interviews
                (
                    candidate_email,
                    answer_1,
                    answer_2,
                    answer_3,
                    answer_4,
                    ai_score,
                    ai_feedback,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.logged_in_email,
                    q1,
                    q2,
                    q3,
                    q4,
                    ai_score,
                    ai_feedback,
                    "Completed"
                )
            )

            cursor.execute(
                """
                SELECT resume_score
                FROM applications
                WHERE email = ?
                """,
                (
                    st.session_state.logged_in_email,
                )
            )

            result = cursor.fetchone()

            resume_score = 0

            if result:

                resume_score = result[0]

            final_score = round(
                (
                    resume_score * 0.5
                )
                +
                (
                    ai_score * 0.5
                )
            )

            cursor.execute(
                """
                UPDATE applications
                SET interview_score = ?,
                    final_score = ?
                WHERE email = ?
                """,
                (
                    ai_score,
                    final_score,
                    st.session_state.logged_in_email
                )
            )

            conn.commit()

            conn.close()

            st.success(
                "Interview Submitted Successfully"
            )

            st.success(
                f"🎯 AI Interview Score : {ai_score}%"
            )

            st.success(
                f"🏆 Final Score : {final_score}%"
            )

            st.info(
                ai_feedback
            )

            st.session_state.page = (
                "thank_you"
            )

            st.rerun()

    if st.button(
        "⬅ Back"
    ):

        st.session_state.page = (
            "applicant_dashboard"
        )

        st.rerun()
# ----------------------------------
# Routing
# ----------------------------------

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "jobs":
    jobs_page()

elif st.session_state.page == "job_details":
    job_details_page()

elif st.session_state.page == "questions":
    screening_questions_page()

elif st.session_state.page == "resume_upload":
    resume_upload_page()

elif st.session_state.page == "analysis":
    analysis_page()

elif st.session_state.page == "thank_you":
    thank_you_page()

elif st.session_state.page == "hr_dashboard":
    hr_dashboard_page()

elif st.session_state.page == "candidate_profile":
    candidate_profile_page()

elif st.session_state.page == "applicant_portal":
    applicant_portal_page()

elif st.session_state.page == "applicant_login":
    applicant_login_page()

elif st.session_state.page == "applicant_signup":
    applicant_signup_page()

elif st.session_state.page == "employee_portal":
    employee_portal_page()

elif st.session_state.page == "employee_login":
    employee_login_page()

elif st.session_state.page == "employee_signup":
    employee_signup_page()

elif st.session_state.page == "applicant_dashboard":
    applicant_dashboard_page()

elif st.session_state.page == "ai_interview":
    ai_interview_page()

elif st.session_state.page == "admin_dashboard":
    admin_dashboard_page()

elif st.session_state.page == "manager_dashboard":
    manager_dashboard_page()

elif st.session_state.page == "employee_dashboard":
    employee_dashboard_page()

elif st.session_state.page == "attendance":
    attendance_page()

elif st.session_state.page == "payroll":
    payroll_page()

elif st.session_state.page == "performance":
    performance_page()