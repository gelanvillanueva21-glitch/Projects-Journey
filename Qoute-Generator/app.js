
let button = document.querySelector('#btn-quote');
let qoute = document.querySelector('.qoute');
let person = document.querySelector('.person');

const listQoutes = [{
    qoutes: '"Be the change that you wish to see in the world."',
    persons: 'Mahatma Gandhi'
}, {
    qoutes: '"The future belongs to those who believe in the beauty of their dreams."',
    persons: 'Eleanor Roosevelt'
}, {
    qoutes: '"The only way to do great work is to love what you do."',
    persons: 'Steve Jobs'
}, {
    qoutes: '"If you tell the truth, you dont have to remember anything."',
    persons: 'Mark Twain'
}, {
    qoutes: '"It is during our darkest moments that we must focus to see the light."',
    persons: 'Aristotle'
}, {
    qoutes: '"Do not go where the path may lead, go instead where there is no path and leave a trail."',
    persons: 'Ralph Waldo Emerson'
}];

button.addEventListener('click', function(){

    let random = Math.floor(Math.random() * listQoutes.length);

    qoute.innerText = listQoutes[random].qoutes;
    person.innerText = listQoutes[random].persons;

});