
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const notificationContainer = document.getElementById('notification-container');

    const notification = document.createElement('div');
    notification.innerHTML = `<p>${data.message}</p>`;
    notificationContainer.appendChild(notification);
};

