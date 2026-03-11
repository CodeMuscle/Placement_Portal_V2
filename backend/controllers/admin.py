from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required, current_user, roles_required
from user_datastore import user_datastore
from database import db
from models import Student, Company, PlacementDrive, Application, User
from cache import cache

class AdminDashboardAPI(Resource):
    @auth_token_required
    @roles_required('Admin')
    @cache.cached(timeout=60, key_prefix='admin_dashboard')

    def get(self):
        total_students = Student.query.count()
        total_companies = Company.query.count()
        total_drives = PlacementDrive.query.count()
        total_applications = Application.query.count()
        pending_companies = Company.query.filter_by(approval_status='Pending').count()
        pending_drives = PlacementDrive.query.filter_by(status='Pending').count()

        return make_response(jsonify({
            'total_students': total_students,
            'total_companies': total_companies,
            'total_drives': total_drives,
            'total_applications': total_applications,
            'pending_companies': pending_companies,
            'pending_drives': pending_drives
        }), 200)


class AdminCompanyApprovalAPI(Resource):
    @auth_token_required
    @roles_required('Admin')
    @cache.cached(timeout=120, key_prefix='admin_companies')
    def get(self):
        status_filter = request.args.get('status', None)

        query = Company.query
        if status_filter:
            query = query.filter_by(approval_status=status_filter)

        companies = query.all()

        result = []
        for company in companies:
            result.append({
                'company_id': company.company_id,
                'name': company.name,
                'description': company.description,
                'hr_contact': company.hr_contact,
                'website': company.website,
                'approval_status': company.approval_status,
                'verified_on': company.verified_on.isoformat() if company.verified_on else None,
                'user_status': company.user.status
            })

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('Admin')
    def put(self, company_id):
        company = Company.query.filter_by(company_id=company_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company not found.'}), 404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        action = data.get('action', None)

        if action not in ('approve', 'reject', 'block'):
            return make_response(jsonify({'message': 'Invalid action. Must be: approve, reject, or block.'}), 400)

        if action == 'approve':
            company.approval_status = 'Approved'
            company.user.status = 'Active'
            from datetime import datetime
            company.verified_on = datetime.utcnow()
        elif action == 'reject':
            company.approval_status = 'Pending'
            company.user.status = 'Pending'
        elif action == 'block':
            company.approval_status = 'Blocked'
            company.user.status = 'Blocked'
            company.user.active = False

        db.session.commit()

        return make_response(jsonify({'message': f'Company {action}d successfully.'}), 200)


class AdminDriveApprovalAPI(Resource):
    @auth_token_required
    @roles_required('Admin')
    @cache.cached(timeout=120, key_prefix='admin_drives')
    def get(self):
        status_filter = request.args.get('status', None)

        query = PlacementDrive.query
        if status_filter:
            query = query.filter_by(status=status_filter)

        drives = query.all()

        result = []
        for drive in drives:
            result.append({
                'drive_id': drive.drive_id,
                'drive_name': drive.drive_name,
                'job_title': drive.job_title,
                'company_name': drive.company.name,
                'status': drive.status,
                'deadline': drive.deadline.isoformat(),
                'created_on': drive.created_on.isoformat()
            })

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('Admin')
    def put(self, drive_id):
        drive = PlacementDrive.query.filter_by(drive_id=drive_id).first()

        if not drive:
            return make_response(jsonify({'message': 'Drive not found.'}), 404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        action = data.get('action', None)

        if action not in ('approve', 'reject', 'close'):
            return make_response(jsonify({'message': 'Invalid action. Must be: approve, reject, or close.'}), 400)

        if action == 'approve':
            drive.status = 'Approved'
        elif action == 'reject':
            drive.status = 'Pending'
        elif action == 'close':
            drive.status = 'Closed'

        db.session.commit()

        return make_response(jsonify({'message': f'Drive {action}d successfully.'}), 200)


class AdminStudentAPI(Resource):
    @auth_token_required
    @roles_required('Admin')
    def get(self):
        students = Student.query.all()

        result = []
        for student in students:
            result.append({
                'student_id': student.student_id,
                'name': student.name,
                'email': student.user.email,
                'username': student.user.username,
                'department': student.department,
                'year_of_study': student.year_of_study,
                'cgpa': student.cgpa,
                'status': student.user.status,
                'active': student.user.active
            })

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('Admin')
    def put(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student not found.'}), 404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        action = data.get('action', None)

        if action not in ('block', 'unblock'):
            return make_response(jsonify({'message': 'Invalid action. Must be: block or unblock.'}), 400)

        if action == 'block':
            student.user.status = 'Blocked'
            student.user.active = False
        elif action == 'unblock':
            student.user.status = 'Active'
            student.user.active = True

        db.session.commit()

        return make_response(jsonify({'message': f'Student {action}ed successfully.'}), 200)


class AdminApplicationsAPI(Resource):
    @auth_token_required
    @roles_required('Admin')
    def get(self):
        applications = Application.query.all()

        result = []
        for app in applications:
            result.append({
                'application_id': app.application_id,
                'student_name': app.student.name,
                'company_name': app.company.name,
                'drive_name': app.drive.drive_name,
                'job_title': app.drive.job_title,
                'status': app.status,
                'applied_at': app.applied_at.isoformat()
            })

        return make_response(jsonify(result), 200)


class AdminSearchAPI(Resource):
    @auth_token_required
    @roles_required('Admin')
    def get(self):
        query = request.args.get('q', '').strip().lower()

        if not query:
            return make_response(jsonify({'message': 'Search query is required.'}), 400)

        students = Student.query.all()
        student_results = []
        for student in students:
            if (query in student.name.lower() or
                query in student.user.email.lower() or
                query in student.department.lower()):
                student_results.append({
                    'type': 'student',
                    'student_id': student.student_id,
                    'name': student.name,
                    'email': student.user.email,
                    'department': student.department,
                    'cgpa': student.cgpa,
                    'status': student.user.status
                })

        companies = Company.query.all()
        company_results = []
        for company in companies:
            if (query in company.name.lower() or
                query in company.user.email.lower() or
                (company.website and query in company.website.lower())):
                company_results.append({
                    'type': 'company',
                    'company_id': company.company_id,
                    'name': company.name,
                    'email': company.user.email,
                    'approval_status': company.approval_status,
                    'status': company.user.status
                })

        return make_response(jsonify({
            'students': student_results,
            'companies': company_results
        }), 200)
