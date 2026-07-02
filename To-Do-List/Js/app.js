

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
            if (userList === []) {
                return
            }
            
            userList.forEach((list) => {
                let li = document.createElement('li');
                li.classList.add('list');
                let btn = document.createElement('button');
                btn.classList.add('trash-btn');
                let img = document.createElement('img');
                img.src = '../Images/trash.svg';
                btn.appendChild(img);
                img.classList.add('image');
                li.innerText = list
                li.appendChild(btn)
                let cleanItem = li.childNodes[0].textContent.trim();
                btn.addEventListener('click', () => {
                        setupDeletion(cleanItem);
                    });

                toDoList.appendChild(li);
            })
            globalId = tempUserId
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
            li.innerText = addInputList.value
            li.appendChild(btn)
            let cleanItem = li.childNodes[0].textContent.trim();
            btn.addEventListener('click', () => {
                setupDeletion(cleanItem);
            });

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
                    console.log(result["status"]);
                    notiWindow.style.display = 'block';
                }
            } catch (error) {
                console.log(error);
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


function setupDeletion(listItem) {
    elementPending = listItem;
    deleteConfirmWindow.style.display = 'block';
}

confirmNo.addEventListener('click', () => {
    deleteConfirmWindow.style.display = 'none';
})

confirmYes.addEventListener('click', () => {
    const allList = document.querySelectorAll('.list-box ul li.list');
    const listBox = document.querySelector('.list-box ul');
    const updatedList = []
    allList.forEach((item) => {
        if (elementPending !== item.childNodes[0].textContent.trim()) {
            let cleanItem = item.childNodes[0].textContent.trim();
            console.log(cleanItem);
            updatedList.push(cleanItem);
        }
    })
    listBox.innerHTML = '';
    if (updatedList === []) {
        return
    }

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
    deleteConfirmWindow.style.display = 'none'
})
