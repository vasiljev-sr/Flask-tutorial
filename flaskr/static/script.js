'use strict';

const header = document.querySelector('.settings__header');
const body = document.querySelector('.settings__body')
console.log(header);
header.addEventListener('click', (e) => {
    if (body.classList.contains('hide')) {
        body.classList.remove('hide')
        body.classList.add('show')
    
    }
    else {
        body.classList.remove('show')
        body.classList.add('hide')
    }
  });