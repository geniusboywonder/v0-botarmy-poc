# BotArmy Quick Start Guide

## 🔥 The Real Solution to Your ControlFlow Issues

Your ControlFlow installation was failing because **ControlFlow 0.8.0 is broken** with modern Python/Prefect versions. Here's the actual fix:

## ✅ Working Solution

### 1. Use the New Setup Script (Easiest)
```bash
# Remove old broken setup
rm -rf venv

# Use the fixed setup script
chmod +x setup-v2.sh
./setup-v2.sh
```

### 2. What This Does
- ✅ **Uses ControlFlow 0.11+** (latest stable version)
- ✅ **Works with Prefect 3.0+** (no more dependency conflicts)
- ✅ **Detects Python 3.11** automatically or guides installation
- ✅ **Fallback to minimal mode** if ControlFlow still fails

## 🚀 Quick Test After Setup

```bash
# Start backend
source venv/bin/activate
cd backend && python main.py

# In new terminal, start frontend
pnpm dev

# Open http://localhost:3000
```

## 🔧 What Was Wrong

| Issue | ❌ Before | ✅ Fixed |
|-------|-----------|----------|
| **ControlFlow Version** | 0.8.0 (broken) | 0.11+ (working) |
| **Prefect Compatibility** | Conflicting deps | Full 3.0+ support |
| **Python Version** | Any 3.11+ | Exactly 3.11 required |
| **Error Handling** | Setup crashes | Graceful fallback |

## 🆘 If It Still Doesn't Work

The `setup-v2.sh` script will offer a **minimal mode** that installs everything except ControlFlow. You'll have:
- ✅ Working FastAPI backend
- ✅ Full frontend functionality  
- ✅ OpenAI integration
- ❌ No agent orchestration (ControlFlow features)

This is better than nothing and lets you test the rest of the system.

## 📋 Commands Summary

```bash
# Full setup (recommended)
./setup-v2.sh

# Manual Python 3.11 install (macOS)
./install-python311-macos.sh

# Verify everything works
./verify-setup.sh

# Start the app
source venv/bin/activate && cd backend && python main.py
pnpm dev  # in new terminal
```

The key insight: **ControlFlow 0.8.0 was the problem all along**. The newer versions work properly with modern Python and Prefect.
