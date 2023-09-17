document.addEventListener("DOMContentLoaded", function() {

    connection = new Connection(onOpen, onMessage, onClose, onError);

}, false);


onMessage = (msg) => {
    let event = JSON.parse(msg.data);
    const kind = event["kind"];
    const payload = event["payload"];

    console.log(`new event with kind ${kind} and payload ${JSON.stringify(payload)}`);

    switch(kind) {
        case INITIAL:
            onFullyConnected(payload);
            break;
        case ADD:
            break;
        case SEND:
            break;
        case REMOVE:
            break;
        default:
            console.log(`unsupported event kind ${kind}, data ${payload}`);
    }
}


onFullyConnected = (payload) => {
    id = payload["id"];
    connection.push(CONNECT_EVENT, {
        id: id,
    });

    setInterval(ping, 1000);
}


ping = () => {
    if (!run) return;
    console.log("ping");
    connection.push(PING_EVENT, {
        id: id,
    });
}


onOpen = () => {
    console.log("Websocket connection opened");
}


onClose = () => {
    console.log("Websocket connection closed");
    connection.push(
        DISCONNECT_EVENT,
        {
            id: id,
        }
    );
    run = false;
}


onError = (e) => {
    console.log(`connection close with error ${e}`);
    run = false;
}