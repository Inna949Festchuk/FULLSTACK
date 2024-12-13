from flask import Flask, jsonify, request
from flask.views import MethodView 
from models import Session, Press

from sqlalchemy.exc import IntegrityError

from shema import CreatPress, UpdatePress 
from pydantic import ValidationError

app = Flask("my_server") 

class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response 

def add_press(press):
    request.session.add(press)
    try:
        request.session.commit()
    except IntegrityError as er:
        raise HttpError(400, "Такой заголовок уже существует")

def validate(schema_cls: type[CreatPress] or type[UpdatePress], json_data):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for errors in errors:
            errors.pop("ctx", None)
        raise HttpError(400, errors)

@app.before_request
def before_requests():
    session = Session()
    request.session = session 

@app.after_request 
def affter_request(http_response):
    request.session.close()
    return http_response

def get_press_by_id(press_id) -> Press: 
    press = request.session.get(Press, press_id)
    if press is None:
        raise HttpError(404, "Объявление не найдено")
    return press
        
class PressView(MethodView):
    def get(self, press_id: int):
        press = get_press_by_id(press_id) 
        return jsonify(press.dict)

    def post(self):
        json_data = validate(CreatPress, request.json)
        press = Press(
            title=json_data['title'],
            body=json_data['body'],
            onwer=json_data['onwer']
        ) 
        add_press(press)
        return jsonify(press.dict)

    def patch(self, press_id: int):
        json_data = validate(UpdatePress, request.json)

        press = get_press_by_id(press_id) 
        for field, value in json_data.items():
            setattr(press, field, value)
            add_press(press)
        return jsonify(press.dict)

    def delete(self, press_id: int):
        press = get_press_by_id(press_id) 
        request.session.delete(press)
        request.session.commit() 
        return jsonify({"status": "deleted"})

press_view = PressView.as_view("press")

app.add_url_rule(
    "/press/<int:press_id>",
    view_func=press_view,
    methods=["GET", "PATCH", "DELETE"] 
)
app.add_url_rule(
    "/press", 
    view_func=press_view,
    methods=["POST"] 
)

app.run()