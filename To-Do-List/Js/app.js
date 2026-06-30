

// VARIABLES

const checkBox = document.getElementById('show-password-checkbox');
const id = document.getElementById('id');
const username = document.getElementById('username');
const password = document.getElementById('password');
const logInBtn = document.getElementById('log-in');

const addButton = document.getElementById('add-btn');
const addInputList = document.getElementById('to-do-list-title');
const toDoList = document.querySelector('.list-box ul');
const notiWindow = document.querySelector('.popup-notification');
const alreadyExistWindow = document.querySelector('.duplicate-popup');
const closeBtn = document.querySelector('.duplicate-close');
const logInError = document.querySelector('.login-error-popup');
const windowSignIn = document.querySelector('.window-box-sign-in');
const tryAgainBtn = document.querySelector('.login-error-close');


// SHOW PASSWORD LAYER

checkBox.addEventListener('change', () => {

    if (checkBox.checked) {
        password.type = 'text';
    } else {
        password.type = 'password';
    }

});


// AUTHENTICATION HANDLE

logInBtn.addEventListener('click', async function() {
    try {
        let tempUser = Number(id.value);
        let tempUsername = username.value;
        let tempPassword = password.value;

        let result = await fetch('http://127.0.0.1:8000/Login', {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                userId : tempUser,
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
                toDoList.appendChild(li);
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

addButton.addEventListener('click', () => {

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
            toDoList.appendChild(li);
            notiWindow.style.display = 'block';
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