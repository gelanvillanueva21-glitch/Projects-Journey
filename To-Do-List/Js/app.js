

// VARIABLES

const checkBox = document.getElementById('show-password-checkbox');
const password = document.getElementById('password');
const addButton = document.getElementById('add-btn');
const addInputList = document.getElementById('to-do-list-title');
const toDoList = document.querySelector('.list-box ul');
const notiWindow = document.querySelector('.popup-notification');
const alreadyExistWindow = document.querySelector('.duplicate-popup');
const closeBtn = document.querySelector('.duplicate-close');


// SHOW PASSWORD LAYER

checkBox.addEventListener('change', () => {

    if (checkBox.checked) {
        password.type = 'text';
    } else {
        password.type = 'password';
    }

});


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