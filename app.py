import json
import re
from abc import ABC, abstractmethod
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# Data layer (same JSON database as the original script)
# ----------------------------------------------------------------------------
DATABASE = Path("School_data.json")


def load_data():
    data = {"STUDENTS": [], "TEACHERS": []}
    if DATABASE.exists():
        try:
            content = DATABASE.read_text()
            if content.strip():
                loaded = json.loads(content)
                data["STUDENTS"] = loaded.get("STUDENTS", [])
                data["TEACHERS"] = loaded.get("TEACHERS", [])
        except json.JSONDecodeError:
            st.warning("School_data.json could not be read, starting with empty data.")
    return data


def save(data):
    DATABASE.write_text(json.dumps(data, indent=4))


# ----------------------------------------------------------------------------
# Domain classes (original OOP structure, now returning results to the UI)
# ----------------------------------------------------------------------------
class Humans(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def getroles(self):
        pass

    @abstractmethod
    def register(self, **kwargs):
        pass

    @abstractmethod
    def showdetails(self, name):
        pass

    @staticmethod
    def validate_email(email):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", email.strip()))

    @staticmethod
    def check_mobile_no(mobile_no):
        return bool(re.fullmatch(r"\d{10}", mobile_no.strip()))


class Students(Humans):
    def getroles(self):
        return "STUDENT"

    def register(self, name, age, std, roll_no, email, mobile_no):
        name = name.strip()
        if not name:
            return False, "Name is required."
        if not self.validate_email(email):
            return False, "Please check the email address."
        if not self.check_mobile_no(mobile_no):
            return False, "Mobile number must be exactly 10 digits."
        for s in self.data["STUDENTS"]:
            if s["name"].lower() == name.lower():
                return False, "This student is already registered."
        self.data["STUDENTS"].append(
            {
                "name": name,
                "std": int(std),
                "age": int(age),
                "roll_no": int(roll_no),
                "email": email.strip(),
                "mobile_no": mobile_no.strip(),
                "grades": {},
            }
        )
        save(self.data)
        return True, f"{name} is registered as a student."

    def showdetails(self, name):
        for s in self.data["STUDENTS"]:
            if s["name"].lower() == name.strip().lower():
                return s
        return None

    def add_grades(self, name, subject, marks):
        subject = subject.strip()
        if not subject:
            return False, "Subject is required."
        student = self.showdetails(name)
        if student is None:
            return False, "Student not found."
        student["grades"][subject] = float(marks)
        save(self.data)
        return True, f"{subject}: {marks:g} saved for {student['name']}."


class Teachers(Humans):
    def getroles(self):
        return "TEACHER"

    def register(self, name, age, edu, subject, email, mobile_no):
        name = name.strip()
        if not name:
            return False, "Name is required."
        if not self.validate_email(email):
            return False, "Please check the email address."
        if not self.check_mobile_no(mobile_no):
            return False, "Mobile number must be exactly 10 digits."
        for t in self.data["TEACHERS"]:
            if t["name"].lower() == name.lower():
                return False, "This teacher is already registered."
        self.data["TEACHERS"].append(
            {
                "name": name,
                "age": int(age),
                "edu": edu.strip(),
                "subject": subject.strip(),
                "email": email.strip(),
                "mobile_no": mobile_no.strip(),
            }
        )
        save(self.data)
        return True, f"{name} is registered as a teacher."

    def showdetails(self, name):
        for t in self.data["TEACHERS"]:
            if t["name"].lower() == name.strip().lower():
                return t
        return None


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def std_of(student):
    # Older records used the key "Std"
    return student.get("std", student.get("Std", "-"))


def average(student):
    grades = student.get("grades", {})
    return sum(grades.values()) / len(grades) if grades else 0.0


def letter(avg):
    if avg >= 90:
        return "A+"
    if avg >= 80:
        return "A"
    if avg >= 70:
        return "B"
    if avg >= 60:
        return "C"
    if avg >= 40:
        return "D"
    return "F"


def initials(name):
    parts = name.split()
    return "".join(p[0] for p in parts[:2]).upper() or "?"


CSS = """
<style>
.block-container {padding-top: 2rem; max-width: 1150px;}
.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
    border-radius: 20px; padding: 2rem 2.2rem; color: white; margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(79,70,229,.25);
}
.hero h1 {margin: 0; font-size: 2rem; color: white;}
.hero p {margin: .3rem 0 0; opacity: .9;}
.stat {
    border-radius: 16px; padding: 1.1rem 1.3rem; border: 1px solid rgba(128,128,128,.25);
    background: rgba(128,128,128,.07);
}
.stat .icon {font-size: 1.6rem;}
.stat .value {font-size: 2rem; font-weight: 700; line-height: 1.1;}
.stat .label {opacity: .7; font-size: .85rem; text-transform: uppercase; letter-spacing: .06em;}
.profile {
    display: flex; gap: 1.2rem; align-items: center; padding: 1.3rem 1.5rem;
    border-radius: 18px; border: 1px solid rgba(128,128,128,.25);
    background: rgba(128,128,128,.07); margin-bottom: 1rem;
}
.avatar {
    width: 72px; height: 72px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 1.6rem; font-weight: 700; color: white;
    background: linear-gradient(135deg, #4f46e5, #db2777); flex-shrink: 0;
}
.profile h3 {margin: 0;}
.badge {
    display: inline-block; padding: .15rem .7rem; border-radius: 999px; font-size: .78rem;
    font-weight: 600; background: rgba(124,58,237,.18); color: #8b5cf6; margin-right: .4rem;
}
.meta {opacity: .75; font-size: .9rem; margin-top: .35rem;}
div[data-testid="stForm"] {border-radius: 16px; padding: 1.4rem;}
.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    border-radius: 10px; font-weight: 600;
}
</style>
"""


def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def stat_card(icon, value, label):
    st.markdown(
        f'<div class="stat"><div class="icon">{icon}</div>'
        f'<div class="value">{escape(str(value))}</div>'
        f'<div class="label">{escape(label)}</div></div>',
        unsafe_allow_html=True,
    )


def profile_card(name, badges, meta_lines):
    badge_html = "".join(f'<span class="badge">{escape(str(b))}</span>' for b in badges)
    meta_html = "".join(f'<div class="meta">{escape(m)}</div>' for m in meta_lines)
    st.markdown(
        f'<div class="profile"><div class="avatar">{escape(initials(name))}</div>'
        f"<div><h3>{escape(name)}</h3>{badge_html}{meta_html}</div></div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def page_dashboard(data):
    hero("🎓 School Management", "Students, teachers and grades in one place.")
    students, teachers = data["STUDENTS"], data["TEACHERS"]
    graded = [average(s) for s in students if s.get("grades")]
    subjects = {t["subject"] for t in teachers if t.get("subject")}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("🧑‍🎓", len(students), "Students")
    with c2:
        stat_card("👩‍🏫", len(teachers), "Teachers")
    with c3:
        stat_card("📊", f"{sum(graded) / len(graded):.1f}" if graded else "–", "Avg. score")
    with c4:
        stat_card("📚", len(subjects), "Subjects taught")

    st.write("")
    left, right = st.columns([3, 2])
    with left:
        st.subheader("Student averages")
        if graded:
            df = pd.DataFrame(
                {"Student": [s["name"] for s in students if s.get("grades")], "Average": graded}
            ).set_index("Student")
            st.bar_chart(df, color="#7c3aed")
        else:
            st.info("No grades recorded yet. Add some from the **Grades** page.")
    with right:
        st.subheader("Recently registered")
        recent = [("🧑‍🎓", s["name"], f"Std {std_of(s)}") for s in students[-4:]] + [
            ("👩‍🏫", t["name"], t.get("subject", "")) for t in teachers[-3:]
        ]
        if recent:
            for icon, name, sub in reversed(recent):
                st.markdown(f"{icon} **{name}** · {sub}")
        else:
            st.info("Nobody registered yet.")


def page_register_student(data):
    hero("🧑‍🎓 Register Student", "Add a new student to the school records.")
    with st.form("student_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full name")
        age = c2.number_input("Age", min_value=3, max_value=25, value=10)
        c3, c4 = st.columns(2)
        std = c3.number_input("Standard", min_value=1, max_value=12, value=1)
        roll_no = c4.number_input("Roll no.", min_value=1, value=1)
        c5, c6 = st.columns(2)
        email = c5.text_input("Student / parent email")
        mobile = c6.text_input("Student / parent mobile (10 digits)", max_chars=10)
        submitted = st.form_submit_button("Register student", type="primary", use_container_width=True)
    if submitted:
        ok, msg = Students(data).register(name, age, std, roll_no, email, mobile)
        (st.success if ok else st.error)(msg)
        if ok:
            st.balloons()


def page_register_teacher(data):
    hero("👩‍🏫 Register Teacher", "Add a new teacher to the school records.")
    with st.form("teacher_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full name")
        age = c2.number_input("Age", min_value=18, max_value=75, value=30)
        c3, c4 = st.columns(2)
        edu = c3.text_input("Education qualification")
        subject = c4.text_input("Subject taught")
        c5, c6 = st.columns(2)
        email = c5.text_input("Email address")
        mobile = c6.text_input("Mobile number (10 digits)", max_chars=10)
        submitted = st.form_submit_button("Register teacher", type="primary", use_container_width=True)
    if submitted:
        ok, msg = Teachers(data).register(name, age, edu, subject, email, mobile)
        (st.success if ok else st.error)(msg)
        if ok:
            st.balloons()


def page_students(data):
    hero("📋 Student Directory", "Search students and view their report.")
    students = data["STUDENTS"]
    if not students:
        st.info("No students registered yet.")
        return

    query = st.text_input("🔍 Search by name", placeholder="Start typing a name…")
    filtered = [s for s in students if query.lower() in s["name"].lower()]
    if not filtered:
        st.warning("STUDENT NOT FOUND")
        return

    df = pd.DataFrame(
        [
            {
                "Name": s["name"],
                "Standard": std_of(s),
                "Roll no.": s["roll_no"],
                "Age": s["age"],
                "Email": s["email"],
                "Mobile": s["mobile_no"],
                "Average": round(average(s), 1),
            }
            for s in filtered
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Student report")
    chosen = st.selectbox("Select a student", [s["name"] for s in filtered])
    s = Students(data).showdetails(chosen)
    avg = average(s)
    profile_card(
        s["name"],
        [f"Std {std_of(s)}", f"Roll {s['roll_no']}", f"Grade {letter(avg)}" if s["grades"] else "No grades"],
        [f"✉️ {s['email']}   ·   📱 {s['mobile_no']}   ·   Age {s['age']}"],
    )
    if s["grades"]:
        c1, c2 = st.columns([2, 3])
        c1.metric("Average", f"{avg:.1f}")
        c1.dataframe(
            pd.DataFrame({"Subject": list(s["grades"]), "Marks": list(s["grades"].values())}),
            hide_index=True,
            use_container_width=True,
        )
        c2.bar_chart(pd.Series(s["grades"], name="Marks"), color="#db2777")
    else:
        st.caption("No grades recorded for this student yet.")


def page_teachers(data):
    hero("📋 Teacher Directory", "Browse and search teaching staff.")
    teachers = data["TEACHERS"]
    if not teachers:
        st.info("No teachers registered yet.")
        return

    query = st.text_input("🔍 Search by name or subject", placeholder="e.g. Maths")
    q = query.lower()
    filtered = [t for t in teachers if q in t["name"].lower() or q in t.get("subject", "").lower()]
    if not filtered:
        st.warning("TEACHER NOT FOUND")
        return

    for t in filtered:
        profile_card(
            t["name"],
            [t.get("subject", "-"), f"Age {t['age']}"],
            [f"🎓 {t.get('edu', '')}", f"✉️ {t['email']}   ·   📱 {t['mobile_no']}"],
        )


def page_grades(data):
    hero("📝 Grades", "Record marks for registered students.")
    students = data["STUDENTS"]
    if not students:
        st.info("Register a student first.")
        return

    name = st.selectbox("Student", [s["name"] for s in students])
    student = Students(data).showdetails(name)

    with st.form("grade_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 2])
        subject = c1.text_input("Subject", placeholder="e.g. Science")
        marks = c2.number_input("Marks", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        submitted = st.form_submit_button("Save grade", type="primary", use_container_width=True)
    if submitted:
        ok, msg = Students(data).add_grades(name, subject, marks)
        (st.success if ok else st.error)(msg)
        student = Students(data).showdetails(name)

    st.subheader(f"{student['name']}'s grades")
    if student["grades"]:
        st.metric("Average", f"{average(student):.1f}", letter(average(student)))
        st.dataframe(
            pd.DataFrame({"Subject": list(student["grades"]), "Marks": list(student["grades"].values())}),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.caption("No grades yet.")


# ----------------------------------------------------------------------------
# App
# ----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="School Management", page_icon="🎓", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    data = load_data()

    pages = {
        "🏠 Dashboard": page_dashboard,
        "🧑‍🎓 Register Student": page_register_student,
        "👩‍🏫 Register Teacher": page_register_teacher,
        "📋 Students": page_students,
        "📋 Teachers": page_teachers,
        "📝 Grades": page_grades,
    }
    with st.sidebar:
        st.markdown("## 🎓 School Portal")
        choice = st.radio("Navigate", list(pages), label_visibility="collapsed")
        st.divider()
        st.caption(f"{len(data['STUDENTS'])} students · {len(data['TEACHERS'])} teachers")

    pages[choice](data)


main()