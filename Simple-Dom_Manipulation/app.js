let openButton = document.getElementById('btn');
let modelContainer = document.getElementById('model-container');
let closeButton = document.getElementById('close-btn');


openButton.addEventListener('click', function(){

    modelContainer.style.display = 'block'

});

closeButton.addEventListener('click', function(){

    modelContainer.style.display = 'none';

});

window.addEventListener('click', function(e){

    if (e.target === modelContainer)
        modelContainer.style.display = 'none';
});

