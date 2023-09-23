addEventListener("DOMContentLoaded", function () {
    connection = new Connection(onOpen, onMessage, onClose, onError);

    addEventListener("beforeunload", beforeUnloadClose);
    enterListener(msgerSentBtn, msgerInput)

}, false);


enterListener = (button, input) => {
    input.addEventListener("keyup", function (event) {
        if (event.code === "Enter") {
            event.preventDefault();
            button.click();
        }
    });
}


msgerForm.addEventListener("submit", event => {
    event.preventDefault();

    const msgText = msgerInput.value;
    if (!msgText) return;

    appendMessage(username, "", "right", msgText);

    connection.push(SEND, {
        id: id,
        name: username,
        message: msgText,
    });

    msgerInput.value = "";
});


appendMessage = (name, img, side, text) => {
    const msgHTML = `
      <div class="msg ${side}-msg">
        <div class="msg-img" style="background-image: url(${img})"></div>
  
        <div class="msg-bubble">
          <div class="msg-info">
            <div class="msg-info-name">${name}</div>
            <div class="msg-info-time">${formatDate(new Date())}</div>
          </div>
  
          <div class="msg-text">${text}</div>
        </div>
      </div>
    `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}


sendMessage = (payload) => {
    appendMessage(payload["name"], "", "left", payload["message"])
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


addUser = (payload) => {
    const element = document.createElement("div");
    const textMessage = document.createTextNode(`User ${payload["name"]} joined the server.`);
    element.appendChild(textMessage);
    chatContainer.appendChild(element);
}


removeUser = (payload) => {
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

    switch (kind) {
        case INITIAL:
            onFullyConnected(payload);
            break;
        case ADD:
            addUser(payload);
            break;
        case SEND:
            sendMessage(payload);
            break;
        case REMOVE:
            removeUser(payload);
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