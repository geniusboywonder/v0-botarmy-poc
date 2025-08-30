# BotArmy Kill Utilities

This directory contains utilities to safely terminate the BotArmy application.

## 🔴 Kill Scripts

### Option 1: npm script (Recommended)
```bash
npm run kill
```
Uses the Node.js version with detailed logging.

### Option 2: Shell script 
```bash
./kill-app.sh
```
Comprehensive bash script with detailed process tracking.

### Option 3: Emergency kill
```bash
./emergency-kill.sh
```
Fast and forceful termination of all processes.

### Option 4: Node.js script
```bash
node kill-app.js
```
Cross-platform Node.js version with detailed output.

## 🔄 Restart Utility

To kill and restart in one command:
```bash
npm run restart
```

## 🎯 What Gets Killed

All scripts will terminate:
- **Frontend processes**: npm dev, Next.js dev server (ports 3000, 3001)
- **Backend processes**: Python main.py, uvicorn server (port 8000)  
- **Parent processes**: npm replit:dev, concurrently
- **Related processes**: Any Node.js or Python processes in the project directory

## 🚨 When to Use

Use these utilities when:
- The app won't respond to Ctrl+C
- Processes are stuck or hanging
- Ports are still in use after stopping
- You need to completely reset the application state
- Before switching between different branches or major changes

## ✅ Verification

After running any kill script, you should see:
- ✅ All target processes terminated
- ✅ Ports 3000, 3001, 8000 are free
- ✅ No remaining BotArmy processes found

## 🔧 Troubleshooting

If processes still remain after running a kill script:
1. Try the emergency kill: `./emergency-kill.sh`
2. Manually check: `lsof -ti:3000 :3001 :8000 | xargs kill -9`
3. Reboot your system if all else fails

## 🏃‍♂️ Quick Reference

```bash
# Start the app
npm run replit:dev

# Kill the app  
npm run kill

# Kill and restart
npm run restart

# Emergency kill (if stuck)
./emergency-kill.sh
```
