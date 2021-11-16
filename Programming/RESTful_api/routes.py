import werkzeug.exceptions
from flask import jsonify, request
from sqlalchemy import or_, desc
from FreelancerModel import *
from Freelancer import Freelancer


freelancer_schema = FreelancerSchema()
freelancers_schema = FreelancerSchema(many=True)


@app.route('/api/v1.0/freelancers', methods=['GET'])
def get_freelancers():
    try:
        sort_by = request.args.get('sort_by')
        sort_type = request.args.get('sort_type', default='desc')
        s = request.args.get('s')
        all_fr = FreelancerModel.query
        count = len(all_fr.all())
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
def get_freelancer(id_):
    results = freelancer_schema.dump(FreelancerModel.query.get(id_))
    if len(results) == 0:
        return jsonify({'status': 404, 'message': "Freelancer is not found"}), 404
    return jsonify({'status': 200, 'data': results}), 200


@app.route('/api/v1.0/freelancers', methods=['POST'])
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
def delete_freelancer(id_):
    try:
        freelancer = FreelancerModel.query.get_or_404(id_)
        db.session.delete(freelancer)
        db.session.commit()
        return jsonify({'status': 200, 'message': "Freelancer has been successfully deleted."}), 200
    except Exception as e:
        return jsonify({'status': 404, 'message': str(e)}), 404


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['PUT'])
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
