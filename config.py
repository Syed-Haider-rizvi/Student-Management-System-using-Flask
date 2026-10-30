class Config:
    SECRET_KEY = "student-management-secret-key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://student_user:StudentDB2026%21@localhost:3306/student_management"

    SQLALCHEMY_TRACK_MODIFICATIONS = False