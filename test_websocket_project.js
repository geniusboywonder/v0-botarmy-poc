#!/usr/bin/env node

const WebSocket = require('ws');

console.log('🧪 Testing WebSocket with PROJECT trigger message');

const ws = new WebSocket('ws://localhost:8000/api/copilotkit-ws');

ws.on('open', function open() {
  console.log('✅ WebSocket connected successfully');
  
  // Send a message that should trigger the project workflow
  const projectMessage = {
    type: "chat_message", 
    content: "start project to build a 'Hello World' html page", 
    session_id: "copilotkit_session"
  };
  
  console.log('📤 Sending PROJECT TRIGGER message:', projectMessage);
  ws.send(JSON.stringify(projectMessage));
  
  // Keep connection open longer to see agent responses
  setTimeout(() => {
    console.log('🔌 Closing connection');
    ws.close();
  }, 10000);
});

ws.on('message', function message(data) {
  console.log('📥 Received from backend:', data.toString());
});

ws.on('error', function error(err) {
  console.error('❌ WebSocket error:', err);
});

ws.on('close', function close() {
  console.log('🔌 WebSocket connection closed');
});