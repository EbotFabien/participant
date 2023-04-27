from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


don_d = db.collection('donneur')





donneur =Blueprint('donneur',__name__)

@donneur.route('/donneur/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in don_d.stream()][-1]['id']
        id=str(int(id)+1)
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        todo = don_d.document(id).get()
        if  todo.to_dict() is None :
            don_d.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@donneur.route('/donneur/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in don_d.stream()]
    return jsonify(all_todos), 200

@donneur.route('/donneur/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = don_d.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@donneur.route('/donneur/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = don_d.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            don_d.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@donneur.route('/donneur/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = don_d.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        don_d.document(todo_id).delete()
        return jsonify({"success": True}), 200