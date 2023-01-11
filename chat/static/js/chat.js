const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function (e){
    console.log("CONNECTED.");
}

socket.onclose = function (e){
    console.log("LOST.");
}

socket.onerror = function (e){
    console.log(e);
}

socket.onmessage = function (e){
    const data = JSON.parse(e.data)
    let html = `<div id="message_box">
                   <p class="text-slate-800 font-semibold text-sm mt-1"> ${data.message}</p>
                 </div>`;

    document.getElementById('chat-messages').innerHTML += html;
}


document.querySelector('#chat-message-submit').onclick = function (e){
    const message_input = document.querySelector('#chat-message-input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message': message,
        'username': message_username,
    }));
    message_input.value = '';

}