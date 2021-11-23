from functools import wraps

import werkzeug.exceptions
from flask import jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from sqlalchemy import or_, desc

import Validation
from FreelancerModel import *
from UserModel import UserModel
from ContractsModel import *
import bcrypt
from Freelancer import Freelancer

freelancer_schema = FreelancerSchema()
freelancers_schema = FreelancerSchema(many=True)
contract_schema = ContractSchema()
contracts_schema = ContractSchema(many=True)

USER_DATA = ['email', 'password', 'surname', 'name']


@app.route('/api/v1.0/register', methods=['POST'])
def register():
    try:
        msg, email, password, name, surname = get_user_data()
        if msg:
            return jsonify({'status': 400, 'message': msg}), 400
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = UserModel(email=email, hash=hashed, name=name, surname=surname, role=UserRole.USER.value)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=create_identity(user))
        return jsonify({'status': 200, 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


def get_user_data():
    msg = ''
    data = {}
    for i in USER_DATA:
        data[i] = request.json.get(i, None)
    if not data['email']:
        msg += 'Missing email '
    else:
        try:
            valid = Validation.is_email(lambda *_: _)
            valid(None, data['email'])
        except ValueError:
            msg += 'Invalid email'
    if not data['password']:
        msg += 'Missing password'
    return msg, *data.values()


def create_identity(user):
    return {"id": user.id, "email": user.email, "role": user.role}


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity['role'] != UserRole.ADMIN.value:
            return jsonify({'status': 403, 'message': 'Admins only!'}), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


@app.route('/api/v1.0/login', methods=['POST'])
def login():
    try:
        msg, email, password, n, s = get_user_data()
        if msg:
            return jsonify({'status': 400, 'message': msg}), 400
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return jsonify({'status': 400, 'message': 'Invalid login info'}), 400
        if bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8')):
            access_token = create_access_token(identity=create_identity(user))

            return jsonify({'status': 200, 'access_token': access_token}), 200
        else:
            return jsonify({'status': 400, 'message': 'Invalid login info'}), 400
    except AttributeError as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers', methods=['GET'])
@jwt_required()
def get_freelancers():
    try:
        sort_by = request.args.get('sort_by')
        sort_type = request.args.get('sort_type', default='desc')
        s = request.args.get('s')
        all_fr = FreelancerModel.query
        if s:
            all_fr = all_fr.filter(
                or_(
                    FreelancerModel.id.like(f"%{s}%"),
                    FreelancerModel.name.like(f"%{s}%"),
                    FreelancerModel.email.like(f"%{s}%"),
                    FreelancerModel.phone_number.like(f"%{s}%"),
                    FreelancerModel.availability.like(f"%{s}%"),
                    FreelancerModel.salary.like(f"%{s}%"),
                    FreelancerModel.position.like(f"%{s}%"),
                ))
        count = len(all_fr.all())
        if sort_by:
            if sort_type.lower() == 'asc':
                all_fr = all_fr.order_by(sort_by)
            else:
                all_fr = all_fr.order_by(desc(sort_by))
        limit, offset = request.args.get('limit', type=int), request.args.get('offset', default=0, type=int)
        if limit:
            all_fr = all_fr.offset(offset * limit).limit(limit)

        results = freelancers_schema.dump(all_fr.all())
        if len(results) == 0:
            return jsonify({'status': 404, 'message': "No matches found"}), 404
        return jsonify({'status': 200, 'data': results, 'count': count}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['GET'])
@jwt_required()
def get_freelancer(id_):
    results = freelancer_schema.dump(FreelancerModel.query.get(id_))
    if len(results) == 0:
        return jsonify({'status': 404, 'message': "Freelancer is not found"}), 404
    return jsonify({'status': 200, 'data': results}), 200


@app.route('/api/v1.0/freelancers', methods=['POST'])
@jwt_required()
@admin_required
def post_freelancer():
    try:
        exception_message = {}
        dummy = Freelancer.init_default()
        if len(request.json) != dummy.count_of_fields:
            exception_message['Amount of data'] = "Invalid"
        for i, field in enumerate(vars(dummy).keys()):
            try:
                setattr(dummy, field.split("__")[-1], request.json[field.split("__")[-1]])
            except ValueError as e:
                exception_message[field.split("__")[-1]] = str(e)
        if exception_message:
            raise ValueError(exception_message)
        new_freelancer = FreelancerModel(*vars(dummy).values())
        db.session.add(new_freelancer)
        db.session.commit()
        return jsonify({'status': 200, 'message': "Freelancer has been successfully created."}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_freelancer(id_):
    try:
        freelancer = FreelancerModel.query.get_or_404(id_)
        db.session.delete(freelancer)
        db.session.commit()
        return jsonify({'status': 200, 'message': "Freelancer has been successfully deleted."}), 200
    except Exception as e:
        return jsonify({'status': 404, 'message': str(e)}), 404


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['PUT'])
@jwt_required()
@admin_required
def update_freelancer(id_):
    try:
        dummy = Freelancer.init_default()
        exception_message = {}
        for i, field in enumerate(request.json.keys()):
            try:
                setattr(dummy, field, request.json[field])
            except ValueError as e:
                exception_message[field] = str(e)
        if exception_message:
            raise ValueError(exception_message)
        freelancer = FreelancerModel.query.filter_by(id=id_)
        if not freelancer.all():
            return jsonify({'status': 404, 'message': "Freelancer is not found"}), 404
        freelancer.update(request.json)
        db.session.commit()
        return jsonify({'status': 200, 'message': "Freelancer has been successfully updated."}), 200
    except Exception as e:
        if isinstance(e, werkzeug.exceptions.NotFound):
            return jsonify({'status': 404, 'message': str(e)}), 404
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/contracts', methods=['POST'])
@jwt_required()
def post_contract():
    try:
        data = request.json
        identity = get_jwt_identity()
        FreelancerModel.query.get_or_404(data['freelancer_id'])
        contracts = ContractsModel.query.filter_by(user_id=identity['id'])
        if len(contracts.all()) >= ContractsModel.CONTRACTS_LIMIT:
            raise ValueError(f"Too much contracts for {identity['email']}")
        new_contract = ContractsModel(freelancer_id=data['freelancer_id'], user_id=identity['id'],
                                      description=data['description'])
        db.session.add(new_contract)
        db.session.commit()
        return jsonify({'status': 200, 'message': "Contract has been successfully created."}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/contracts', methods=['GET'])
@jwt_required()
def get_contracts():
    try:
        identity = get_jwt_identity()
        results = contracts_schema.dump(ContractsModel.query.filter_by(user_id=identity['id']).all())
        if len(results) == 0:
            return jsonify({'status': 404, 'message': "No matches found"}), 404
        return jsonify({'status': 200, 'data': results}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/contracts/<int:id_>', methods=['GET'])
@jwt_required()
def get_contract(id_):
    results = contract_schema.dump(ContractsModel.query.get(id_))
    if len(results) == 0:
        return jsonify({'status': 404, 'message': "Contract is not found"}), 404
    return jsonify({'status': 200, 'data': results}), 200


@app.route('/api/v1.0/contracts/<int:id_>', methods=['DELETE'])
@jwt_required()
def delete_contract(id_):
    try:
        contract = ContractsModel.query.get_or_404(id_)
        if contract.user_id != get_jwt_identity()['id']:
            raise ValueError
        db.session.delete(contract)
        db.session.commit()
        return jsonify({'status': 200, 'message': "Contract has been successfully deleted."}), 200
    except Exception as e:
        return jsonify({'status': 404, 'message': 'Contract not found!'}), 404


@app.route('/api/v1.0/jwt_test', methods=['GET'])
@jwt_required()
def test():
    user = get_jwt_identity()
    email = user['email']
    return jsonify({"status": 200, "message": f'Welcome to the protected route {email}!'}), 200
