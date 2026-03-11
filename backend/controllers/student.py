from flask_restful import Resource
from flask import request, jsonify, make_response, current_app
from flask_security import auth_token_required, current_user, roles_required
from user_datastore import user_datastore
from database import db
from models import Student, Application, PlacementDrive, Company
from tasks import export_applications_csv
import os


class StudentProfileAPI(Resource):
    @auth_token_required
    @roles_required('Student')
    def get(self):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        return make_response(jsonify({
            'student_id': student.student_id,
            'name': student.name,
            'email': current_user.email,
            'username': current_user.username,
            'department': student.department,
            'year_of_study': student.year_of_study,
            'cgpa': student.cgpa,
            'resume_url': student.resume_url
        }), 200)

    @auth_token_required
    @roles_required('Student')
    def put(self):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)

        student.name = data.get('name', student.name)
        student.department = data.get('department', student.department)
        student.year_of_study = data.get('year_of_study', student.year_of_study)
        student.cgpa = data.get('cgpa', student.cgpa)

        db.session.commit()

        return make_response(jsonify({'message': 'Profile updated successfully.'}), 200)


class StudentResumeAPI(Resource):
    @auth_token_required
    @roles_required('Student')
    def post(self):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        if 'resume' not in request.files:
            return make_response(jsonify({'message': 'Resume file is required.'}), 400)

        file = request.files['resume']

        if file.filename == '':
            return make_response(jsonify({'message': 'No file selected.'}), 400)

        if not file.filename.endswith('.pdf'):
            return make_response(jsonify({'message': 'Only PDF files are allowed.'}), 400)

        upload_folder = os.path.join(current_app.root_path, 'static', 'resumes')
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"student_{student.student_id}.pdf"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        student.resume_url = f"/static/resumes/{filename}"
        db.session.commit()

        return make_response(jsonify({
            'message': 'Resume uploaded successfully.',
            'resume_url': student.resume_url
        }), 200)


class StudentDrivesAPI(Resource):
    @auth_token_required
    @roles_required('Student')
    def get(self):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        search = request.args.get('search', '').lower()

        drives = PlacementDrive.query.filter_by(status='Approved').all()

        result = []
        for drive in drives:
            if search and search not in drive.job_title.lower() and search not in drive.drive_name.lower():
                continue

            eligible_depts = [d.strip() for d in drive.eligible_departments.split(',')] if drive.eligible_departments else []
            eligible_years = [int(y.strip()) for y in drive.eligible_years.split(',')] if drive.eligible_years else []

            is_eligible = (
                (not eligible_depts or student.department in eligible_depts) and
                (not eligible_years or student.year_of_study in eligible_years) and
                (student.cgpa >= drive.min_cgpa)
            )

            result.append({
                'drive_id': drive.drive_id,
                'drive_name': drive.drive_name,
                'job_title': drive.job_title,
                'job_description': drive.job_description,
                'company_name': drive.company.name,
                'location': drive.location,
                'salary': drive.salary,
                'deadline': drive.deadline.isoformat(),
                'min_cgpa': drive.min_cgpa,
                'eligible_departments': eligible_depts,
                'eligible_years': eligible_years,
                'is_eligible': is_eligible
            })

        return make_response(jsonify(result), 200)


class StudentApplicationAPI(Resource):
    @auth_token_required
    @roles_required('Student')
    def post(self, drive_id):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        drive = PlacementDrive.query.filter_by(drive_id=drive_id, status='Approved').first()

        if not drive:
            return make_response(jsonify({'message': 'Placement drive not found or not approved.'}), 404)

        existing = Application.query.filter_by(student_id=student.student_id, drive_id=drive_id).first()
        if existing:
            return make_response(jsonify({'message': 'You have already applied for this drive.'}), 409)

        eligible_depts = [d.strip() for d in drive.eligible_departments.split(',')] if drive.eligible_departments else []
        eligible_years = [int(y.strip()) for y in drive.eligible_years.split(',')] if drive.eligible_years else []

        if eligible_depts and student.department not in eligible_depts:
            return make_response(jsonify({'message': 'You are not eligible: department mismatch.'}), 403)

        if eligible_years and student.year_of_study not in eligible_years:
            return make_response(jsonify({'message': 'You are not eligible: year of study mismatch.'}), 403)

        if student.cgpa < drive.min_cgpa:
            return make_response(jsonify({'message': f'You are not eligible: minimum CGPA required is {drive.min_cgpa}.'}), 403)

        application = Application(
            student_id=student.student_id,
            company_id=drive.company_id,
            drive_id=drive_id,
            status='Applied'
        )
        db.session.add(application)
        db.session.commit()

        return make_response(jsonify({'message': 'Application submitted successfully.'}), 201)

    @auth_token_required
    @roles_required('Student')
    def get(self):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        applications = Application.query.filter_by(student_id=student.student_id).all()

        result = []
        for app in applications:
            result.append({
                'application_id': app.application_id,
                'drive_id': app.drive_id,
                'drive_name': app.drive.drive_name,
                'job_title': app.drive.job_title,
                'company_name': app.company.name,
                'status': app.status,
                'remarks': app.remarks,
                'applied_at': app.applied_at.isoformat()
            })

        return make_response(jsonify(result), 200)


class StudentExportAPI(Resource):
    @auth_token_required
    @roles_required('Student')
    def post(self):
        student = Student.query.filter_by(user_id=current_user.user_id).first()

        if not student:
            return make_response(jsonify({'message': 'Student profile not found.'}), 404)

        export_applications_csv.delay(student.student_id, current_user.email)

        return make_response(jsonify({'message': 'Export started. You will receive an email when done.'}), 202)
