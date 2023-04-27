from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


prop_ = db.collection('info_bancaire')





prop=Blueprint('proprietaire',__name__)

@prop.route('/info_bancaire/ajouter', methods=['POST'])
def create():
    temp,parti=prop_.add(request.json)
    todo = prop_.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200
    

@prop.route('/info_bancaire/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in prop_.stream()]
    return jsonify(all_todos), 200

@prop.route('/info_bancaire/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = prop_.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@prop.route('/proprietaire/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = prop_.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            prop_.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@prop.route('/proprietaire/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = prop_.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        prop_.document(todo_id).delete()
        return jsonify({"success": True}), 200