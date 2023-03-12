// login form submission handler
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault(); // prevent form from submitting
    var formData = new FormData(this); // get form data
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error logging in');
        }
    })
    .then(data => {
        if (data.success) {
            window.location.href = '/dashboard'; // redirect to dashboard page
        } else {
            displayMessage('Invalid username or password');
        }
    })
    .catch(error => {
        displayMessage('Error logging in');
        console.error(error);
    });
});

// registration form submission handler
document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault(); // prevent form from submitting
    var formData = new FormData(this); // get form data
    fetch('/register', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error registering');
        }
    })
    .then(data => {
        if (data.success) {
            window.location.href = '/dashboard'; // redirect to dashboard page
        } else {
            displayMessage('Username already taken');
        }
    })
    .catch(error => {
        displayMessage('Error registering');
        console.error(error);
    });
});

// lost account form submission handler
document.getElementById('lost-account-form').addEventListener('submit', function(e) {
    e.preventDefault(); // prevent form from submitting
    var formData = new FormData(this); // get form data
    fetch('/lost_account', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error retrieving account');
        }
    })
    .then(data => {
        if (data.success) {
            displayMessage('Account information sent to your email');
        } else {
            displayMessage('Invalid username');
        }
    })
    .catch(error => {
        displayMessage('Error retrieving account');
        console.error(error);
    });
});

// function to display messages to user
function displayMessage(message) {
    var messageElem = document.getElementById('message');
    messageElem.textContent = message;
    messageElem.classList.remove('hidden');
}
