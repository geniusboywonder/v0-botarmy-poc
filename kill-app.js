#!/usr/bin/env node

// BotArmy Application Killer - Node.js version
// Cross-platform utility to kill all BotArmy processes

const { exec, spawn } = require('child_process');
const path = require('path');

const PROJECT_PATH = '/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc';
const PORTS = [3000, 3001, 8000];

console.log('🔴 Killing BotArmy Application...');
console.log('==================================');

// Function to execute command and return promise
function execAsync(command, description) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error && error.code !== 1) { // Ignore "no process found" errors
                console.log(`⚠️  ${description}: ${error.message}`);
            }
            if (stdout.trim()) {
                console.log(`🔍 ${description}: ${stdout.trim()}`);
            }
            resolve({ stdout, stderr, error });
        });
    });
}

async function killApp() {
    try {
        // Kill processes by pattern
        const processPatterns = [
            { pattern: 'npm.*replit:dev', desc: 'npm replit:dev' },
            { pattern: 'npm.*run.*dev', desc: 'npm run dev' },
            { pattern: 'next.*dev', desc: 'Next.js dev server' },
            { pattern: 'python3.*main.py', desc: 'Python backend' },
            { pattern: 'uvicorn.*main:app', desc: 'Uvicorn server' },
            { pattern: 'concurrently.*npm', desc: 'Concurrently process' }
        ];

        for (const { pattern, desc } of processPatterns) {
            console.log(`\n🎯 Targeting ${desc}...`);
            await execAsync(`pkill -f "${pattern}"`, `Kill ${desc}`);
            // Force kill if needed
            await new Promise(resolve => setTimeout(resolve, 1000));
            await execAsync(`pkill -9 -f "${pattern}"`, `Force kill ${desc}`);
        }

        // Kill by ports
        console.log('\n🚪 Clearing ports...');
        for (const port of PORTS) {
            const portDesc = port === 3000 || port === 3001 ? 'Frontend' : 'Backend';
            console.log(`\n🎯 Clearing port ${port} (${portDesc})...`);
            
            // Use lsof to find and kill processes on specific ports
            await execAsync(`lsof -ti:${port} | xargs -r kill -TERM`, `Kill processes on port ${port}`);
            await new Promise(resolve => setTimeout(resolve, 2000));
            await execAsync(`lsof -ti:${port} | xargs -r kill -KILL`, `Force kill processes on port ${port}`);
        }

        // Additional cleanup
        console.log('\n🧹 Additional cleanup...');
        await execAsync(`pgrep -f "node.*${PROJECT_PATH}" | xargs -r kill -TERM`, 'Kill project Node.js processes');
        await execAsync(`pgrep -f "python.*${PROJECT_PATH}" | xargs -r kill -TERM`, 'Kill project Python processes');
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        await execAsync(`pgrep -f "node.*${PROJECT_PATH}" | xargs -r kill -KILL`, 'Force kill project Node.js processes');
        await execAsync(`pgrep -f "python.*${PROJECT_PATH}" | xargs -r kill -KILL`, 'Force kill project Python processes');

        // Final status check
        console.log('\n🔍 Final Status Check...');
        console.log('========================');
        
        for (const port of PORTS) {
            const portDesc = port === 3000 || port === 3001 ? 'Frontend' : 'Backend';
            const result = await execAsync(`lsof -ti:${port}`, `Check port ${port}`);
            if (result.stdout.trim()) {
                console.log(`⚠️  Port ${port} (${portDesc}) is still in use!`);
            } else {
                console.log(`✅ Port ${port} (${portDesc}) is free`);
            }
        }

        console.log('\n🎉 BotArmy Application Termination Complete!');
        console.log('=============================================');
        console.log('You can now safely restart the application with:');
        console.log('npm run replit:dev');
        console.log('');

    } catch (error) {
        console.error('❌ Error during cleanup:', error);
        process.exit(1);
    }
}

// Run the killer
killApp().catch(console.error);
