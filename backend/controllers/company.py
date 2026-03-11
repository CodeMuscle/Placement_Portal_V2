from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required, current_user, roles_required
from database import db
from models import Company, PlacementDrive, Application
from datetime import datetime


class CompanyProfileAPI(Resource):
    @auth_token_required
    @roles_required('Company')
    def get(self):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        return make_response(jsonify({
            'company_id': company.company_id,
            'name': company.name,
            'description': company.description,
            'hr_contact': company.hr_contact,
            'website': company.website,
            'approval_status': company.approval_status,
            'verified_on': company.verified_on.isoformat() if company.verified_on else None
        }), 200)

    @auth_token_required
    @roles_required('Company')
    def put(self):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        company.description = data.get('description', company.description)
        company.hr_contact = data.get('hr_contact', company.hr_contact)
        company.website = data.get('website', company.website)

        db.session.commit()

        return make_response(jsonify({'message': 'Company profile updated successfully.'}), 200)


class CompanyDriveAPI(Resource):
    @auth_token_required
    @roles_required('Company')
    def post(self):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        if company.approval_status != 'Approved':
            return make_response(jsonify({'message': 'Company not approved by admin yet.'}), 403)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        drive_name = data.get('drive_name', None)
        job_title = data.get('job_title', None)
        job_description = data.get('job_description', None)
        deadline = data.get('deadline', None)

        if not all([drive_name, job_title, job_description, deadline]):
            return make_response(jsonify({'message': 'Required fields: drive_name, job_title, job_description, deadline.'}), 400)

        try:
            deadline_dt = datetime.fromisoformat(deadline)
        except ValueError:
            return make_response(jsonify({'message': 'Invalid deadline format. Use ISO format: YYYY-MM-DDTHH:MM:SS.'}), 400)

        drive = PlacementDrive(
            company_id=company.company_id,
            drive_name=drive_name,
            job_title=job_title,
            job_description=job_description,
            eligible_departments=data.get('eligible_departments', None),
            min_cgpa=data.get('min_cgpa', 0.0),
            eligible_years=data.get('eligible_years', None),
            salary=data.get('salary', None),
            location=data.get('location', None),
            deadline=deadline_dt,
            status='Pending'
        )
        db.session.add(drive)
        db.session.commit()

        return make_response(jsonify({'message': 'Placement drive created. Awaiting admin approval.'}), 201)

    @auth_token_required
    @roles_required('Company')
    def get(self):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        drives = PlacementDrive.query.filter_by(company_id=company.company_id).all()

        result = []
        for drive in drives:
            result.append({
                'drive_id': drive.drive_id,
                'drive_name': drive.drive_name,
                'job_title': drive.job_title,
                'status': drive.status,
                'deadline': drive.deadline.isoformat(),
                'applicant_count': len(drive.applications)
            })

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('Company')
    def put(self, drive_id):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        drive = PlacementDrive.query.filter_by(drive_id=drive_id, company_id=company.company_id).first()

        if not drive:
            return make_response(jsonify({'message': 'Drive not found.'}), 404)

        if drive.status not in ('Pending', 'Approved'):
            return make_response(jsonify({'message': 'Only Pending or Approved drives can be edited.'}), 403)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        drive.drive_name = data.get('drive_name', drive.drive_name)
        drive.job_title = data.get('job_title', drive.job_title)
        drive.job_description = data.get('job_description', drive.job_description)
        drive.eligible_departments = data.get('eligible_departments', drive.eligible_departments)
        drive.min_cgpa = data.get('min_cgpa', drive.min_cgpa)
        drive.eligible_years = data.get('eligible_years', drive.eligible_years)
        drive.salary = data.get('salary', drive.salary)
        drive.location = data.get('location', drive.location)

        if data.get('deadline'):
            try:
                drive.deadline = datetime.fromisoformat(data.get('deadline'))
            except ValueError:
                return make_response(jsonify({'message': 'Invalid deadline format.'}), 400)

        db.session.commit()

        return make_response(jsonify({'message': 'Drive updated successfully.'}), 200)


class CompanyApplicationsAPI(Resource):
    @auth_token_required
    @roles_required('Company')
    def get(self, drive_id):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        drive = PlacementDrive.query.filter_by(drive_id=drive_id, company_id=company.company_id).first()

        if not drive:
            return make_response(jsonify({'message': 'Drive not found.'}), 404)

        applications = Application.query.filter_by(drive_id=drive_id).all()

        result = []
        for app in applications:
            result.append({
                'application_id': app.application_id,
                'student_id': app.student_id,
                'student_name': app.student.name,
                'department': app.student.department,
                'year_of_study': app.student.year_of_study,
                'cgpa': app.student.cgpa,
                'resume_url': app.student.resume_url,
                'status': app.status,
                'remarks': app.remarks,
                'applied_at': app.applied_at.isoformat()
            })

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('Company')
    def put(self, drive_id, application_id):
        company = Company.query.filter_by(user_id=current_user.user_id).first()

        if not company:
            return make_response(jsonify({'message': 'Company profile not found.'}), 404)

        drive = PlacementDrive.query.filter_by(drive_id=drive_id, company_id=company.company_id).first()

        if not drive:
            return make_response(jsonify({'message': 'Drive not found.'}), 404)

        application = Application.query.filter_by(application_id=application_id, drive_id=drive_id).first()

        if not application:
            return make_response(jsonify({'message': 'Application not found.'}), 404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        new_status = data.get('status', None)
        valid_statuses = ('Applied', 'Shortlisted', 'Selected', 'Rejected')

        if new_status and new_status not in valid_statuses:
            return make_response(jsonify({'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}.'}), 400)

        application.status = new_status or application.status
        application.remarks = data.get('remarks', application.remarks)

        db.session.commit()

        return make_response(jsonify({'message': 'Application status updated successfully.'}), 200)
