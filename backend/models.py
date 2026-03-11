from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash
from datetime import datetime
import uuid


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum("Admin", "Company", "Student", name="user_roles"), nullable=False)
    status = db.Column(db.Enum("Active", "Pending", "Blocked", name="user_status"), default="Pending")
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)

    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))
    student_profile = db.relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    company_profile = db.relationship("Company", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def get_id(self):
        return str(self.user_id)


class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(256), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    resume_url = db.Column(db.String(512), nullable=True)

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")


class Company(db.Model):
    __tablename__ = "company"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), unique=True, nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.Text)
    hr_contact = db.Column(db.String(256))
    website = db.Column(db.String(256))
    approval_status = db.Column(db.Enum("Pending", "Approved", "Blocked", name="company_status"), default="Pending")
    verified_on = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="company_profile")
    drives = db.relationship("PlacementDrive", back_populates="company", cascade="all, delete-orphan")
    applications = db.relationship("Application", back_populates="company")


class PlacementDrive(db.Model):
    __tablename__ = "placement_drive"

    drive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"), nullable=False)
    drive_name = db.Column(db.String(256), nullable=False)
    job_title = db.Column(db.String(256), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligible_departments = db.Column(db.String(512))
    min_cgpa = db.Column(db.Float, default=0.0)
    eligible_years = db.Column(db.String(128))
    salary = db.Column(db.Integer)
    location = db.Column(db.String(256))
    deadline = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum("Pending", "Approved", "Closed", "Completed", name="drive_status"), default="Pending")

    company = db.relationship("Company", back_populates="drives")
    applications = db.relationship("Application", back_populates="drive", cascade="all, delete-orphan")


class Application(db.Model):
    __tablename__ = "application"

    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.drive_id"), nullable=False)
    status = db.Column(db.Enum("Applied", "Shortlisted", "Selected", "Rejected", name="application_status"), default="Applied")
    remarks = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )

    student = db.relationship("Student", back_populates="applications")
    company = db.relationship("Company", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")


class Feedback(db.Model):
    __tablename__ = "feedback"

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)

