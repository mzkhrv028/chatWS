class Connection {
    constructor(onOpen, onMessage, onClose, onError) {
        if (path === "${CONNECT_PATH}") {
            path = `ws://${window.location.hostname}:${window.location.port}/connect`;
        }
        this.connection = new WebSocket(path);
        this.connection.onopen = onOpen;
        this.connection.onmessage = onMessage;
        this.connection.onclose = onClose;
        this.connection.onerror = onError;
    }

    push = (kind, data) => {
        this.connection.send(JSON.stringify({kind: kind, payload: data}));
    }
}