from flask_restful import reqparse, abort, Resource
from flask import jsonify
from . import db_session, users

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('created_date', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(users.User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        one_user = session.query(users.User).get(user_id)
        return jsonify({'user': one_user.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password',
                  'created_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        one_user = session.query(users.User).get(user_id)
        session.delete(one_user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        all_users = session.query(users.User).all()
        return jsonify({'users': [user.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password',
                  'created_date')) for user in all_users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        added_user = users.User(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            created_date=args['created_date']
        )
        session.add(added_user)
        session.commit()
        return jsonify({'success': 'OK'})
