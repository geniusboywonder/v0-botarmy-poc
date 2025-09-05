// Test script for HITL bug fix
// Run this in the browser console to test the HITL display bug fix

// Function to create a test HITL request
function createTestHITL() {
  const { addRequest } = useHITLStore.getState();
  
  addRequest({
    agentName: 'Analyst',
    decision: 'Test HITL Request - Please approve this test action',
    context: {
      test: true,
      timestamp: new Date().toISOString()
    },
    priority: 'medium'
  });
  
  console.log('✅ Test HITL request created for Analyst agent');
}

// Function to simulate clicking HITL alert
function simulateHITLAlertClick() {
  const { requests, navigateToRequest } = useHITLStore.getState();
  const pendingRequests = requests.filter(r => r.status === 'pending');
  
  if (pendingRequests.length > 0) {
    console.log('🔄 Simulating HITL alert click...');
    navigateToRequest(pendingRequests[0].id);
    console.log('✅ Navigated to HITL request:', pendingRequests[0].id);
    
    // Check if HITL is displayed
    setTimeout(() => {
      const hitlElement = document.querySelector('.bg-amber-50');
      if (hitlElement) {
        console.log('✅ SUCCESS: HITL prompt is visible on first click!');
      } else {
        console.log('❌ FAILED: HITL prompt not visible on first click');
      }
    }, 100);
  } else {
    console.log('❌ No pending HITL requests found. Create one first.');
  }
}

// Function to clear all HITL requests
function clearAllHITL() {
  const { requests, resolveRequest } = useHITLStore.getState();
  requests.forEach(req => {
    if (req.status === 'pending') {
      resolveRequest(req.id, 'rejected', 'Cleared for testing');
    }
  });
  console.log('✅ All HITL requests cleared');
}

// Test sequence
console.log('=== HITL Bug Fix Test Suite ===');
console.log('Available commands:');
console.log('1. createTestHITL() - Create a test HITL request');
console.log('2. simulateHITLAlertClick() - Simulate clicking HITL alert');
console.log('3. clearAllHITL() - Clear all pending HITL requests');
console.log('');
console.log('Test procedure:');
console.log('1. Run createTestHITL() to create a test request');
console.log('2. Check that HITL alert appears in the header');
console.log('3. Click the HITL alert manually or run simulateHITLAlertClick()');
console.log('4. Verify HITL prompt appears immediately in chat (amber background)');
console.log('5. Run clearAllHITL() to clean up');
