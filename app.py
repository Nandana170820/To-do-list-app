from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize DB
def init_db():
    with sqlite3.connect("todos.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0
            )
        ''')

init_db()

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = sqlite3.connect("todos.db")
    cursor = conn.execute("SELECT * FROM todos")
    todos = [{"id": row[0], "task": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    conn = sqlite3.connect("todos.db")
    conn.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (data["task"], False))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo added"}), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    conn = sqlite3.connect("todos.db")
    conn.execute("UPDATE todos SET completed = ? WHERE id = ?", (data["completed"], todo_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo updated"})

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = sqlite3.connect("todos.db")
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Todo deleted"})

if __name__ == "__main__":
    app.run(debug=True)
    
    # Add this inside app.py (below your existing routes)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    with sqlite3.connect("todos.db") as conn:
        conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
    return jsonify({'message': 'Deleted'}), 200

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    completed = data.get('completed', False)
    with sqlite3.connect("todos.db") as conn:
        conn.execute('UPDATE todos SET completed = ? WHERE id = ?', (completed, todo_id))
        conn.commit()
    return jsonify({'message': 'Updated'}), 200

