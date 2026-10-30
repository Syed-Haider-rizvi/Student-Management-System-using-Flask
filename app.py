from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models.student import db, Student

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    query = Student.query
    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    students = query.order_by(Student.id.desc()).all()
    return render_template("index.html", students=students, search=search)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student = Student(
            name=request.form["name"].strip(),
            email=request.form["email"].strip(),
            phone=request.form.get("phone", "").strip(),
            course=request.form.get("course", "").strip(),
            address=request.form.get("address", "").strip()
        )
        db.session.add(student)
        try:
            db.session.commit()
            flash("Student added successfully!", "success")
            return redirect(url_for("index"))
        except Exception:
            db.session.rollback()
            flash("Could not add student. Check whether the email already exists.", "danger")
    return render_template("add_student.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = db.get_or_404(Student, id)
    if request.method == "POST":
        student.name = request.form["name"].strip()
        student.email = request.form["email"].strip()
        student.phone = request.form.get("phone", "").strip()
        student.course = request.form.get("course", "").strip()
        student.address = request.form.get("address", "").strip()
        try:
            db.session.commit()
            flash("Student updated successfully!", "success")
            return redirect(url_for("index"))
        except Exception:
            db.session.rollback()
            flash("Could not update student. Check whether the email already exists.", "danger")
    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    student = db.get_or_404(Student, id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
