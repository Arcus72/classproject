const API_URL = 'http://127.0.0.1:5000';
const inputField = document.querySelector('input');
const addButton = document.querySelector('button');

addButton.addEventListener('click',  () => {
    const inputValue = inputField.value || "";
    sendData(inputValue);
    inputField.value = "";
})


async function sendData(inputValue) {

    const response = await fetch("http://127.0.0.1:5000/api/data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: inputValue })
    });

    if (response.ok) {
       fetchTodos();
    } else {
        console.error("Error sending data:", response.statusText);
    }

}

const addItemToList = (list, item) => {
    const li = document.createElement('li');
    li.textContent = item[1];
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = () => deleteItem(item[0]);
    li.appendChild(deleteBtn);
    list.appendChild(li);
}

async function fetchTodos() {
    const response = await fetch(`${API_URL}/api/data`);
    const todos = await response.json();
    const list = document.getElementById('shoplist');
    list.innerHTML = '';
    todos.forEach(todo => {
        addItemToList(list, todo);
    });
}

async function deleteItem(id) {
    const response = await fetch(`${API_URL}/api/data/${id}`, {
        method: 'DELETE'
    });
    if (response.ok) {
        fetchTodos();
    } else {
        console.error('Failed to delete item');
    }


}

fetchTodos();

