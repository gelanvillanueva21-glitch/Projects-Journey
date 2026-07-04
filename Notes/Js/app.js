

// VARIABLES
const titleBtn = document.getElementById('title-button');
const weatherBox = document.getElementById('weather-container');
const calculatorBox = document.getElementById('calculator-container');
const textArea = document.getElementById('note-content');
const searchBtn = document.getElementById('search-note');
const addBtn = document.getElementById('add-note');
const deleteBtn = document.querySelector('.delete-note');
const saveBtn = document.getElementById('save-note');
const windowSearch = document.getElementById('window-box-search');
const windowTitle = document.getElementById('window-title-box');
const windowDelete = document.getElementById('window-delete-confirm');
let savedList = document.getElementById('saved-note-list');
const searchInput = document.getElementById('search-note-title');
const searchTitleBtn = document.getElementById('search');
const titleInput = document.getElementById('add-notes-title');
const confirmBtn = document.getElementById('confirm-button');
let headingTitle = document.getElementById('heading-title');
let deleteNoteBtn = document.querySelectorAll('.delete-btn');
let activeNote = null;


// LOCAL STORAGE FILE

function saveNotesStorage() {
    let allNotes = document.querySelectorAll('.list');
    let notesArray = []

    allNotes.forEach(function(note){
        notesArray.push({
            id: note.id,
            content: note.dataset.content
        });
    });
    localStorage.setItem('note', JSON.stringify(notesArray));
}


// DISPLAY LIST

let notes = JSON.parse(localStorage.getItem('note')) || [];

notes.forEach(function(note) {

    let li = document.createElement('li');
    li.classList.add('list');
    li.id = note.id;
    li.innerText = note.id;
    li.dataset.content = note.content;
    savedList.appendChild(li);

});


titleBtn.addEventListener('click', function(){
    window.location.reload();
})



// WINDOW POP UP COMPONENTS

searchBtn.addEventListener('click', function(e){
    e.stopPropagation();
    windowSearch.style.display = 'block';

});

addBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    windowTitle.style.display = 'block';

})


// SEARCH NOTES


let highlightedNote = null;


searchTitleBtn.addEventListener('click', function(){


    if (highlightedNote) {
        highlightedNote.style.border = 'none';
    }

    if (searchInput.value === '') {
        alert('You must enter title to search');
    } else {
        const allNotes = document.querySelectorAll('.list');
        allNotes.forEach(function(note){
            if (['calculator', 'calculator app'].includes(searchInput.value.toLowerCase())) {
                headingTitle.innerText = searchInput.value.toUpperCase();
                textArea.style.display = 'none';
                calculatorBox.style.display =  'flex';
                note.style.borderColor = 'blue';
                note.style.borderStyle = 'solid';
                weatherBox.style.display = 'none';

                searchInput.value = '';
                windowSearch.style.display = 'none';
                highlightedNote = note;
            } else if (['weather app', 'weather'].includes(searchInput.value.toLowerCase())) {
                headingTitle.innerText = searchInput.value.toUpperCase();
                textArea.style.display = 'none';
                calculatorBox.style.display = 'none';
                weatherBox.style.display = 'block';

                note.style.borderColor = 'blue';
                note.style.borderStyle = 'solid';
                searchInput.value = '';
                windowSearch.style.display = 'none';
                highlightedNote = note;
            } else if (searchInput.value.toLowerCase() === note.innerText.toLowerCase()) {
                note.style.borderColor = 'blue';
                note.style.borderStyle = 'solid';
                searchInput.value = '';
                windowSearch.style.display = 'none';
                weatherBox.style.display = 'none';
                activeNote = note;

                headingTitle.innerText = note.innerText;
                textArea.value = note.dataset.content;
                highlightedNote = note;
            }
        });
    }


});



// ADD NOTES COMPONENTS



confirmBtn.addEventListener('click', function(){

    let allNotes = document.querySelectorAll('.list');
    if (titleInput.value === '') {
        alert('You must Enter a title word');
    } else {
        var isExist = true;
        allNotes.forEach(function(note) {
            if (note.innerText.toLowerCase() === titleInput.value.toLowerCase()) {
                isExist = false;
            }
        });
        if (isExist) {
            let li = document.createElement('li');
            li.innerText = titleInput.value;
            li.classList.add('list');
            li.id = titleInput.value;
            li.dataset.content = '';
            savedList.appendChild(li);
            titleInput.value = '';
            windowTitle.style.display = 'none';
            saveNotesStorage(); 
        } else {
            alert(`${titleInput.value} is Already Exist`);
        }
    }

});

window.addEventListener('click', function(e) {

    if (e.target === windowSearch) {
        windowSearch.style.display = 'none';
    } else if (e.target === windowTitle) {
        windowTitle.style.display = 'none';
    }

});


// ACTIVE NOTES


window.addEventListener('click', function(e) {

    const allNotes = document.querySelectorAll('.list');
    allNotes.forEach(function(note) {

        if (['calculator', 'calculator app'].includes(e.target.innerText.toLowerCase())) {
            headingTitle.innerText = e.target.innerText.toUpperCase();
            textArea.style.display = 'none';
            weatherBox.style.display = 'none';
            calculatorBox.style.display =  'flex';
        } else if (['weather app', 'weather'].includes(e.target.innerText.toLowerCase())) {
            headingTitle.innerText = e.target.innerText.toUpperCase();
            textArea.style.display = 'none';
            calculatorBox.style.display =  'none';
            weatherBox.style.display = 'block';
        } else if (e.target === note) {
            weatherBox.style.display = 'none';
            calculatorBox.style.display = 'none';
            textArea.style.display = 'inline-block';
            headingTitle.innerText = note.innerText;
            textArea.value = note.dataset.content;
            activeNote = note;
        }
    })
});


saveBtn.addEventListener('click', function(){
    if (activeNote) {
        activeNote.dataset.content = textArea.value;
        saveNotesStorage();
    }
});


// DELETE NOTES

let hasDeleteBtn = true;


deleteBtn.addEventListener('click', function(){

    const allNotes = document.querySelectorAll('.list');
    if (hasDeleteBtn)  {
        allNotes.forEach(function(note){
            let image = document.createElement('img');
            image.src = '../Image/trash-circle.svg';
            image.style.width = '30px';

            const button = document.createElement('button');
            button.classList.add('delete-note', 'delete-btn');
            button.appendChild(image);
            note.appendChild(button);
        })
        hasDeleteBtn = false;
    } else {
        const allBtn = document.querySelectorAll('.delete-btn');
        allBtn.forEach(function(note) {
            note.remove();
        })
        hasDeleteBtn = true;
    }
});


// function isDeleteBtn(button) {
//     deleteNoteBtn.forEach(function(noteBtn) {
//         if (button === noteBtn.parentElement.id) {
//             return true;
//         }
//     })
// }

let activeId = null;
const noBtn = document.getElementById('no');
const confirmButton = document.getElementById('confirm');


window.addEventListener('click', function(e) {

    let trashBtn = e.target.closest('.delete-btn');

    if(trashBtn) {
        activeId = trashBtn.parentElement;
        console.log(activeId);
        windowDelete.style.display = 'block';
    }
});

noBtn.addEventListener('click', function(){
    windowDelete.style.display = 'none';
});


confirmButton.addEventListener('click', function(){

    const allNotes = document.querySelectorAll('.list');
    allNotes.forEach(function(note){
        if (note.id === activeId.id) {
            note.remove();
            windowDelete.style.display = 'none';
        }
    });
    saveNotesStorage();

});


// CALCULATOR

// VARIABLE


const displayCalculate = document.getElementById('display-input');

function saveCalculate() {
    let allCalculateHistory = document.querySelectorAll('.second-list');
    let history = []

    allCalculateHistory.forEach((x) => {
        history.push(x.innerText);
    });
    localStorage.setItem('history', JSON.stringify(history));
}

function appendDisplay(input) {

    displayCalculate.value += input;
}

function deleteNumber() {
    let tempVar = displayCalculate.value;
    displayCalculate.value = tempVar.slice(0, -1);
}

let calculateHistoryBox = document.getElementById('history-box');


function calculate() {

    let isTrue = true;
    let expression = displayCalculate.value;

    try {
        const operation = {
            '+': (a, b) => a + b,
            '-': (a, b) => a - b,
            'x': (a, b) => a * b,
            '/': (a, b) => a / b
        };
        let tokens = [];
        let tempList = []

        for (let i = 0; i < expression.length; i++) {

            if (['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].includes(expression[i])) {
                tempList.push(expression[i]);
                if (!['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].includes(expression[i+1])) {
                    let result = tempList.join("");
                    tempList = []
                    tokens.push(result);
                }
            } else {
                if (expression[i] === '-') {
                    if (i === 0 || ['+', '-', 'x', '/'].includes(expression[i-1])) {
                        let num = '-';
                        i++;
                        while (i < expression.length && ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].includes(expression[i])) {
                            num += expression[i];
                            i++
                        }
                    tokens.push(num)
                    i--;
                    } else {
                        tokens.push('-');
                    }
                } else {
                    tokens.push(expression[i]);
                }
            }
        }
        console.log(tokens);
        let result = [];

        for (let i = 0; i < tokens.length; i++) {
            if (tokens[i] === 'x' || tokens[i] === '/') {
                let prevNum = parseFloat(result[result.length-1]);
                let nextNum = parseFloat(tokens[i+1]);
                let resultNum = operation[tokens[i]](prevNum, nextNum);
                result[result.length-1] = resultNum;
                i++;
            } else {
                result.push(tokens[i]);
            }
        }

        let total = parseFloat(result[0])
        for (let i = 1; i < result.length; i++) {
            if (result[i] === '+' || result[i] === '-') {
                let prevNum = total;
                let nextNum = parseFloat(result[i+1]);
                let resultNum = operation[result[i]](prevNum, nextNum);
                total = resultNum;
            }
        }
        displayCalculate.value = total;

        if (displayCalculate.value === 'NaN') {
            throw new Error;
        }

    } catch (error) {
        isTrue = false;
        displayCalculate.value = 'Syntax Error';
    }

    if (isTrue) {
        let li = document.createElement('li');
        li.innerText = `${expression} = ${displayCalculate.value}`;
        li.classList.add('second-list');
        calculateHistoryBox.appendChild(li);
    }

}

calculatorBox.addEventListener('click', (e) => {

    if(!e.target.matches('button'))
        return;

    if(e.target.innerText === '=') {
        calculate();
        return;
    }

    if (e.target.innerText === '⌫') {
        return;
    }

    if (e.target.innerText === 'C') {
        displayCalculate.value = '';
        return;
    }

    if (displayCalculate.value === 'Syntax Error') {
        displayCalculate.value = '';
    }


    appendDisplay(e.target.innerText);

});

// WINDOW UNLOAD AND LOAD

window.addEventListener('beforeunload', () => {
    saveCalculate();
});

window.addEventListener('DOMContentLoaded', () => {

    let history = JSON.parse(localStorage.getItem('history')) || [];


    history.forEach(function(x) {
        let li = document.createElement('li');
        li.innerText = x;
        li.classList.add('second-list');
        calculateHistoryBox.appendChild(li);
    });


});

