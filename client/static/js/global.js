// globals
let connection;
let path;
let run = true;

// chat
let chatSendButton = document.getElementById("send-button");
let chatContainer = document.getElementById("chat-container");
let connectButton = document.getElementById("connect-button");

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