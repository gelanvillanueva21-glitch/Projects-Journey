// VARIABLES

const errorP = document.getElementById('error-paragraph');
const emptyInputWindow = document.querySelector('.empty-fields-popup');
const emptyWindowCloseBtn = document.querySelector('.empty-close');
const emptyWindowTryAgainBtn = document.querySelector('.empty-fields-try-again');
const errorPopup = document.querySelector('.error-occurred-popup');
const errorCloseBtn2 = document.querySelector('.error-occurred-close');
const errorTryAgainBtn = document.querySelector('.error-occurred-retry');
const alreadyExistBtn = document.querySelector('.account-exists-content');
const successContinueBtn = document.querySelector('.account-success-continue');
const successBtn = document.querySelector('.account-success-close');
const succesWindow = document.querySelector('.account-success-popup');
const showPass = document.getElementById('create-show-password-checkbox');
const accountAlreadyExistWindow = document.querySelector('.account-exists-popup');
const alreadyExistTryAgainBtn = document.querySelector('.account-exists-try-again');
const createId = document.getElementById('create-id');
const createUser = document.getElementById('create-username');
const createPass = document.getElementById('create-password');
const createAccBtn = document.getElementById('create-account-btn');

// EMPTY INPUT WINDOW POP UP

emptyWindowCloseBtn.addEventListener('click', () => {
    emptyInputWindow.style.display = 'none';
})

emptyWindowTryAgainBtn.addEventListener('click', () => {
    emptyInputWindow.style.display = 'none';
})


// ALREADY EXIST POP UP WINDOW

alreadyExistTryAgainBtn.addEventListener('click', () => {
    accountAlreadyExistWindow.style.display = 'none';
})

alreadyExistBtn.addEventListener('click', () => {
    accountAlreadyExistWindow.style.display = 'none';
})

createAccBtn.addEventListener('click', async () => {
    try {
        
        if (createId.value === '' || createUser.value === '' || createPass.value === '') {
            emptyInputWindow.style.display = 'block';
            return
        }

        let temporaryId = Number(createId.value);
        let temporaryUsername = createUser.value;
        let temporaryPassword = createPass.value;

        let result = await fetch("http://127.0.0.1:8000/Register", {
            method : "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                userId : temporaryId,
                username : temporaryUsername,
                password : temporaryPassword
            })
        })

        if (!result.ok) {
            if (result.status === 422) {
                throw new Error(`Invalid Data Format: Correctly Fix it To Identify`);
            }
            accountAlreadyExistWindow.style.display = 'block';
            return
        }

        let data = await result.json();
        succesWindow.style.display = 'block';

    } catch (error) {
        errorP.innerText = error.message;
        errorPopup.style.display = 'block';
    }
})

// SHOW PASSWORD TEXT

showPass.addEventListener('change', () => {
    if (showPass.checked) {
        createPass.type = 'text';
    } else {
        createPass.type = 'password';
    }
})


// SUCCESS WINDOW POP UP

successBtn.addEventListener('click', () => {
    succesWindow.style.display = 'none';
})

successContinueBtn.addEventListener('click', () => {
    window.location.href = '../Html/index.html';
    succesWindow.style.display = 'none';
})


// ERROR OCCURED WINDOW

errorCloseBtn2.addEventListener('click', () => {
    errorPopup.style.display = 'none';
})

errorTryAgainBtn.addEventListener('click', () => {
    errorPopup.style.display = 'none';
})