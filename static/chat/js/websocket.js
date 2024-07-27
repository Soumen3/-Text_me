console.log("websocket connection");

const friend_id = JSON.parse(document.getElementById('json-friend_id').textContent);
const friend_username = JSON.parse(document.getElementById('json-reciever_username').textContent);
const sender_username = JSON.parse(document.getElementById('json-sender_username').textContent);


const socket = new WebSocket('ws://' + window.location.host + '/ws/' + friend_username + '/'+ friend_id + '/');

socket.onopen = function(e) {
	console.log('Connection established');
};

socket.onmessage = function(e) {
	console.log(e);
	const data = JSON.parse(e.data);
	const message = data['message'];
	console.log(message);

	if (data.sender_username == sender_username) {
        document.querySelector('#chat-body').innerHTML += `
        <tr class="table-secondary">
            <td style="display:grid">
                <p class="sender-message-element bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                    ${data.message} <br>
                    <small class="p-1  time-stamp">${data.timestamp}</small>
                </p>
            </td>
                               
        </tr>`
    }
    else {
        document.querySelector('#chat-body').innerHTML += `
        <tr class="table-secondary">
            <td style="display:grid">
                <p class="receiver-message-element bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
                    ${data.message} <br>
                    <small class="p-1  time-stamp">${data.timestamp}</small>
                </p>
            </td>                                
        </tr>`
    }
}

socket.onclose = function(e) {
	console.log('Connection closed');
}

socket.onerror = function(e) {
	console.log('Error occured');
}



function send_messagge(){
	console.log("send_messagge");
	const messageInputDom = document.querySelector("#message_input");
	const message = messageInputDom.value;

	var currentTime = new Date();
	var options = { hour12: true };
	var timeString = currentTime.toLocaleTimeString([], options);
	
	if (message === "") {
		return;
	}

	socket.send(JSON.stringify({
		'message': message,
		'sender_username': sender_username,
		'friend_id': friend_id,		
		'timestamp': timeString
	}));
	
	messageInputDom.value = '';

	// var chatWindow = document.getElementById("chat-window");
	chatWindow.scrollTop = chatWindow.scrollHeight;
	
}





document.querySelector("#chat-message-submit").onclick = send_messagge;


document.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
      // Call your function here
      send_messagge();
    }
  });

  

var chatWindow = document.getElementById("chat-window");
chatWindow.scrollTop = chatWindow.scrollHeight;
