#!/usr/bin/env python3
"""
Dependency analysis script to understand package sizes and identify optimization opportunities.
"""

import subprocess
import sys
import json
from pathlib import Path

def analyze_installed_packages():
    """Analyze installed packages and their sizes."""
    try:
        # Get list of installed packages
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            print("📦 Installed Python packages:")
            print("=" * 50)
            
            for pkg in sorted(packages, key=lambda x: x['name']):
                print(f"{pkg['name']:<30} {pkg['version']}")
            
            print(f"\n📊 Total packages: {len(packages)}")
            
            # Identify potentially heavy packages
            heavy_packages = [
                'tensorflow', 'torch', 'numpy', 'scipy', 'pandas', 
                'matplotlib', 'seaborn', 'opencv-python', 'Pillow',
                'transformers', 'sklearn', 'scikit-learn', 'nltk',
                'spacy', 'prefect', 'controlflow'
            ]
            
            found_heavy = []
            for pkg in packages:
                if any(heavy in pkg['name'].lower() for heavy in heavy_packages):
                    found_heavy.append(pkg['name'])
            
            if found_heavy:
                print(f"\n⚠️  Potentially heavy packages found:")
                for pkg in found_heavy:
                    print(f"   - {pkg}")
                print("\n💡 Consider alternatives or exclude from Vercel deployment")
            
        else:
            print("❌ Failed to get package list")
            
    except Exception as e:
        print(f"❌ Error analyzing packages: {e}")

def check_import_dependencies():
    """Check what your main application actually imports."""
    print("\n🔍 Checking actual imports in your application...")
    
    main_files = [
        'backend/main.py',
        'backend/workflow.py',
        'backend/agents/__init__.py',
        'api/index.py'
    ]
    
    imports = set()
    
    for file_path in main_files:
        if Path(file_path).exists():
            print(f"\n📄 Analyzing {file_path}:")
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Find import statements
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        print(f"   {line}")
                        # Extract package name
                        if line.startswith('import '):
                            pkg = line.split('import ')[1].split('.')[0].split(' ')[0]
                        else:
                            pkg = line.split('from ')[1].split('.')[0].split(' ')[0]
                        imports.add(pkg)
                        
            except Exception as e:
                print(f"   ❌ Error reading {file_path}: {e}")
    
    print(f"\n📋 Unique top-level imports: {sorted(imports)}")

def suggest_optimizations():
    """Suggest optimization strategies."""
    print("\n🎯 Optimization Strategies for Vercel:")
    print("=" * 50)
    
    strategies = [
        "1. 🔬 Minimal Dependencies: Use requirements-vercel.txt with only essential packages",
        "2. 📦 Bundle Analysis: Check what's actually being imported vs installed",
        "3. 🚀 Edge Functions: Move lightweight operations to Vercel Edge Functions",
        "4. 🌐 External Services: Move heavy operations (AI processing) to external APIs",
        "5. 📁 File Exclusion: Use .vercelignore and vercel.json excludeFiles",
        "6. 🎭 Conditional Imports: Use dynamic imports for heavy dependencies",
        "7. 🔄 Alternative Libraries: Replace heavy packages with lighter alternatives"
    ]
    
    for strategy in strategies:
        print(strategy)
    
    print("\n💡 Recommended approach:")
    print("   - Start with minimal API (api/index-minimal.py)")
    print("   - Use requirements-vercel.txt")
    print("   - Test deployment")
    print("   - Gradually add features while monitoring bundle size")

if __name__ == "__main__":
    print("🔍 BotArmy Dependency Analysis")
    print("=" * 50)
    
    analyze_installed_packages()
    check_import_dependencies()
    suggest_optimizations()
    
    print("\n✅ Analysis complete!")
    print("💡 Run ./scripts/prepare_vercel_deploy.sh to optimize for Vercel")
