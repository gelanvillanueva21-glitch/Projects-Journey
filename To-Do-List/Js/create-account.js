// VARIABLES

const showPass = document.getElementById('create-show-password-checkbox');
const accountAlreadyExistWindow = document.querySelector('.account-exists-popup');
const alreadyExistTryAgainBtn = document.querySelector('.account-exists-try-again');
const createId = document.getElementById('create-id');
const createUser = document.getElementById('create-username');
const createPass = document.getElementById('create-password');
const createAccBtn = document.getElementById('create-account-btn');


// ALREADY EXIST POP UP WINDOW

alreadyExistTryAgainBtn.addEventListener('click', () => {
    accountAlreadyExistWindow.style.display = 'none';
})

createAccBtn.addEventListener('click', async () => {
    try {
        
        let temporaryId = Number(createId.value);
        let temporaryUsername = createUser.value;
        let temporaryPassword = createPass.value;

        let result = await fetch("http://127.0.0.1:8000", {
            method : "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                
            })
        })

    } catch (error) {
        accountAlreadyExistWindow.style.display = 'block';
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
