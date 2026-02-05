from database import db
from mixin import (
    TimestampMixin,
    StatusMixin,
    RoleMixin,
    ProfileMixin,
    SerializableMixin
)
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, TimestampMixin, StatusMixin, RoleMixin, ProfileMixin, SerializableMixin):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum("Company", "Student", name="user_roles"), nullable=False)
    status = db.Column(
        db.Enum("Active", "Pending", "Blocked", name="user_status"),
        default="Pending"
    )

    student_profile = db.relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    company_profile = db.relationship(
        "Company",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


class Student(db.Model, TimestampMixin, SerializableMixin):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), unique=True)
    name = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(256), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    resume_url = db.Column(db.String(512), nullable=False)

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student")


class Company(db.Model, TimestampMixin, StatusMixin, SerializableMixin):
    __tablename__ = "company"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), unique=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.Text)
    hr_contact = db.Column(db.String(256))
    website = db.Column(db.String(256))
    status = db.Column(
        db.Enum("Pending", "Approved", "Blocked", name="company_status"),
        default="Pending"
    )
    verified_on = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="company_profile")
    drives = db.relationship("PlacementDrive", back_populates="company")
    applications = db.relationship("Application", back_populates="company")


class Admin(db.Model, TimestampMixin, SerializableMixin):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class PlacementDrive(db.Model, TimestampMixin, StatusMixin, SerializableMixin):
    __tablename__ = "placement_drive"

    drive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"))
    drive_name = db.Column(db.String(256), nullable=False)
    job_title = db.Column(db.String(256), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.Text)
    salary = db.Column(db.Integer)
    location = db.Column(db.String(256))
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum("Pending", "Approved", "Closed", "Completed", name="drive_status"),
        default="Pending"
    )

    company = db.relationship("Company", back_populates="drives")
    applications = db.relationship("Application", back_populates="drive")


class Application(db.Model, TimestampMixin, StatusMixin, SerializableMixin):
    __tablename__ = "application"

    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"))
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.drive_id"))
    status = db.Column(
        db.Enum("Applied", "Shortlisted", "Selected", "Rejected", name="application_status"),
        default="Applied"
    )
    remarks = db.Column(db.Text)

    student = db.relationship("Student", back_populates="applications")
    company = db.relationship("Company", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")


class Feedback(db.Model, TimestampMixin, SerializableMixin):
    __tablename__ = "feedback"

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    to_user = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
