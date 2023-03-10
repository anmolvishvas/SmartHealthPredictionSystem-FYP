let showpw = document.querySelector('.eyes');
let hidepw = document.querySelector('.showHidePw');
const passwordInput = document.getElementById('password');

showpw.addEventListener('click', () => {
    if (passwordInput.type == 'password') {
        passwordInput.type = 'text';
        hidepw.style.display = 'block';
        showpw.style.display = 'none';
    } else {
        passwordInput.type = 'password';
        hidepw.style.display = 'none';
        showpw.style.display = 'block';
    }
})

hidepw.addEventListener('click', () => {
    if (passwordInput.type == 'text') {
        passwordInput.type = 'password';
        hidepw.style.display = 'none';
        showpw.style.display = 'block';
        
    } else {
        passwordInput.type = 'text';
        hidepw.style.display = 'block';
        showpw.style.display = 'none';
        
    }
})
