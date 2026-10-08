import pandas as pd
import numpy as np
import sqlite3

from flask import Flask, render_template

# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# ============================================================
# 1. STUDENT DATASET
# ============================================================

data = {
    "Student_ID": [
        101, 102, 103, 104, 105, 106,
        107, 108, 109, 110, 111, 112
    ],

    "Name": [
        "Anjali", "Rahul", "Sneha", "Arjun",
        "Priya", "Kiran", "Divya", "Ravi",
        "Pooja", "Vikram", "Swathi", "Naveen"
    ],

    "Python": [
        85, 72, 95, 60, 88, 76,
        91, 68, 84, 79, 93, 70
    ],

    "HTML": [
        90, 75, 88, 58, 91, 82,
        94, 70, 86, 80, 90, 76
    ],

    "CSS": [
        88, 70, 94, 62, 89, 78,
        92, 67, 83, 81, 91, 72
    ],

    "JavaScript": [
        82, 78, 96, 70, 90, 80,
        95, 72, 85, 79, 94, 75
    ],

    "Attendance": [
        92, 85, 98, 75, 94, 88,
        96, 79, 91, 86, 97, 83
    ]
}


# Create DataFrame
df = pd.DataFrame(data)

# ============================================================
# DATABASE
# ============================================================

conn = sqlite3.connect("student_performance.db")

df.to_sql(
    "students",
    conn,
    if_exists="replace",
    index=False
)

df = pd.read_sql_query(
    "SELECT * FROM students",
    conn
)

# ============================================================
# 2. DISPLAY TITLE
# ============================================================

print("=" * 65)
print("          STUDENT PERFORMANCE ANALYTICS SYSTEM")
print("=" * 65)

# ============================================================
# 3. DISPLAY STUDENT DATA
# ============================================================

print("\n")
print("--------------- STUDENT DATA ---------------")

print(df.to_string(index=False))

# ============================================================
# 4. SUBJECTS
# ============================================================

subjects = [
    "Python",
    "HTML",
    "CSS",
    "JavaScript"
]

# ============================================================
# 5. TOTAL MARKS
# ============================================================

df["Total"] = df[subjects].sum(axis=1)

# ============================================================
# 6. AVERAGE MARKS
# ============================================================

df["Average"] = df[subjects].mean(axis=1)

df["Average"] = df["Average"].round(2)

# ============================================================
# 7. GRADE FUNCTION
# ============================================================

def calculate_grade(average):

    if average >= 90:
        return "A+"

    elif average >= 80:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    elif average >= 50:
        return "D"

    else:
        return "F"


df["Grade"] = df["Average"].apply(calculate_grade)

# ============================================================
# 8. RESULT FUNCTION
# ============================================================

def calculate_result(average):

    if average >= 40:
        return "Pass"

    else:
        return "Fail"

df["Result"] = df["Average"].apply(calculate_result)

# ============================================================
# 9. STUDENT PERFORMANCE
# ============================================================

print("\n")
print("------------- STUDENT PERFORMANCE -------------")

performance = df[
    [
        "Student_ID",
        "Name",
        "Total",
        "Average",
        "Grade",
        "Result"
    ]
]

print(performance.to_string(index=False))

# ============================================================
# 10. NUMPY ANALYSIS
# ============================================================

print("\n")
print("---------------- ANALYSIS ----------------")

# Subject-wise average
subject_average = df[subjects].mean()

print("\nSubject-wise Average:")

for subject in subjects:

    print(
        subject,
        ":",
        round(subject_average[subject], 2)
    )

# ============================================================
# 11. OVERALL CLASS AVERAGE
# ============================================================

overall_average = np.mean(df["Average"])

print(
    "\nOverall Class Average:",
    round(overall_average, 2)
)

# ============================================================
# 12. HIGHEST TOTAL
# ============================================================

highest_total = np.max(df["Total"])

print(
    "Highest Total Marks:",
    highest_total
)

# ============================================================
# 13. LOWEST TOTAL
# ============================================================

lowest_total = np.min(df["Total"])

print(
    "Lowest Total Marks:",
    lowest_total
)

# ============================================================
# 14. TOP PERFORMER
# ============================================================

top_index = df["Total"].idxmax()

top_student = df.loc[top_index, "Name"]

top_average = df.loc[top_index, "Average"]

print("\nTop Performer:", top_student)

print(
    "Top Performer Average:",
    top_average
)

# ============================================================
# 15. LOWEST PERFORMER
# ============================================================

lowest_index = df["Total"].idxmin()

lowest_student = df.loc[
    lowest_index,
    "Name"
]

print(
    "Lowest Performer:",
    lowest_student
)

# ============================================================
# 16. HIGHEST ATTENDANCE
# ============================================================

highest_attendance_index = df[
    "Attendance"
].idxmax()

highest_attendance_student = df.loc[
    highest_attendance_index,
    "Name"
]

highest_attendance = df.loc[
    highest_attendance_index,
    "Attendance"
]

print(
    "\nHighest Attendance:",
    highest_attendance_student
)

print(
    "Attendance:",
    highest_attendance,
    "%"
)

# ============================================================
# 17. LOW ATTENDANCE STUDENTS
# ============================================================

print("\n")
print("---------- LOW ATTENDANCE STUDENTS ----------")

low_attendance = df[
    df["Attendance"] < 80
]

if len(low_attendance) == 0:

    print("No students have attendance below 80%.")

else:

    print(
        low_attendance[
            [
                "Student_ID",
                "Name",
                "Attendance"
            ]
        ].to_string(index=False)
    )

# ============================================================
# 18. PASSED STUDENTS
# ============================================================

passed_students = df[
    df["Result"] == "Pass"
]

failed_students = df[
    df["Result"] == "Fail"
]

print("\n")

print(
    "Number of Passed Students:",
    len(passed_students)
)

print(
    "Number of Failed Students:",
    len(failed_students)
)

# ============================================================
# 19. SUBJECT-WISE TOP STUDENT
# ============================================================

print("\n")
print("-------- SUBJECT-WISE TOP STUDENTS --------")

for subject in subjects:

    index = df[subject].idxmax()

    student_name = df.loc[
        index,
        "Name"
    ]

    marks = df.loc[
        index,
        subject
    ]

    print(
        subject,
        ":",
        student_name,
        "-",
        marks
    )

# ============================================================
# 20. GRADE ANALYSIS
# ============================================================

print("\n")
print("-------------- GRADE ANALYSIS --------------")

grade_count = df["Grade"].value_counts()

print(grade_count)

# ============================================================
# 21. STUDENTS ABOVE CLASS AVERAGE
# ============================================================

print("\n")
print("------ STUDENTS ABOVE CLASS AVERAGE ------")

above_average = df[
    df["Average"] > overall_average
]

print(
    above_average[
        [
            "Student_ID",
            "Name",
            "Average",
            "Grade"
        ]
    ].to_string(index=False)
)

# ============================================================
# 22. STUDENT SEARCH FUNCTION
# ============================================================

def search_student(student_id):

    result = df[
        df["Student_ID"] == student_id
    ]

    if result.empty:

        print("\nStudent not found.")

    else:

        print("\nStudent Details:")

        print(
            result.to_string(index=False)
        )

# Example search
search_student(105)

# ============================================================
# 23. FINAL OUTCOME
# ============================================================

print("\n")
print("=" * 65)
print("                     FINAL OUTCOME")
print("=" * 65)

print(
    "\nTotal Students:",
    len(df)
)

print(
    "Class Average:",
    round(overall_average, 2)
)

print(
    "Top Performer:",
    top_student
)

print(
    "Lowest Performer:",
    lowest_student
)

print(
    "Passed Students:",
    len(passed_students)
)

print(
    "Failed Students:",
    len(failed_students)
)

print(
    "Highest Attendance:",
    highest_attendance_student
)

print(
    "\nStudent Performance Analysis Completed Successfully!"
)

print("=" * 65)

# ============================================================
# TOP 5 TOPPERS
# ============================================================

print("\n")
print("--------------- TOP 5 TOPPERS ---------------")

top_5 = df.sort_values(
    by="Total",
    ascending=False
).head(5)

print(
    top_5[
        [
            "Student_ID",
            "Name",
            "Total",
            "Average",
            "Grade"
        ]
    ].to_string(index=False)
)

# ============================================================
# SAVE CSV
# ============================================================

df.to_csv(
    "students.csv",
    index=False
)

print("\nstudents.csv created successfully!")

# ============================================================
# FLASK ROUTE
# ============================================================

@app.route("/")
def home():

    # Convert complete DataFrame to dictionary
    students = df.to_dict(orient="records")

    # Subject averages
    subject_avg = {
        subject: round(subject_average[subject], 2)
        for subject in subjects
    }

    # Grade counts
    grades = grade_count.to_dict()

    # Top 5 students
    top5_students = top_5[
        [
            "Student_ID",
            "Name",
            "Total",
            "Average",
            "Grade"
        ]
    ].to_dict(orient="records")

    # Low attendance students
    low_attendance_students = low_attendance[
        [
            "Student_ID",
            "Name",
            "Attendance"
        ]
    ].to_dict(orient="records")

    return render_template(
        "index.html",
        students=students,
        subject_avg=subject_avg,
        overall_average=round(overall_average, 2),
        highest_total=highest_total,
        lowest_total=lowest_total,
        top_student=top_student,
        top_average=top_average,
        lowest_student=lowest_student,
        highest_attendance_student=highest_attendance_student,
        highest_attendance=highest_attendance,
        passed_count=len(passed_students),
        failed_count=len(failed_students),
        top5_students=top5_students,
        low_attendance_students=low_attendance_students,
        grades=grades
    )

# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
)
