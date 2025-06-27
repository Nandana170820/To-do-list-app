document.addEventListener('DOMContentLoaded', loadTodos);

function loadTodos() {
    fetch('http://127.0.0.1:5000/todos')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('todo-list');
            list.innerHTML = '';
            data.forEach(todo => {
                const li = document.createElement('li');
                li.className = todo.completed ? 'completed' : '';
                li.innerHTML = `
                    <span>${todo.task}</span>
                    <button onclick="toggleDone(${todo.id}, ${todo.completed})">✔</button>
                    <button onclick="deleteTodo(${todo.id})">✖</button>
                `;
                list.appendChild(li);
            });
        });
}

function addTask() {
    const task = document.getElementById('taskInput').value;
    if (!task) return;
    fetch('http://127.0.0.1:5000/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    }).then(loadTodos);
    document.getElementById('taskInput').value = '';
}

function deleteTodo(id) {
    fetch(`http://127.0.0.1:5000/todos/${id}`, {
        method: 'DELETE'
    }).then(loadTodos);
}

function toggleDone(id, currentStatus) {
    fetch(`http://127.0.0.1:5000/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !currentStatus })
    }).then(loadTodos);
}
