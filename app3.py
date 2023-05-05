from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

@app.get("/get_todo")
def get_user():
    url = "http://127.0.0.1:5000/todo"

    response = requests.get(url)
    response_json = response.json()
    return jsonify(
        response_json
    )


@app.post("/create_post")
def post_todo():
    data = request.get_json()   
    print(data)

    response = requests.post('http://127.0.0.1:5000/create_todo', json=data)


    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Error creating post.'}), 500


@app.put("/update_t/<int:todo_id>")
def put_todo(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'})
    
    #headers = {'Content-type': 'application/json; charset=UTF-8'}

    response = requests.put(f'http://127.0.0.1:5000/todo/{todo_id}',json=data)

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Error creating post.'}), 500



@app.delete("/delete_todo/<int:todo_id>")
def delete_todo(todo_id):
    response = requests.delete(f'http://127.0.0.1:5000/todo/{todo_id}')
    #return{"messsage":"Item deleted"}

    # We'll return the status code from the response as a response to our own request.
    return jsonify(response.json())























if __name__ == '__main__':
    #with app.app_context():
       # db.create_all()
    app.run(debug=True,port=5001)
