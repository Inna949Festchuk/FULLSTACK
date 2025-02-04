from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import DisconnectionError, IntegrityError

from models import Session, User
from shema import CreatUser, UpdateUser

app = Flask("my_server")
bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes)
    password_hashed = password_hashed_bytes.decode()
    return password_hashed


def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(hashed_password, password)


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


def validate(schema_cls: type[CreatUser] | type[UpdateUser], json_data):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)


@app.before_request
def before_requests():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response):
    request.session.close()
    return http_response


def add_user(user):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError as er:
        raise HttpError(409, "user already exist")


def get_user_by_id(user_id) -> User:
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(CreatUser, request.json)
        user = User(
            name=json_data["name"], password=hash_password(json_data["password"])
        )
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        json_data = validate(UpdateUser, request.json)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user_by_id(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
            add_user(user)
        return user.dict

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})


user_view = UserView.as_view("user")

app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/user", view_func=user_view, methods=["POST"])
app.run()
