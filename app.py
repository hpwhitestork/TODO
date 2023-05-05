from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields, validate, ValidationError
from flask_smorest import Blueprint , abort
import requests
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/Todo'
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__="Todo_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tittle = db.Column(db.String(100))
    completed = db.Column(db.String(100))

class TodoSchema(Schema):
    id=fields.Integer()
    name=fields.String(validate=validate.Length(min=1),)
    tittle=fields.String(validate=validate.Length(min=1,max=200),error_messages={"required": "Please enter valid length (max length is 3)"})
    completed=fields.String(validate=validate.Length(min=1))

@app.get("/todo")
def todo_all():
    todo_data=Todo.query.all()

    serializer=TodoSchema(many=True)

    data=serializer.dump(todo_data)

    return jsonify(
        data
    )

@app.get("/todo/<int:todo_id>")
def todo_by_id(todo_id):
    todo_data=Todo.query.get(todo_id)

    serializer=TodoSchema()

    data=serializer.dump(todo_data)

    return jsonify(
        data
    ),200


@app.post("/create_todo")
def create_todo():
    data = request.get_json()
    if (
        "name" not in data 
        or "tittle" not in data
        or "completed" not in data
    ):
        abort(
            400,
            message="Bad request. Ensure 'name', 'tittle', and 'completed' are included in the JSON payload.",
        )
    try:
        TodoSchema().load(data)
    except ValidationError as err:
        return jsonify({'message':"Please does not empty any field"}),404

    #print(data, "request")
    user = Todo(**data)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Todo created  successfully.'}), 200


@app.put("/todo/<int:todo_id>")
def update_todo(todo_id):
    todo_data = Todo.query.filter_by(id=todo_id).first()
    print(todo_id)
    if not todo_data:
       return jsonify({'message': 'Todo not found.'}), 404
    data = request.get_json()
    todo_data.name = data['name']
    todo_data.tittle = data['tittle']
    todo_data.completed = data['completed']
    db.session.commit()
    
    return jsonify({'message': 'Item updated successfully.'}), 200

@app.delete("/todo/<int:todo_id>")
def delete_user(todo_id):
    
    user = Todo.query.filter_by(id=todo_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return{"messsage":"Item deleted"}
    
    return{"message":"Item not found"}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5000)


