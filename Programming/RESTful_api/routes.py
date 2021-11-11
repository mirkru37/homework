from flask import jsonify, request

import sql_query
from init import *
from Freelancer import Freelancer


def push_sql(sql, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
    return res


@app.route('/api/v1.0/freelancers', methods=['GET'])
def get_freelancers():
    try:
        sort_by = request.args.get('sort_by')
        sort_type = request.args.get('sort_type', default='desc')
        s = request.args.get('s')
        dummy = Freelancer.init_default()
        sql = sql_query.gen_search('freelancers', [x.split('__')[-1] for x in vars(dummy).keys()], sort_by, sort_type, s)
        results = push_sql(sql, mysql)
        if len(results) == 0:
            return jsonify({'status': 404, 'message': "No matches found"}), 404
        return jsonify({'status': 200, 'data': results}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['GET'])
def get_freelancer(id_):
    sql = sql_query.gen_search_by_field('freelancers', 'id', id_)
    results = push_sql(sql, mysql)
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
        sql = "INSERT INTO freelancers (id, name, email, phone_number, availability, salary, position)" \
             " VALUES (\"{}\", \"{}\", \"{}\", \"{}\", {}, {}, \"{}\");".format(*request.json.values())
        push_sql(sql, mysql)
        return jsonify({'status': 200, 'message': "Freelancer has been successfully created."}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['DELETE'])
def delete_freelancer(id_):
    try:
        if get_freelancer(id_)[1] == 404:
            return jsonify({'status': 404, 'message': "Freelancer is not found"}), 404
        sql = f"DELETE FROM freelancers WHERE id={id_}"
        push_sql(sql, mysql)
        return jsonify({'status': 200, 'message': "Freelancer has been successfully deleted."}), 200
    except Exception as e:
        return jsonify({'status': 404, 'message': str(e)}), 404


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['PUT'])
def update_freelancer(id_):
    try:
        # if id is not in table return
        if get_freelancer(id_)[1] == 404:
            return jsonify({'status': 404, 'message': "Freelancer is not found"}), 404
        dummy = Freelancer.init_default()
        exception_message = {}
        for i, field in enumerate(request.json.keys()):
            try:
                setattr(dummy, field, request.json[field])
            except ValueError as e:
                exception_message[field] = str(e)
        if exception_message:
            raise ValueError(exception_message)
        sql = "UPDATE freelancers SET"
        a = []
        for key, value in request.json.items():
            a.append(f" {key}='{value}' ")
        sql += ', '.join(a) + f" WHERE id={id_}"
        push_sql(sql, mysql)
        return jsonify({'status': 200, 'message': "Freelancer has been successfully updated."}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400
