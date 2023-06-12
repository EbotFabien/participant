from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


don_d = db.collection('voie')





voie =Blueprint('voie',__name__)

@voie.route('/voie/ajouter', methods=['POST'])
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

@voie.route('/voie/tous', methods=['GET'])
def read():
    all_todos = []
    #return jsonify(all_todos), 200
    for doc in don_d.stream():
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        #all_todos = [[doc.to_dict(),doc.id] for doc in clien_t.stream()]
    return jsonify(all_todos), 200

@voie.route('/voie/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = don_d.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@voie.route('/voie/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = don_d.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            don_d.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@voie.route('/voie/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = don_d.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        don_d.document(todo_id).delete()
        return jsonify({"success": True}), 200