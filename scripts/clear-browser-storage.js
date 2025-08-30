// Clear localStorage to fix corrupted conversation data
// Run this in browser console or add to a utility script

console.log("Clearing conversation store data...")

// Clear the conversation store data
localStorage.removeItem('conversation-store')
localStorage.removeItem('agent-store')
localStorage.removeItem('task-store')
localStorage.removeItem('artifact-store')
localStorage.removeItem('log-store')

// Clear any other potential app storage
Object.keys(localStorage).forEach(key => {
  if (key.includes('conversation') || key.includes('botarmy')) {
    localStorage.removeItem(key)
  }
})

console.log("Storage cleared! Please refresh the page.")
