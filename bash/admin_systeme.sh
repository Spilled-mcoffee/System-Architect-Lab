#!/bin/bash

# ------------------ CHECK ROOT ------------------
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)"
    exit 1
fi

echo "=== SYSTEM ADMINISTRATION SCRIPT ==="

# ------------------ USER INPUT ------------------
read -p "Enter username: " username

# Check if user exists
if id "$username" &>/dev/null; then
    echo "User already exists!"
    exit 1
fi

# ------------------ CREATE USER ------------------
useradd -m "$username"

if [ $? -eq 0 ]; then
    echo "User created successfully."
else
    echo "Error creating user."
    exit 1
fi

# ------------------ SET PASSWORD ------------------
echo "Set password for $username:"
passwd "$username"

# ------------------ CREATE DIRECTORY ------------------
user_dir="/home/$username/workspace"
mkdir -p "$user_dir"

# ------------------ PERMISSIONS ------------------
chown "$username":"$username" "$user_dir"
chmod 700 "$user_dir"

echo "Directory $user_dir created with secure permissions."

# ------------------ QUOTA (SIMULATED) ------------------
echo "Simulating disk quota assignment..."
echo "User $username assigned 100MB quota (simulation)"

# ------------------ SUMMARY ------------------
echo "=== SUMMARY ==="
echo "User: $username"
echo "Home: /home/$username"
echo "Workspace: $user_dir"
echo "Permissions: 700 (owner only)"

echo "Script execution completed successfully."