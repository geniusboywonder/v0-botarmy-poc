# Vercel Deployment Solutions for BotArmy

This document explains how to resolve the "Serverless Function has exceeded the unzipped maximum size of 250 MB" error when deploying to Vercel.

## 🚨 The Problem

Vercel has a hard limit of 250MB (unzipped) / 50MB (compressed) for serverless functions. Your Python dependencies (especially ControlFlow and Prefect) are likely exceeding this limit.

## 🛠️ Solutions Implemented

### Solution 1: Minimal API Deployment (Recommended)

**Files created:**
- `requirements-vercel.txt` - Minimal dependencies for Vercel
- `api/index-minimal.py` - Lightweight API with basic endpoints

**Use this when:**
- You need a working deployment quickly
- You can accept limited functionality on Vercel
- Heavy operations can be moved to external services

### Solution 2: Optimized Full API Deployment

**Files created:**
- `vercel.json` - Excludes unnecessary files from deployment
- Updated `next.config.mjs` - Better file tracing
- `.vercelignore` - Additional file exclusions

**Use this when:**
- You need full functionality on Vercel
- You're willing to optimize dependencies
- You want to keep the complete workflow system

## 🚀 Deployment Steps

### Step 1: Rebuild Virtual Environment

```bash
# Make scripts executable
chmod +x scripts/rebuild_venv.sh
chmod +x scripts/prepare_vercel_deploy.sh

# Rebuild your local venv with updated requirements
./scripts/rebuild_venv.sh
```

### Step 2: Analyze Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate

# Run dependency analysis
python scripts/analyze_dependencies.py
```

### Step 3: Choose Deployment Strategy

```bash
# Run the deployment preparation script
./scripts/prepare_vercel_deploy.sh
```

This script will ask you to choose:
1. **Minimal API** (safer, limited functionality)
2. **Full API** (optimized, full functionality)

### Step 4: Deploy to Vercel

```bash
# Test locally first
npm run dev

# Build the project
npm run build

# Deploy to Vercel
vercel --prod
```

## 📊 File Size Optimization Techniques

### 1. Dependency Exclusion
- **Excluded**: `venv/`, `__pycache__/`, test files, documentation
- **Excluded**: Development tools like Docker files and debug scripts

### 2. Minimal Requirements
The `requirements-vercel.txt` includes only:
- FastAPI core
- Uvicorn
- Pydantic
- Google Generative AI
- Essential utilities

### 3. Smart File Tracing
- Next.js configuration excludes Python-specific files
- Vercel configuration prevents uploading development artifacts

## 🔧 Alternative Approaches

### Option A: Microservices Architecture
Split heavy operations into separate services:

```
Frontend (Vercel) → Lightweight API (Vercel) → Heavy Processing (External)
```

### Option B: Edge Functions
Move simple operations to Vercel Edge Functions (even smaller limits but faster).

### Option C: Hybrid Deployment
- Frontend: Vercel
- API: Railway, Render, or DigitalOcean App Platform

## 🐛 Troubleshooting

### If deployment still fails:

1. **Check bundle size:**
   ```bash
   vercel --debug
   ```

2. **Reduce dependencies further:**
   - Remove unused imports
   - Use lighter alternatives
   - Implement lazy loading

3. **Move to external service:**
   - Deploy the Python backend separately
   - Use Vercel only for the frontend

### Common Culprits:
- ✅ **Prefect**: 50-100MB+ (moved to local-only)
- ✅ **ControlFlow**: 20-50MB+ (moved to local-only)
- ✅ **NumPy/SciPy**: 50MB+ (excluded)
- ✅ **TensorFlow/PyTorch**: 500MB+ (not used)

## 📈 Monitoring Bundle Size

Add this to your CI/CD pipeline:

```bash
# Check bundle size after build
du -sh .vercel/output/functions/
```

Set up alerts if size approaches limits.

## 🎯 Recommended Strategy

1. **Start with Minimal API** for immediate deployment
2. **Test core functionality** works on Vercel
3. **Gradually add features** while monitoring size
4. **Move heavy operations** to external services as needed

## 📞 Support

If you continue having issues:
- Check the dependency analysis output
- Consider the hybrid deployment approach
- Move AI processing to dedicated services (OpenAI API, etc.)

The goal is to have a lean, fast-loading serverless function that delegates heavy work to appropriate services.
