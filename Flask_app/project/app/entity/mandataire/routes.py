from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


man_d = db.collection('Mandataire')





mandataire =Blueprint('mandataire',__name__)

@mandataire.route('/mandataire/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        todo = man_d.document(id).get()
        if  todo.to_dict() is None :
            man_d.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@mandataire.route('/mandataire/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in man_d.stream()]
    return jsonify(all_todos), 200

@mandataire.route('/mandataire/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = man_d.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@mandataire.route('/mandataire/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = man_d.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            man_d.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@mandataire.route('/mandataire/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = man_d.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        man_d.document(todo_id).delete()
        return jsonify({"success": True}), 200