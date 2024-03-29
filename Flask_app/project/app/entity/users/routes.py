from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from firebase_admin import credentials, firestore
import requests

agent_sec = db.collection('partcipants')





users =Blueprint('users',__name__)

@users.route('/participant/ajouter', methods=['POST'])
def create():
    temp,parti=agent_sec.add(request.json)
    todo = agent_sec.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

"""
@users.route('/participant/tous/<start>/<limit>', methods=['GET'])
def read(start,limit):
    if start !='0':
        last_doc=agent_sec.document(start).get()
        last_email=last_doc.to_dict()['email']   
        last_tel=last_doc.to_dict()['telephone']   
        sec=agent_sec.order_by('email').order_by('telephone').start_after({'email':last_email,'telephone':last_tel}).limit(int(limit))
        
        all_todos = [doc.to_dict() for doc in sec.stream()]
        return jsonify(all_todos), 200
    else:
        sec=agent_sec.order_by('email', direction=firestore.Query.ASCENDING).order_by('telephone', direction=firestore.Query.ASCENDING).limit(int(limit))
        all_todos = [doc.to_dict() for doc in sec.stream()]
        return jsonify(all_todos), 200
        #all_todos = [doc.to_dict() for doc in agent_sec.stream()]
    
    return  401

    all_todos = [doc.to_dict() for doc in agent_sec.stream()]"""
@users.route('/participant/tous', methods=['GET'])
def read():
    #all_todos = [doc.to_dict() for doc in agent_sec.stream()]
    all_todos=[]
    for doc in agent_sec.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        
        URL="http://195.15.218.172/participant/extension/"+v["extension_de_la_voie"]
        r = requests.get(url=URL)
          
        v["extension_de_la_voie"]=r.json()
    
        URL="http://195.15.218.172/participant/voie/"+v["type_de_voie"]
        r = requests.get(url=URL)
        v["type_de_voie"]=r.json()
        
        all_todos.append(v)
    return jsonify(all_todos), 200


@users.route('/participant/tous/user/<ide>', methods=['GET'])
def read_user(ide):
    #all_todos = [doc.to_dict() for doc in agent_sec.stream()]
    all_todos=[]
    for doc in agent_sec.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        if v["iduser"] == ide:
            v["id"]=doc.id
            
            URL="http://195.15.218.172/participant/extension/"+v["extension_de_la_voie"]
            r = requests.get(url=URL)
            
            v["extension_de_la_voie"]=r.json()
        
            URL="http://195.15.218.172/participant/voie/"+v["type_de_voie"]
            r = requests.get(url=URL)
            v["type_de_voie"]=r.json()
            
            all_todos.append(v)
    return jsonify(all_todos), 200

@users.route('/participant/tous/client/<ide>', methods=['GET'])
def read_client(ide):
    #all_todos = [doc.to_dict() for doc in agent_sec.stream()]
    all_todos=[]
    for doc in agent_sec.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        if v["compte_client"]["_id"] == ide:
            v["id"]=doc.id
            
            URL="http://195.15.218.172/participant/extension/"+v["extension_de_la_voie"]
            r = requests.get(url=URL)
            
            v["extension_de_la_voie"]=r.json()
        
            URL="http://195.15.218.172/participant/voie/"+v["type_de_voie"]
            r = requests.get(url=URL)
            v["type_de_voie"]=r.json()
            
            all_todos.append(v)
    return jsonify(all_todos), 200
    

@users.route('/participant/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = agent_sec.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@users.route('/participant/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = agent_sec.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            agent_sec.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@users.route('/participant/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = agent_sec.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        agent_sec.document(todo_id).delete()
        return jsonify({"success": True}), 200
