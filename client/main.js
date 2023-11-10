//@ts-check

window.addEventListener("DOMContentLoaded", () => {
  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:8001/");
  receiveMessageHandler(websocket);

  const form = document.getElementById("temp-form");

  form?.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!websocket || !form) return;

    const formData = new FormData(form);

    const setpoint = formData.get("setpoint-temp");

    if (!setpoint) return;

    websocket.send(setpoint?.toString());
  });
});

function parseMessage(message) {
  const data = message.replace("\n\u0000", "");

  // Split the string into an array of key-value pairs
  let pairs = data.split("; ");

  // Convert each pair into a [key, value] array
  let keyValuePairs = pairs.map((pair) => {
    let [key, value] = pair.split("=");
    return [key, parseFloat(value)]; // Convert the value to a number
  });

  return [keyValuePairs[0], keyValuePairs[1]];
}

function receiveMessageHandler(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const message = parseMessage(JSON.parse(data));

    const setpoint = message[0][1];

    const currentTemp = message[1][1];

    const setpointElement = document.getElementById("setpoint-value");
    setpointElement.innerHTML = setpoint;

    const currentTempElement = document.getElementById("current-temp-value");
    currentTempElement.innerHTML = currentTemp;

    // append message to the DOM
    const newMessage = document.createElement("div");
    newMessage.innerHTML = JSON.parse(data);

    const consoleSection = document.getElementById("console");
    consoleSection.appendChild(newMessage);
  });
}
