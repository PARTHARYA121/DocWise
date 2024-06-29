function sendMessage(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if (username.trim() === '' || password.trim() === '') return;
    
    // Logic to handle form submission
    console.log('Username:', username);
    console.log('Password:', password);

    // You can add API call logic here
}
