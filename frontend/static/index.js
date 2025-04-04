const API_URL = 'http://127.0.0.1:5000';
const inputField = document.querySelector('input');
const addButton = document.querySelector('button');
const list = document.getElementById('shoplist');

addButton.addEventListener('click', async () => {
    const inputValue = inputField.value.trim();
    if (inputValue) {
        await sendItem(inputValue);
        inputField.value = '';
    }
});

async function sendItem(inputValue) {
    const response = await fetch(`${API_URL}/api/data`);
    let data = await response.json();
    let items = data.messages || [];

    items.push(inputValue);

    await fetch(`${API_URL}/api/data`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: items }),
    });

    fetchTodos();
}

function addItemToList(index, item) {
    const li = document.createElement('li');
    li.textContent = item;
    li.setAttribute('data-index', index);

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = () => deleteItem(index);

    li.appendChild(deleteBtn);
    list.appendChild(li);
}

async function fetchTodos() {
    const response = await fetch(`${API_URL}/api/data`);
    const data = await response.json();
    const items = data.messages || [];

    list.innerHTML = '';
    items.forEach((item, index) => {
        addItemToList(index, item);
    });
}

async function deleteItem(index) {
    const response = await fetch(`${API_URL}/api/data`);
    let data = await response.json();
    let items = data.messages || [];

    items.splice(index, 1);

    await fetch(`${API_URL}/api/data`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: items }),
    });

    fetchTodos();
}

fetchTodos();
