from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


prop_ = db.collection('proprietaire')





prop=Blueprint('proprietaire',__name__)

@prop.route('/proprietaire/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        todo = prop_.document(id).get()
        if  todo.to_dict() is None :
            prop_.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@prop.route('/proprietaire/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in prop_.stream()]
    return jsonify(all_todos), 200

@prop.route('/proprietaire/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = prop_.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@prop.route('/proprietaire/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = prop_.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            don_d.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@prop.route('/proprietaire/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = prop_.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        prop_.document(todo_id).delete()
        return jsonify({"success": True}), 200