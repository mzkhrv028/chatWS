// globals
let connection;
let path;
let run = true;

// chat
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const msgerSentBtn = get(".msger-send-btn")

// user
let id = "initial";
let username = "undefined";

// server
const INITIAL = "initial";
const ADD = "add";
const SEND = "send";
const REMOVE = "remove";

// client
const CONNECT_EVENT = "connect";
const DISCONNECT_EVENT = "disconnect";
const PING_EVENT = "ping";