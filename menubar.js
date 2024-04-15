// Get the current page name
var currentPage = window.location.pathname.split("/").pop();

// Get the menubar and login button elements
var menubar = document.getElementById('menubar');
var loginButton = document.getElementById('login-btn');

// If the current page is the login page, hide the login button
if (currentPage === 'login.html') {
    loginButton.style.display = 'none';
}

// If the current page is the admin page, show a welcome message and a logout link
if (currentPage === 'admin.html') {
    var welcomeMessage = document.createElement('span');
    welcomeMessage.textContent = 'Welcome, ' + username + '!'; // replace 'username' with the actual username
    menubar.appendChild(welcomeMessage);

    var logoutLink = document.createElement('a');
    logoutLink.href = 'logout.html';
    logoutLink.textContent = 'Logout';
    menubar.appendChild(logoutLink);
}