console.log("websocket connection");

const friend_id = JSON.parse(document.getElementById('json-friend_id').textContent);
const friend_username = JSON.parse(document.getElementById('json-friend_username').textContent);


const socket = new WebSocket('ws://' + window.location.host + '/ws/' + friend_username + '/'+ friend_id + '/');

socket.onopen = function(e) {
	console.log('Connection established');
};

socket.onmessage = function(e) {
	console.log(e);
	const data = JSON.parse(e.data);
	const message = data['message'];
	console.log(message);
}

socket.onclose = function(e) {
	console.log('Connection closed');
}

socket.onerror = function(e) {
	console.log('Error occured');
}



function sendMsg(){
	socket.send(JSON.stringify({
		'message': 'Hello from client'
	}));
}