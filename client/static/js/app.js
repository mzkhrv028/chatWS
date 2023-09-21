connectButton.addEventListener("click", function() {

    username = document.getElementById("username-field").value;

    if (!username) return;

    connection = new Connection(onOpen, onMessage, onClose, onError);

    enterListener("send-button", "chat-container");
    addEventListener("beforeunload", beforeUnloadClose);

    chatSendButton.addEventListener("click", messageListener);

});


enterListener = (element, container) => {
    window.document.getElementById(container).addEventListener("keyup", function(event) {
        if (event.code === "Enter") {
            event.preventDefault();
            document.getElementById(element).click();
        }
    });
}


messageListener = () => {
    const messageFieldElem = document.getElementById("message-field");
    if (!messageFieldElem.value) return;
    connection.push(SEND, {
        id: id,
        name: username,
        message: messageFieldElem.value,
    });
}


ping = () => {
    if (!run) return;
    connection.push(PING_EVENT, {
        id: id,
    });
}


onFullyConnected = (payload) => {
    id = payload["id"];
    connection.push(CONNECT_EVENT, {
        id: id,
        name: username,
    });

    setInterval(ping, 15000);
}


onSendMessage = (payload) => {
    const element = document.createElement("div");
    const textMessage = document.createTextNode(`[${payload["time"]}] ${payload["name"]}: ${payload["message"]}`);
    element.appendChild(textMessage);
    chatContainer.appendChild(element);
}


onAddUser = (payload) => {
    const element = document.createElement("div");
    const textMessage = document.createTextNode(`User ${payload["name"]} joined the server.`);
    element.appendChild(textMessage);
    chatContainer.appendChild(element);
}


onRemoveUser = (payload) => {
    const element = document.createElement("div");
    const textMessage = document.createTextNode(`User ${payload["name"]} leave the server.`);
    element.appendChild(textMessage);
    chatContainer.appendChild(element);
}


onMessage = (event) => {
    let msg = JSON.parse(event.data);
    const kind = msg["kind"];
    const payload = msg["payload"];

    console.log(`new event with kind ${kind} and payload ${JSON.stringify(payload)}`);

    switch(kind) {
        case INITIAL:
            onFullyConnected(payload);
            break;
        case ADD:
            onAddUser(payload);
            break;
        case SEND:
            onSendMessage(payload);
            break;
        case REMOVE:
            onRemoveUser(payload);
            break;
        default:
            console.log(`unsupported event kind ${kind}, data ${payload}`);
    }
}


onOpen = () => {
    console.log("Websocket connection opened");
}


beforeUnloadClose = (event) => {
    event.preventDefault();
    connection.push(DISCONNECT_EVENT, {
        id: id,
    });
    run = false;
}


onClose = () => {
    console.log("Websocket connection closed");
}


onError = (e) => {
    console.log(`connection close with error ${e}`);
    run = false;
}