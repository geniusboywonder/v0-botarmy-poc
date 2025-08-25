#!/usr/bin/env python3

import subprocess
import os
import sys

def run_command(cmd, cwd=None):
    """Run a command and return the output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def main():
    project_path = "/Users/neill/Documents/AI Code/Projects/v0-botarmy-poc"

    print("=== BotArmy Git Status Check ===")
    print(f"Working directory: {project_path}")
    print()

    # Check current branch
    print("Current branch:")
    current_branch = run_command("git branch --show-current", cwd=project_path)
    print(f"  {current_branch}")
    print()

    # Check all branches
    print("All local branches:")
    branches = run_command("git branch", cwd=project_path)
    for line in branches.split('\n'):
        print(f"  {line}")
    print()

    # Check remote branches
    print("Remote branches:")
    remote_branches = run_command("git branch -r", cwd=project_path)
    for line in remote_branches.split('\n'):
        if 'enhanced-hitl' in line.lower():
            print(f"  >>> {line}")  # Highlight HITL branches
        else:
            print(f"  {line}")
    print()

    # Try to fetch latest
    print("Fetching from origin...")
    fetch_result = run_command("git fetch origin", cwd=project_path)
    print(f"  {fetch_result if fetch_result else 'Fetch completed'}")
    print()

    # Check if the remote branch exists
    print("Checking for enhanced-hitl-integration-final branch:")
    remote_check = run_command("git ls-remote --heads origin enhanced-hitl-integration-final", cwd=project_path)
    if remote_check and not remote_check.startswith("Error"):
        print(f"  ✅ Found: {remote_check}")
    else:
        print(f"  ❌ Not found or error: {remote_check}")
    print()

    # Current git status
    print("Git status:")
    status = run_command("git status --porcelain", cwd=project_path)
    if status:
        print("  Modified files:")
        for line in status.split('\n'):
            print(f"    {line}")
    else:
        print("  Clean working directory")

if __name__ == "__main__":
    main()
