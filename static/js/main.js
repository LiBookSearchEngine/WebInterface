document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("focus", function () {
        this.placeholder = "";
    });
    searchInput.addEventListener("blur", function () {
        this.placeholder = "Search for books here:";
    });
});

function validateForm() {
    var nameField = document.getElementById("name");
    var emailField = document.getElementById("email");
    var messageField = document.getElementById("message");
    var acceptCheckbox = document.getElementById("accept");
    var errorMessage = document.getElementById("error-message");

    if (nameField.value === "" || emailField.value === "" || messageField.value === "") {
        errorMessage.style.display = "block";
        return false;
    }

    if (!acceptCheckbox.checked) {
        errorMessage.style.display = "block";
        return false;
    }

    errorMessage.style.display = "none";
    return true;
}

document.getElementById('register-form').addEventListener('submit', function(event) {
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    const error_message = document.getElementById('error-message');

    if (password !== confirm_password) {
        event.preventDefault();
        error_message.textContent = 'Passwords do not match. Please try again.';
    } else {
        error_message.textContent = '';
    }
});