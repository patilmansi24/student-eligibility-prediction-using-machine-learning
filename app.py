import streamlit as st
from utils.auth import check_authentication, login, logout
from models.user import User
from config.database import get_connection, init_database, create_default_admin

# Page configuration
st.set_page_config(
    page_title="Academic and Skill-Based Filtering Using ML",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database (first-time setup)
# init_database()
# create_default_admin()

# Custom CSS
st.markdown("""
<style>
.main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center; padding: 1rem; }
.sub-header { font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
.stButton>button { width: 100%; background-color: #1f77b4; color: white; border-radius: 5px; padding: 0.5rem 1rem; font-weight: bold; }
.stButton>button:hover { background-color: #155a8a; }
</style>
""", unsafe_allow_html=True)

# ---------------- Helper functions ----------------
def fetch_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()
    conn.close()
    return students

def fetch_all_companies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies;")
    companies = cur.fetchall()
    conn.close()
    return companies

# def fetch_eligible_count():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT COUNT(DISTINCT student_id) FROM eligibility_results WHERE eligibility_status='Eligible';")
#     count = cur.fetchone()[0]
#     conn.close()
#     return count

def fetch_eligible_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT student_id) AS eligible FROM eligibility_results WHERE eligibility_status='Eligible';")
    result = cur.fetchone()
    conn.close()
    return result['eligible'] if result else 0


# def fetch_total_matches():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT COUNT(*) FROM eligibility_results;")
#     count = cur.fetchone()[0]
#     conn.close()
#     return count

def fetch_total_matches():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM eligibility_results;")
    result = cur.fetchone()
    conn.close()
    return result['total'] if result else 0


# ---------------- Main ----------------
def main():
    if not check_authentication():
        show_login_page()
    else:
        show_dashboard()

# ---------------- Login Page ----------------
def show_login_page():
    st.markdown("<div class='main-header'>🎓 Academic and Skill-Based Filtering Using ML</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>AI-Powered Placement Eligibility Platform</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### Login to Continue")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login")
            if submit:
                if username and password:
                    if login(username, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

        st.markdown("---")
        st.info("""
**Default Login Credentials:**
- Username: `admin`
- Password: `admin123`

*Please change the password after first login*
""")

# ---------------- Dashboard ----------------
def show_dashboard():
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.username}!")
        st.markdown(f"**Role:** {st.session_state.role.title()}")
        st.markdown("---")
        st.markdown("### Navigation")

        role = st.session_state.role
        if role == 'teacher':
            st.page_link("pages/1_Teacher_Portal.py", label="👨‍🏫 Teacher Portal", use_container_width=True)
        elif role == 'student':
            st.page_link("pages/2_Student_Dashboard.py", label="🎓 Student Dashboard", use_container_width=True)
        elif role == 'admin':
            st.page_link("pages/1_Teacher_Portal.py", label="👨‍🏫 Teacher Portal", use_container_width=True)
            st.page_link("pages/3_Admin_Panel.py", label="👔 Admin Panel", use_container_width=True)

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    st.markdown("<div class='main-header'>🎓 Academic and Skill-Based Filtering Using ML</div>", unsafe_allow_html=True)

    # Role-based dashboard
    if role == 'teacher':
        show_teacher_home()
    elif role == 'student':
        show_student_home()
    elif role == 'admin':
        show_admin_home()

# ---------------- Teacher ----------------
def show_teacher_home():
    st.markdown("### Teacher Dashboard")
    students = fetch_all_students()
    companies = fetch_all_companies()
    eligible_count = fetch_eligible_count()
    avg_cgpa = sum([s['cgpa'] for s in students])/len(students) if students else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(students))
    col2.metric("Total Companies", len(companies))
    col3.metric("Eligible Students", eligible_count)
    col4.metric("Average CGPA", f"{avg_cgpa:.2f}")

    st.markdown("---")
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    if col1.button("➕ Add New Student"): st.switch_page("pages/1_Teacher_Portal.py")
    if col2.button("🏢 Add New Company"): st.switch_page("pages/1_Teacher_Portal.py")
    if col3.button("📊 View Reports"): st.switch_page("pages/1_Teacher_Portal.py")

# ---------------- Student ----------------
def show_student_home():
    st.markdown("### Student Dashboard")
    st.info("Navigate to Student Dashboard from the sidebar to view your profile and eligible companies.")

# ---------------- Admin ----------------
def show_admin_home():
    st.markdown("### Admin Dashboard")
    students = fetch_all_students()
    companies = fetch_all_companies()
    total_matches = fetch_total_matches()
    users = User.get_all_users()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(students))
    col2.metric("Total Companies", len(companies))
    col3.metric("Total Matches", total_matches)
    col4.metric("Total Users", len(users))

    st.markdown("---")
    st.markdown("### System Management")
    col1, col2, col3 = st.columns(3)
    if col1.button("👥 Manage Users"): st.switch_page("pages/3_Admin_Panel.py")
    if col2.button("📊 View Analytics"): st.switch_page("pages/3_Admin_Panel.py")
    if col3.button("🔧 System Settings"): st.switch_page("pages/3_Admin_Panel.py")

# ---------------- Run ----------------
if __name__ == "__main__":
    main()
