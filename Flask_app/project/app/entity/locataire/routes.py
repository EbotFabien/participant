from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


loc_a = db.collection('locataire')





locataire =Blueprint('locataire',__name__)

@locataire.route('/locataire/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        todo = loc_a.document(id).get()
        if  todo.to_dict() is None :
            loc_a.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@locataire.route('/locataire/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in loc_a.stream()]
    return jsonify(all_todos), 200

@locataire.route('/locataire/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = loc_a.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@locataire.route('/locataire/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = loc_a.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            loc_a.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@locataire.route('/locataire/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = loc_a.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        loc_a.document(todo_id).delete()
        return jsonify({"success": True}), 200