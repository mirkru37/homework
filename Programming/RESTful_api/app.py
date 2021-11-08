#!flask/bin/python
from flask import Flask, jsonify, abort, request
from flask_mysqldb import MySQL
from Freelancer import Freelancer
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/api/v1.0/index'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Freelancer-api"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'UniversityDB'

mysql = MySQL(app)


@app.route('/api/v1.0/freelancers', methods=['GET'])
def get_freelancers():
    try:
        sort_by = request.args.get('sort_by')
        sort_type = request.args.get('sort_type', default='desc')
        s = request.args.get('s')
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM freelancers"
        if s:
            sql += f" WHERE name LIKE '%{s}%' OR id LIKE '%{s}%' OR email LIKE '%{s}%' OR phone_number LIKE '%{s}%' " \
                   f" OR availability LIKE '%{s}%'  OR salary LIKE '%{s}%'  OR position LIKE '%{s}%'"
        if sort_by:
            if sort_type.lower() not in ['asc', 'desc']:
                sort_type = 'desc'
            sql += f" ORDER BY {sort_by} {sort_type}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            return jsonify({'status': 404, 'message': "No matches found"}), 404
        return jsonify({'status': 200, 'data': results}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['GET'])
def get_freelancer(id_):
    cursor = mysql.connection.cursor()
    sql = f"SELECT * FROM freelancers WHERE id={id_}"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
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
        # freelancer = Freelancer(request.json['id'], request.json['name'], request.json['email'],
        #                         request.json['phone_number'], request.json['availability'], request.json['salary'],
        #                         request.json['position'])
        sql = "INSERT INTO freelancers (id, name, email, phone_number, availability, salary, position)" \
             " VALUES (\"{}\", \"{}\", \"{}\", \"{}\", {}, {}, \"{}\");".format(*request.json.values())
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 200, 'message': "Freelancer has been successfully created."}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


@app.route('/api/v1.0/freelancers/<int:id_>', methods=['DELETE'])
def delete_freelancer(id_):
    try:
        if get_freelancer(id_)[1] == 404:
            return jsonify({'status': 404, 'message': "Freelancer is not found"}), 404
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM freelancers WHERE id={id_}"
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
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
        cursor = mysql.connection.cursor()
        sql = "UPDATE freelancers SET"
        a = []
        for key, value in request.json.items():
            a.append(f" {key}='{value}' ")
        sql += ', '.join(a) + f" WHERE id={id_}"
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'status': 200, 'message': "Freelancer has been successfully updated."}), 200
    except Exception as e:
        return jsonify({'status': 400, 'message': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
