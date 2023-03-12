function displayWarning(message) {
    const warningDiv = document.createElement('div');
    warningDiv.classList.add('warning');
    warningDiv.textContent = message;
    const form = document.querySelector('form');
    form.insertAdjacentElement('beforebegin', warningDiv);
  }
  function validateForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    if (email === '') {
      displayWarning('Please enter your email.');
      return false;
    }
  
    if (password === '') {
      displayWarning('Please enter your password.');
      return false;
    }
  
    return true;
  }
  