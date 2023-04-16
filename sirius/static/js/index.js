document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("btn").addEventListener("click", function(event) {
        event.preventDefault();
        sendEmail();
    });

    function sendEmail() {
        var name = document.getElementById("name").value;
        var phone = document.getElementById("phone").value;
        var email = document.getElementById("email").value;
        var subject = document.getElementById("subject").value;
        var message = document.getElementById("message").value;

        var body = "Name: " + name + "\nPhone: " + phone + "\nEmail: " + email + "\n\nMessage:\n" + message;

        window.location.href = "mailto:bouzidiwaad19@gmail.com?subject=" + subject + "&body=" + body;
        alert("Your message has been sent!");
    }
});