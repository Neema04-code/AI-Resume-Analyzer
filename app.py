import os
import sqlite3

from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename

from resume_reader import extract_text
from analyzer import analyze_resume
from recommendation import get_recommendations
from pdf_report import create_pdf
from flask import send_file

app = Flask(__name__)

app.secret_key = "resume_analyzer_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Database connection
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email, password)
            )

            conn.commit()
            conn.close()

            return "Registration successful. Please login."

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered"

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:
            session["user"] = user["name"]

            return render_template(
                "dashboard.html",
                name=user["name"]
            )

        else:
            return "Invalid email or password"

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" in session:
        return render_template(
            "dashboard.html",
            name=session["user"]
        )

    return render_template("login.html")
# Upload Resume + Analyze
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["resume"]

        if file:

            filename = secure_filename(file.filename)

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(path)


            # Extract resume text
            resume_text = extract_text(path)


            # Analyze resume
            result = analyze_resume(resume_text)


            # Get suggestions and jobs
            suggestions, jobs = get_recommendations(
                result["found"],
                result["missing"]
            )


            # Store data for PDF report
            session["score"] = result["score"]
            session["found"] = result["found"]
            session["missing"] = result["missing"]
            session["jobs"] = jobs


            # Save history in database
            conn = get_db()

            conn.execute(
                """
                INSERT INTO history
                (user_name, score, skills, missing, jobs)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session["user"],
                    result["score"],
                    ", ".join(result["found"]),
                    ", ".join(result["missing"]),
                    ", ".join(jobs)
                )
            )

            conn.commit()
            conn.close()


            # Show result page
            return render_template(
                "result.html",
                text=resume_text,
                score=result["score"],
                found=result["found"],
                missing=result["missing"],
                suggestions=suggestions,
                jobs=jobs
            )


    return render_template("upload.html")
# Profile Page
@app.route("/profile")
def profile():

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE name=?",
        (session["user"],)
    ).fetchone()


    data = conn.execute(
        "SELECT COUNT(*) as total, MAX(score) as best_score FROM history WHERE user_name=?",
        (session["user"],)
    ).fetchone()


    conn.close()


    return render_template(
        "profile.html",
        name=user["name"],
        email=user["email"],
        total=data["total"],
        best_score=data["best_score"] or 0
    )
# History Page
@app.route("/history")
def history():

    conn = get_db()

    search = request.args.get("search")

    if search:

        data = conn.execute(
            """
            SELECT * FROM history
            WHERE user_name=?
            AND (
                skills LIKE ?
                OR jobs LIKE ?
                OR missing LIKE ?
            )
            """,
            (
                session["user"],
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    else:

        data = conn.execute(
            "SELECT * FROM history WHERE user_name=?",
            (session["user"],)
        ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=data
    )

#download_report
@app.route("/download_report")
def download_report():

    filename = "resume_analysis_report.pdf"

    create_pdf(
        filename,
        session["score"],
        session["found"],
        session["missing"],
        session["jobs"]
    )

    return send_file(
        filename,
        as_attachment=True
    )
    #about
@app.route("/about")
def about():
    return render_template("about.html")
#admin
@app.route("/admin")
def admin():

    conn = get_db()

    users = conn.execute("SELECT * FROM users").fetchall()

    total_users = conn.execute(
        "SELECT COUNT(*) AS total FROM users"
    ).fetchone()["total"]

    total_history = conn.execute(
        "SELECT COUNT(*) AS total FROM history"
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        total_users=total_users,
        total_history=total_history
    )
#contact
@app.route("/contact")
def contact():
    return render_template("contact.html")
# Logout
@app.route("/logout")
def logout():

    session.clear()

    return render_template("login.html")
# Run app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )