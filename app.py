from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
import random

# Kết nối MongoDB
client = MongoClient("mongodb+srv://dtc225201320:trang123@clusternv1.oxtkczh.mongodb.net/?retryWrites=true&w=majority&appName=Clusternv1")
db = client.camp2016
todos = db.todo

app = Flask(__name__)

title = "Danh sách nhân viên"
heading = "Quản lý nhân viên"

# Hàm sinh ID dạng NVxxxxxxxx
def generate_custom_id():
    return "NV" + ''.join(random.choices('0123456789', k=8))

# Hàm sinh ID không trùng
def generate_unique_id():
    while True:
        new_id = generate_custom_id()
        if not todos.find_one({"_id": new_id}):
            return new_id

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('tasks')

@app.route("/")
def tasks():
    todos_l = todos.find()
    return render_template('index.html', todos=todos_l, t=title, h=heading)

@app.route("/list")
def lists():
    todos_l = todos.find()
    return render_template('index.html', todos=todos_l, t=title, h=heading)

@app.route("/done")
def done():
    id = request.values.get("_id")
    task = todos.find_one({"_id": id})
    if task and task.get("done") == "yes":
        todos.update_one({"_id": id}, {"$set": {"done": "no"}})
    else:
        todos.update_one({"_id": id}, {"$set": {"done": "yes"}})
    return redirect(redirect_url())

@app.route("/action", methods=['POST'])
def action():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")  # "Nam" hoặc "Nữ"
    phone = request.values.get("phone")
    address = request.values.get("address")
    department = request.values.get("department")
    position = request.values.get("position")
    done = request.values.get("done")

    custom_id = generate_unique_id()

    todos.insert_one({
        "_id": custom_id,
        "name": name,
        "desc": desc,
        "date": date,
        "pr": pr,
        "phone": phone,
        "address": address,
        "department": department,
        "position": position,
        "done": done
    })
    return redirect("/")

@app.route("/remove")
def remove():
    key = request.args.get("_id")
    if key:
        result = todos.delete_one({"_id": key})
        if result.deleted_count == 0:
            return f"Không tìm thấy nhân viên có ID: {key}", 404
    else:
        return "Thiếu tham số _id", 400
    return redirect("/")

@app.route("/update")
def update():
    id = request.values.get("_id")
    task = todos.find_one({"_id": id})
    if not task:
        return "Không tìm thấy nhân viên!", 404

    return render_template('update.html', task=task, h=heading, t=title)

@app.route("/action3", methods=['POST'])
def action3():
    id = request.values.get("_id")
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")  # "Nam" hoặc "Nữ"
    phone = request.values.get("phone")
    address = request.values.get("address")
    department = request.values.get("department")
    position = request.values.get("position")
    done = request.values.get("done")

    todos.update_one({"_id": id}, {
        '$set': {
            "name": name,
            "desc": desc,
            "date": date,
            "pr": pr,
            "phone": phone,
            "address": address,
            "department": department,
            "position": position,
            "done": done
        }
    })
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    key = request.values.get("key")
    refer = request.values.get("refer")
    todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)

@app.route("/about")
def about():
    return render_template('credits.html', t=title, h=heading)

if __name__ == "__main__":
    env = os.environ.get('FLASK_ENV', 'development')
    port = int(os.environ.get('PORT', 5000))
    debug = False if env == 'production' else True
    app.run(host='0.0.0.0', port=port, debug=debug)

