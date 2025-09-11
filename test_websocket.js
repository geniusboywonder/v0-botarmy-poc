#!/usr/bin/env node

const WebSocket = require('ws');

console.log('🧪 Testing direct WebSocket connection to /api/copilotkit-ws');

const ws = new WebSocket('ws://localhost:8000/api/copilotkit-ws');

ws.on('open', function open() {
  console.log('✅ WebSocket connected successfully');
  
  // Send a test message that should trigger our colored emoji breakpoints
  const testMessage = {
    type: "chat_message", 
    content: "test message from direct WebSocket", 
    session_id: "copilotkit_session"
  };
  
  console.log('📤 Sending test message:', testMessage);
  ws.send(JSON.stringify(testMessage));
  
  // Keep connection open for a few seconds to see response
  setTimeout(() => {
    console.log('🔌 Closing connection');
    ws.close();
  }, 3000);
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