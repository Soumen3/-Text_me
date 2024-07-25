console.log("websocket connection");



const socket = new WebSocket('ws://' + window.location.host + '/ws/connect/');

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