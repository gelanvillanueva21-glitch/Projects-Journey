

// VARIABLES


const deleteConfirmWindow = document.querySelector('.delete-confirm-popup');
const confirmNo = document.querySelector('.delete-confirm-no');
const confirmYes = document.querySelector('.delete-confirm-yes');

const checkBox = document.getElementById('show-password-checkbox');
const id = document.getElementById('id');
const username = document.getElementById('username');
const password = document.getElementById('password');
const logInBtn = document.getElementById('log-in');

const errorWindow = document.querySelector('.error-popup');
const errorCloseBtn2 = document.querySelector('.error-close');
const addButton = document.getElementById('add-btn');
const addInputList = document.getElementById('to-do-list-title');
const toDoList = document.querySelector('.list-box ul');
const notiWindow = document.querySelector('.popup-notification');
const alreadyExistWindow = document.querySelector('.duplicate-popup');
const closeBtn = document.querySelector('.duplicate-close');
const logInError = document.querySelector('.login-error-popup');
const windowSignIn = document.querySelector('.window-box-sign-in');
const tryAgainBtn = document.querySelector('.login-error-close');
var trashBtn = null
let globalId = null

// CHECK IF ALREADY LOG IN THIS DEVICE

window.addEventListener('DOMContentLoaded', async () => {

    const savedId = localStorage.getItem('id');
    if (!savedId) { return }
    globalId = Number(savedId);

    try {

        let result = await fetch(`http://127.0.0.1:8000/GetItems?id=${globalId}`);

        if (!result.ok) {
            throw new Error("Something error occured During fetching data");
        }
        windowSignIn.style.display = 'none';
        let data = await result.json();
        let itemList = data["item-list"];
        let checkedList = data["checked-item"];
        console.log("Item List: " ,itemList);
        console.log("Check List :" , checkedList);

        if (itemList.length !== 0) {
            itemList.forEach((list) => {
                let li = document.createElement('li');
                li.classList.add('list');
                let btn = document.createElement('button');
                btn.classList.add('trash-btn');
                let img = document.createElement('img');
                img.src = '../Images/trash.svg';
                img.classList.add('image');
                btn.appendChild(img);
                li.innerText = list
                li.appendChild(btn);
                toDoList.appendChild(li);
            })
        }

        if (checkedList.length === 0) { return }
            let allNotes = document.querySelectorAll('.list-box ul li.list');
            allNotes.forEach((item) => {
            tempItem = item.childNodes[0].textContent.trim();
            if (checkedList.includes(tempItem)) {
                item.classList.add('completed');
                item.style.borderColor = '#10b981';
            }
        })

    } catch (error) {
        errorWindow.style.display = 'block';
    }

})


// SHOW PASSWORD LAYER

checkBox.addEventListener('change', () => {

    if (checkBox.checked) {
        password.type = 'text';
    } else {
        password.type = 'password';
    }

});

// 

errorCloseBtn2.addEventListener('click', function() {
    errorWindow.style.display = 'none';
})


// AUTHENTICATION HANDLE

logInBtn.addEventListener('click', async function() {
    try {
        let tempUserId = Number(id.value);
        let tempUsername = username.value;
        let tempPassword = password.value;

        let result = await fetch('http://127.0.0.1:8000/Login', {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                userId : tempUserId,
                username : tempUsername,
                password : tempPassword
            })
        });

        if (!result.ok) {
            throw new Error("Invalid credentials or server error");
        }

        const data = await result.json();
        if (data['status']) {
            windowSignIn.style.display = 'none';
            let userList = data['todo_list'];
            let checkedList = data['checked_list'];
            localStorage.setItem('id' , tempUserId);
            globalId = tempUserId
            if (userList.length === 0) { return }
            
            userList.forEach((list) => {
                let li = document.createElement('li');
                li.classList.add('list');
                let btn = document.createElement('button');
                btn.classList.add('trash-btn');
                let img = document.createElement('img');
                img.src = '../Images/trash.svg';
                btn.appendChild(img);
                img.classList.add('image');
                li.innerText = list;
                li.appendChild(btn);
                toDoList.appendChild(li);
            })

            if (checkedList.length === 0) { return }
            let allNotes = document.querySelectorAll('.list-box ul li.list');
            allNotes.forEach((item) => {
                tempItem = item.childNodes[0].textContent.trim();
                if (checkedList.includes(tempItem)) {
                    item.classList.add('completed');
                    item.style.borderColor = '#10b981';
                }
            })
        }
        
    } catch (error) {
        logInError.style.display = 'block';
    }


});

tryAgainBtn.addEventListener('click', function() {
    logInError.style.display = 'none';
})


// ADD LIST LAYER 

addButton.addEventListener('click', async () => {

    if (addInputList.value) {
        const allList = document.querySelectorAll('.list-box ul li.list');
        let isAlreadyExist = false;
        allList.forEach((list) => {
            if (list.innerText === addInputList.value) {
                isAlreadyExist = true
                alreadyExistWindow.style.display = 'block';
                return
            }
        })
        if (!isAlreadyExist) {
            let li = document.createElement('li');
            li.classList.add('list');
            let btn = document.createElement('button');
            btn.classList.add('trash-btn');
            let img = document.createElement('img');
            img.src = '../Images/trash.svg';
            btn.appendChild(img);
            img.classList.add('image');
            li.innerText = addInputList.value;
            li.appendChild(btn);

            toDoList.appendChild(li);
            try {
                
                let data = await fetch("http://127.0.0.1:8000/AddItem", {
                    method : 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body : JSON.stringify({
                        item : addInputList.value,
                        id : globalId
                    })
                })
                
                if (!data.ok) {
                    throw new Error("Error Occured while fetching a data");
                }

                let result = await data.json();
                if (result["status"]) {
                    notiWindow.style.display = 'block';
                }
            } catch (error) {
                errorWindow.style.display = 'none';
            }
        }
    }
});

window.addEventListener('click', (e) => {

    if (event.target.classList.contains('popup-notification')) {
        notiWindow.style.display = 'none';
    }

    if (event.target.classList.contains('duplicate-popup')) {
        alreadyExistWindow.style.display = 'none';
    }

})

closeBtn.addEventListener('click', () => {

    alreadyExistWindow.style.display = 'none';

});


// DELETE LIST COMPONENTS LAYER

let elementPending = null
const ulBox = document.querySelector('.list-box ul');


ulBox.addEventListener('click', async (e) => {

    const trashBtn = e.target.closest('.trash-btn');

    if (trashBtn) {
        let parentTrashBtn = trashBtn.parentElement;
        elementPending = parentTrashBtn.childNodes[0].textContent.trim();
        deleteConfirmWindow.style.display = 'block';
    }
    if (!trashBtn) {
        const allList = document.querySelectorAll('.list-box ul li.list');
        let updatedCheckList = [];
        e.target.classList.toggle('completed');
        if (e.target.classList.contains('completed')) {
            e.target.style.borderColor = '#10b981';
        }
        else {
            e.target.style.borderColor = '';
        }

        allList.forEach((item) => {
            if (item.classList.contains('completed')) {
                updatedCheckList.push(item.childNodes[0].textContent.trim());
            }
        })
        console.log("Updated List: ", updatedCheckList);

        try {
            
            let result = await fetch("http://127.0.0.1:8000/UpdateChecked", {
                method : "PUT",
                headers : {'Content-Type' : 'application/json'},
                body : JSON.stringify({
                    checked_list : updatedCheckList,
                    id : globalId
                })
            })

            if (!result.ok) {
                throw new Error("Error Occurred During Fetching Data");
            }
        } catch (error) {
            errorWindow.style.display = 'block';
        }
    } 
})


confirmNo.addEventListener('click', () => {
    deleteConfirmWindow.style.display = 'none';
})

confirmYes.addEventListener('click', async () => {
    const allList = document.querySelectorAll('.list-box ul li.list');
    const listBox = document.querySelector('.list-box ul');
    const updatedList = []
    allList.forEach((item) => {
        if (elementPending !== item.childNodes[0].textContent.trim()) {
            let cleanItem = item.childNodes[0].textContent.trim();
            updatedList.push(cleanItem);
        }
    })
    listBox.innerHTML = '';
    if (updatedList.length === 0) { return }

    updatedList.forEach((item) => {
        let li = document.createElement('li');
        li.classList.add('list');
        let btn = document.createElement('button');
        btn.classList.add('trash-btn');
        let img = document.createElement('img');
        img.src = '../Images/trash.svg';
        btn.appendChild(img);
        img.classList.add('image');
        li.innerText = item
        li.appendChild(btn)
        listBox.appendChild(li);
    })


    try {
        
        let result = await fetch('http://127.0.0.1:8000/DeleteList', {
            method : 'PUT',
            headers : {'Content-Type' : 'application/json'},
            body : JSON.stringify({
                todo_list : updatedList,
                deleted_list : elementPending,
                id : globalId
            })
        });

        if (!result.ok) {
            throw new Error("Error Occurred During Fetching Data");
        }
        let data = await result
        deleteConfirmWindow.style.display = 'none';

    } catch (error) {
        errorWindow.style.display = 'block';
    }


    deleteConfirmWindow.style.display = 'none'
})
