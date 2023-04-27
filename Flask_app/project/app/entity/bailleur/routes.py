from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


bai_l = db.collection('bailleur')





bailleur =Blueprint('bailleur',__name__)

@bailleur.route('/bailleur/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in bai_l.stream()][-1]['id']
        id=str(int(id)+1)
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        todo = bai_l.document(id).get()
        if  todo.to_dict() is None :
            bai_l.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@bailleur.route('/bailleur/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in bai_l.stream()]
    return jsonify(all_todos), 200

@bailleur.route('/bailleur/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = bai_l.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@bailleur.route('/bailleur/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = bai_l.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            bai_l.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@bailleur.route('/bailleur/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = bai_l.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        bai_l.document(todo_id).delete()
        return jsonify({"success": True}), 200