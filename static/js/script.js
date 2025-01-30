// script.js

// Optional: You can implement AJAX calls for chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages');

    // Function to refresh chat messages periodically
    function refreshMessages() {
        fetch('/chat')
            .then(response => response.text())
            .then(data => {
                messagesContainer.innerHTML = data;
            })
            .catch(error => console.error('Error fetching messages:', error));
    }

    // Set an interval to refresh messages every 5 seconds
    setInterval(refreshMessages, 5000);
});
