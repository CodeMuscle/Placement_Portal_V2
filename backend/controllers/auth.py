from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required, roles_required
from user_datastore import user_datastore
from database import db
from models import Student, Company
import uuid


class CheckEmailAPI(Resource):
    def post(self):
        credential = request.get_json()

        if not credential:
            return make_response(jsonify({'message': 'Request body is required.'}), 400)
        email = credential.get('email', None)

        if not email:
            return make_response(jsonify({'message': 'Email is required.'}), 400)

        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({'available': False}), 200)
        else:
            return make_response(jsonify({'available': True}), 200)


class LoginAPI(Resource):
    def post(self):
        creds = request.get_json()

        if not creds:
            return make_response(jsonify({'message': 'Login credentials are required.'}), 400)

        email = creds.get('email', None)
        password = creds.get('password', None)

        if not email or not password:
            return make_response(jsonify({'message': 'Email and password are required.'}), 400)

        user = user_datastore.find_user(email=email)

        if not user:
            return make_response(jsonify({'message': 'User not found.'}), 404)

        if not user.active:
            return make_response(jsonify({'message': 'Account is deactivated. Contact admin.'}), 403)

        if user.status == 'Blocked':
            return make_response(jsonify({'message': 'Account is blocked. Contact admin.'}), 403)

        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message': 'Invalid password.'}), 401)

        auth_token = user.get_auth_token()
        utils.login_user(user)

        response = {
            'message': 'Login successful.',
            'user_details': {
                'user_id': user.user_id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'status': user.status,
                'roles': [role.name for role in user.roles],
                'auth_token': auth_token
            }
        }
        return make_response(jsonify(response), 200)


class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'message': 'Logout successful.'}), 200)


class RegisterStudentAPI(Resource):
    def post(self):
        creds = request.get_json()

        if not creds:
            return make_response(jsonify({'message': 'Registration credentials are required.'}), 400)

        email = creds.get('email', None)
        password = creds.get('password', None)
        username = creds.get('username', None)
        name = creds.get('name', None)
        department = creds.get('department', None)
        year_of_study = creds.get('year_of_study', None)
        cgpa = creds.get('cgpa', None)

        if not all([email, password, username, name, department, year_of_study, cgpa]):
            return make_response(jsonify({'message': 'All fields are required: email, password, username, name, department, year_of_study, cgpa.'}), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({'message': 'User already exists with this email.'}), 409)

        student_role = user_datastore.find_role('Student')

        user = user_datastore.create_user(
            username=username,
            email=email,
            password=utils.hash_password(password),
            role='Student',
            status='Active',
            active=True,
            fs_uniquifier=str(uuid.uuid4()),
            roles=[student_role]
        )
        db.session.flush()

        student_profile = Student(
            user_id=user.user_id,
            name=name,
            department=department,
            year_of_study=year_of_study,
            cgpa=cgpa
        )
        db.session.add(student_profile)
        db.session.commit()

        return make_response(jsonify({
            'message': 'Student registration successful.',
            'user_details': {
                'email': user.email,
                'username': user.username,
                'role': user.role
            }
        }), 201)


class RegisterCompanyAPI(Resource):
    def post(self):
        creds = request.get_json()

        if not creds:
            return make_response(jsonify({'message': 'Registration credentials are required.'}), 400)

        email = creds.get('email', None)
        password = creds.get('password', None)
        username = creds.get('username', None)
        company_name = creds.get('company_name', None)
        description = creds.get('description', None)
        hr_contact = creds.get('hr_contact', None)
        website = creds.get('website', None)

        if not all([email, password, username, company_name]):
            return make_response(jsonify({'message': 'Required fields: email, password, username, company_name.'}), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({'message': 'User already exists with this email.'}), 409)

        company_role = user_datastore.find_role('Company')

        user = user_datastore.create_user(
            username=username,
            email=email,
            password=utils.hash_password(password),
            role='Company',
            status='Pending',
            active=True,
            fs_uniquifier=str(uuid.uuid4()),
            roles=[company_role]
        )
        db.session.flush()

        company_profile = Company(
            user_id=user.user_id,
            name=company_name,
            description=description,
            hr_contact=hr_contact,
            website=website,
            approval_status='Pending'
        )
        db.session.add(company_profile)
        db.session.commit()

        return make_response(jsonify({
            'message': 'Company registration successful. Await admin approval.',
            'user_details': {
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'approval_status': company_profile.approval_status
            }
        }), 201)
