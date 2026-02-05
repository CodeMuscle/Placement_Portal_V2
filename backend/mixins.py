from datetime import datetime
from models import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class StatusMixin:
    def is_active(self):
        return getattr(self, "status", None) == "Active"

    def is_pending(self):
        return getattr(self, "status", None) == "Pending"

    def is_blocked(self):
        return getattr(self, "status", None) == "Blocked"


class RoleMixin:
    def is_student(self):
        return getattr(self, "role", None) == "Student"

    def is_company(self):
        return getattr(self, "role", None) == "Company"


class ProfileMixin:
    def has_student_profile(self):
        return hasattr(self, "student_profile") and self.student_profile is not None

    def has_company_profile(self):
        return hasattr(self, "company_profile") and self.company_profile is not None


class SerializableMixin:
    def to_dict(self, exclude=None):
        exclude = exclude or []
        data = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                data[column.name] = getattr(self, column.name)
        return data
