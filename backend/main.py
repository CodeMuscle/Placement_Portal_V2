from flask import Flask
from flask_security import Security
from database import db
from config import config
from user_datastore import user_datastore
from flask_restful import Api
from flask_cors import CORS
from cache import cache

from controllers.auth import (
    LoginAPI, LogoutAPI, RegisterStudentAPI,
    RegisterCompanyAPI, CheckEmailAPI
)
from controllers.student import (
    StudentProfileAPI, StudentResumeAPI,
    StudentDrivesAPI, StudentApplicationAPI,
    StudentExportAPI
)
from controllers.company import (
    CompanyProfileAPI, CompanyDriveAPI,
    CompanyApplicationsAPI
)
from controllers.admin import (
    AdminDashboardAPI, AdminCompanyApprovalAPI,
    AdminDriveApprovalAPI, AdminStudentAPI,
    AdminApplicationsAPI, AdminSearchAPI
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    security = Security(app, user_datastore)

    with app.app_context():
        import models
        db.create_all()

        for role_name in ("Admin", "Company", "Student"):
            if not user_datastore.find_role(role_name):
                user_datastore.create_role(name=role_name)
        db.session.commit()

        if not user_datastore.find_user(email="admin@ppa.com"):
            from flask_security import utils
            import uuid
            admin_user = user_datastore.create_user(
                username="admin",
                email="admin@ppa.com",
                password=utils.hash_password("admin"),
                role="Admin",
                status="Active",
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
            )
            user_datastore.add_role_to_user(admin_user, "Admin")
            db.session.commit()

    api = Api(app, prefix='/api')

    api.add_resource(CheckEmailAPI,          '/auth/check-email')
    api.add_resource(LoginAPI,               '/auth/login')
    api.add_resource(LogoutAPI,              '/auth/logout')
    api.add_resource(RegisterStudentAPI,     '/auth/register/student')
    api.add_resource(RegisterCompanyAPI,     '/auth/register/company')

    api.add_resource(StudentProfileAPI,      '/student/profile')
    api.add_resource(StudentResumeAPI,       '/student/resume')
    api.add_resource(StudentDrivesAPI,       '/student/drives')
    api.add_resource(StudentApplicationAPI,  '/student/apply/<int:drive_id>', '/student/applications')
    api.add_resource(StudentExportAPI,       '/student/export')

    api.add_resource(CompanyProfileAPI,      '/company/profile')
    api.add_resource(CompanyDriveAPI,        '/company/drives', '/company/drives/<int:drive_id>')
    api.add_resource(CompanyApplicationsAPI, '/company/drives/<int:drive_id>/applications',
                                             '/company/drives/<int:drive_id>/applications/<int:application_id>')

    api.add_resource(AdminDashboardAPI,      '/admin/dashboard')
    api.add_resource(AdminCompanyApprovalAPI,'/admin/companies', '/admin/companies/<int:company_id>')
    api.add_resource(AdminDriveApprovalAPI,  '/admin/drives', '/admin/drives/<int:drive_id>')
    api.add_resource(AdminStudentAPI,        '/admin/students', '/admin/students/<int:student_id>')
    api.add_resource(AdminApplicationsAPI,   '/admin/applications')
    api.add_resource(AdminSearchAPI,         '/admin/search')

    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
