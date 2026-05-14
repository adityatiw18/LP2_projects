print("Hello from Cloud Instance!")
print("This file was transferred securely via SCP.")

# ============================================================
# CC ASSIGNMENT 8
# Secure File Sharing Between Cloud Instances
# ============================================================

# ============================================================
# OBJECTIVE
# ============================================================

# Create a secure cloud environment where two Azure Virtual
# Machines communicate privately inside the same Virtual
# Network (VNet) and exchange files securely using SSH & SCP.

# ============================================================
# ARCHITECTURE
# ============================================================

#                    Internet
#                        |
#                Azure Resource Group
#                        |
#                Azure Virtual Network
#                        |
#        ---------------------------------
#        |                               |
#   VM1 (Sender)  <----Private---->  VM2 (Receiver)

# ============================================================
# TECHNOLOGIES USED
# ============================================================

# Microsoft Azure  -> Cloud Infrastructure
# Ubuntu 22.04     -> Operating System
# SSH              -> Secure Remote Login
# SCP              -> Secure File Transfer
# RSA-4096         -> Encryption & Authentication
# VNet             -> Private Internal Communication

# ============================================================
# STEP 1 — CREATE RESOURCE GROUP
# ============================================================

# Azure Portal -> Resource Groups -> Create

# Resource Group Name : cc-assignment
# Region              : nearest region

# Purpose:
# Resource Group logically groups all Azure resources together.

# ============================================================
# STEP 2 — CREATE VIRTUAL NETWORK (VNet)
# ============================================================

# Azure Portal -> Virtual Networks -> Create

# Name          : secure-vnet
# Address Space : 10.0.0.0/16

# Subnet:
# Name  : subnet1
# Range : 10.0.1.0/24

# Networking Explanation:
# 10.0.0.0/16  -> Entire Virtual Network
# 10.0.1.0/24  -> Subnet inside VNet

# Purpose:
# VNet allows secure internal communication between VMs.

# ============================================================
# STEP 3 — CREATE VM1
# ============================================================

# Azure Portal -> Virtual Machines -> Create

# VM Name        : vm1
# OS             : Ubuntu 22.04
# Size           : Standard_B1s
# Username       : azureuser
# Authentication : SSH Public Key

# IMPORTANT:
# Select:
# "Generate new key pair"

# Download:
# vm1_key.pem

# Networking:
# Virtual Network : secure-vnet
# Subnet          : subnet1
# Allow SSH       : Yes (Port 22)

# ============================================================
# STEP 4 — CREATE VM2
# ============================================================

# VM Name        : vm2
# OS             : Ubuntu 22.04
# Username       : azureuser

# IMPORTANT:
# VM2 MUST use SAME VNet and SAME subnet.

# Virtual Network : secure-vnet
# Subnet          : subnet1

# MOST IMPORTANT:
# Use SAME SSH PUBLIC KEY as VM1.

# Why?
# Because VM2 must trust the same private key used by VM1.

# ============================================================
# STEP 5 — CONNECT TO VM1
# ============================================================

# Give permission to PEM key:

chmod 400 vm1_key.pem

# Connect to VM1:

ssh -i vm1_key.pem azureuser@VM1_PUBLIC_IP

# Explanation:
# chmod 400 -> read permission only for owner
# SSH uses PEM private key for secure authentication

# ============================================================
# STEP 6 — INSTALL SSH SERVICES
# ============================================================

# Update packages:

sudo apt update

# Install OpenSSH server:

sudo apt install openssh-server -y

# Check SSH service:

sudo systemctl status ssh

# Expected Output:
# active (running)

# ============================================================
# STEP 7 — CREATE TEST FILE
# ============================================================

# Create file:

nano hello.txt

# Add content inside file:

# Secure cloud file sharing successful

# Save and exit.

# ============================================================
# STEP 8 — SECURE FILE TRANSFER USING SCP
# ============================================================

# Find VM2 Private IP:
# Azure Portal -> VM2 -> Networking -> Private IP

# Example:
# 10.0.1.5

# Transfer file securely:

scp -i vm1_key.pem hello.txt azureuser@10.0.1.5:/home/azureuser/

# Explanation:
# SCP = Secure Copy Protocol
# Uses SSH encryption for secure file transfer
# Transfer occurs over PRIVATE IP inside VNet

# Expected Output:
# hello.txt    100%    39     10KB/s   00:00

# Meaning:
# File transfer successful

# ============================================================
# STEP 9 — VERIFY FILE ON VM2
# ============================================================

# Connect to VM2:

ssh -i vm1_key.pem azureuser@10.0.1.5

# Check files:

ls

# Read file:

cat hello.txt

# Expected Output:
# Secure cloud file sharing successful

# ============================================================
# STEP 10 — APPLY FILE PERMISSIONS
# ============================================================

# Secure SSH directory:

chmod 700 ~/.ssh

# Secure authorized_keys:

chmod 600 ~/.ssh/authorized_keys

# Explanation:
# chmod 700 -> only owner gets full access
# chmod 600 -> only owner can read/write

# Security Principle:
# Least Privilege Access Control

# ============================================================
# WHAT TO SHOW IN PRACTICAL
# ============================================================

# 1. Azure Resource Group
# 2. VNet configuration
# 3. VM1 and VM2 inside same VNet
# 4. Private IP communication
# 5. SCP file transfer
# 6. File received successfully
# 7. SSH permissions

# ============================================================
# COMMON FAILURE CASES + SOLUTIONS
# ============================================================

# ------------------------------------------------------------
# FAILURE CASE 1 — Different VNets
# ------------------------------------------------------------

# Problem:
# VM1 cannot connect to VM2 private IP.

# Cause:
# Both VMs are inside different VNets.

# Example:
# vm1 -> vm1-vnet
# vm2 -> secure-vnet

# Solution:
# Both VMs MUST be inside SAME VNet.

# Recommended Fix:
# Delete incorrect VM and recreate properly.

# ------------------------------------------------------------
# FAILURE CASE 2 — Permission denied (publickey)
# ------------------------------------------------------------

# Error:
# Permission denied (publickey)

# Cause:
# VM2 does not trust the SSH key used by VM1.

# Usually happens when:
# VM1 and VM2 use different SSH keys.

# Solution:
# Create both VMs using SAME SSH public key.

# ------------------------------------------------------------
# FAILURE CASE 3 — Wrong Username
# ------------------------------------------------------------

# Wrong:

# ssh -i vm1_key.pem azurenet@10.0.1.5

# Correct:

# ssh -i vm1_key.pem azureuser@10.0.1.5

# Explanation:
# Azure authentication requires BOTH:
# 1. Correct username
# 2. Correct private key

# ------------------------------------------------------------
# FAILURE CASE 4 — SSH Service Not Running
# ------------------------------------------------------------

# Error:
# Connection refused

# Solution:

sudo systemctl start ssh

sudo systemctl enable ssh

# ------------------------------------------------------------
# FAILURE CASE 5 — Host Key Verification Failed
# ------------------------------------------------------------

# Error:
# Host key verification failed

# Cause:
# Old SSH fingerprint stored locally.

# Solution:

ssh-keygen -R 10.0.1.5

# ------------------------------------------------------------
# FAILURE CASE 6 — PEM File Permission Error
# ------------------------------------------------------------

# Error:
# Permissions are too open

# Solution:

chmod 400 vm1_key.pem

# ------------------------------------------------------------
# FAILURE CASE 7 — Incorrect SCP Command
# ------------------------------------------------------------

# Wrong:

# ssh -i vm1_key.pem hello.txt user@ip:~/

# Correct:

scp -i vm1_key.pem hello.txt azureuser@10.0.1.5:/home/azureuser/

# ============================================================
# IMPORTANT VIVA QUESTIONS
# ============================================================

# Q1. What is SCP?
# Secure Copy Protocol used for encrypted file transfer over SSH.

# Q2. Why use SSH keys instead of passwords?
# SSH keys provide stronger authentication and better security.

# Q3. Why use private IP communication?
# Private IP communication stays inside Azure internal network,
# improving security and reducing internet exposure.

# Q4. Why use a VNet?
# VNet allows isolated and secure communication between cloud resources.

# Q5. What is RSA-4096?
# RSA-4096 is a strong asymmetric encryption algorithm using 4096-bit keys.

# Q6. What is Port 22?
# Default SSH communication port.

# Q7. Why use chmod 700 and chmod 600?
# To restrict unauthorized access to SSH credentials and files.

# ============================================================
# SECURITY FEATURES IMPLEMENTED
# ============================================================

# 1. SSH key-based authentication
# 2. SCP encrypted file transfer
# 3. Private VNet communication
# 4. RSA-4096 encryption
# 5. Least privilege permissions
# 6. Internal networking

# ============================================================
# FINAL RESULT
# ============================================================

# Successfully implemented:
# - Secure inter-VM communication
# - Private cloud networking
# - Encrypted file transfer using SCP
# - SSH authentication
# - Access permission hardening

# ============================================================
# HOW TO SAVE AZURE CREDITS
# ============================================================

# Stop VMs after exam:

sudo shutdown now

# OR

# Azure Portal -> VM -> Stop

# BEST OPTION:
# Delete entire Resource Group.

# This removes:
# - VMs
# - disks
# - networking
# - public IPs

# and stops billing completely.

# ============================================================
# END OF ASSIGNMENT
# ============================================================
















# ============================================================
# PROJECT:
# Secure File Sharing Between AWS EC2 Instances
# Using Amazon Linux + SSH + SCP
# ============================================================


# ============================================================
# STEP 1 — Launch 2 Amazon Linux EC2 Instances
# ============================================================

# Open AWS EC2 Console:
# https://console.aws.amazon.com/ec2/

# Create 2 instances:
# 1. Sender-VM
# 2. Receiver-VM

# Configuration:
# AMI            -> Amazon Linux 2023
# Instance Type  -> t2.micro
# Key Pair       -> Create "cloud-key.pem"

# Download and save:
# cloud-key.pem


# ============================================================
# STEP 2 — Configure Security Group
# ============================================================

# Add inbound rules:

# Type   Port   Source
# SSH    22     My IP
# SSH    22     Same Security Group

# Why?
# - First rule allows YOUR PC to connect to EC2.
# - Second rule allows EC2 instances to communicate with each other.


# ============================================================
# STEP 3 — Connect to EC2
# ============================================================

# Amazon Linux username:
# ec2-user

# Give PEM file correct permissions:
chmod 400 cloud-key.pem

# Connect to Sender VM:
ssh -i cloud-key.pem ec2-user@PUBLIC_IP_1

# Connect to Receiver VM:
ssh -i cloud-key.pem ec2-user@PUBLIC_IP_2


# ============================================================
# STEP 4 — Update Packages
# ============================================================

# Run on BOTH instances:

sudo dnf update -y

# Explanation:
# dnf -> package manager for Amazon Linux 2023
# -y  -> automatically answer YES


# ============================================================
# STEP 5 — Create Secure Directory on Receiver VM
# ============================================================

# SSH into Receiver VM first.

# Create directory:
sudo mkdir /secure-share

# Change ownership:
sudo chown ec2-user:ec2-user /secure-share

# Set permissions:
sudo chmod 700 /secure-share

# Meaning of 700:
# Owner  -> Read + Write + Execute
# Others -> No access

# This makes the directory secure.


# ============================================================
# STEP 6 — Copy PEM Key to Sender VM
# ============================================================

# Run from YOUR LOCAL MACHINE:

scp -i cloud-key.pem cloud-key.pem ec2-user@PUBLIC_IP_1:/home/ec2-user/

# Why do this?
# Because Sender VM needs the key to SSH into Receiver VM.


# ============================================================
# STEP 7 — SSH Into Sender VM
# ============================================================

ssh -i cloud-key.pem ec2-user@PUBLIC_IP_1

# Give proper permissions to PEM file INSIDE Sender VM:
chmod 400 cloud-key.pem

# If permissions are wrong, SSH will reject the key.


# ============================================================
# STEP 8 — Test Internal Communication
# ============================================================

# From Sender VM connect to Receiver VM using PRIVATE IP:

ssh -i cloud-key.pem ec2-user@PRIVATE_IP_2

# IMPORTANT:
# Use PRIVATE IP because:
# - Both VMs are inside same VPC
# - Faster and more secure
# - Avoids public internet traffic


# ============================================================
# STEP 9 — Create Sample File
# ============================================================

# On Sender VM:

echo "Hello from Sender VM" > file.txt

# Verify:
cat file.txt


# ============================================================
# STEP 10 — Transfer File Securely Using SCP
# ============================================================

scp -i cloud-key.pem file.txt ec2-user@PRIVATE_IP_2:/secure-share/

# Explanation:
# scp  -> secure copy command
# -i   -> specifies private key
# file.txt -> file to transfer
# /secure-share/ -> destination directory


# ============================================================
# STEP 11 — Verify File on Receiver VM
# ============================================================

# SSH into Receiver VM:

ssh -i cloud-key.pem ec2-user@PUBLIC_IP_2

# Check file:
ls /secure-share

# Expected Output:
# file.txt

# Read file:
cat /secure-share/file.txt

# Expected Output:
# Hello from Sender VM


# ============================================================
# OPTIONAL SECURITY HARDENING
# ============================================================

# Open SSH configuration:
sudo nano /etc/ssh/sshd_config

# Find:
# PasswordAuthentication yes

# Change to:
# PasswordAuthentication no

# Why?
# Disables password login.
# Only SSH key authentication allowed.

# Restart SSH service:
sudo systemctl restart sshd


# ============================================================
# COMMON FAIL CASES + SOLUTIONS
# ============================================================


# ------------------------------------------------------------
# ISSUE 1:
# Permission denied (publickey)
# ------------------------------------------------------------

# Cause:
# - Wrong username
# - Wrong key
# - Wrong permissions on PEM file

# Solution:

chmod 400 cloud-key.pem

# Use correct username:
# Amazon Linux -> ec2-user
# Ubuntu       -> ubuntu
# Azure        -> azureuser


# ------------------------------------------------------------
# ISSUE 2:
# ssh: connect to host timed out
# ------------------------------------------------------------

# Cause:
# Security group does not allow SSH.

# Solution:
# Add inbound rule:
# SSH -> Port 22 -> My IP


# ------------------------------------------------------------
# ISSUE 3:
# SCP hangs forever
# ------------------------------------------------------------

# Cause:
# Receiver VM security group blocks internal SSH.

# Solution:
# Add:
# SSH -> Same Security Group


# ------------------------------------------------------------
# ISSUE 4:
# WARNING: UNPROTECTED PRIVATE KEY FILE!
# ------------------------------------------------------------

# Cause:
# PEM file permissions too open.

# Solution:

chmod 400 cloud-key.pem


# ------------------------------------------------------------
# ISSUE 5:
# No such file or directory
# ------------------------------------------------------------

# Cause:
# Wrong path used in SCP command.

# Solution:
# Verify file exists:

ls

# Then retry SCP.


# ------------------------------------------------------------
# ISSUE 6:
# Permission denied while writing into /secure-share
# ------------------------------------------------------------

# Cause:
# Directory ownership incorrect.

# Solution:

sudo chown ec2-user:ec2-user /secure-share


# ============================================================
# ARCHITECTURE
# ============================================================

#                AWS CLOUD
# ------------------------------------------------
#
#      Sender EC2          Receiver EC2
#    (Amazon Linux)      (Amazon Linux)
#
#           |                  |
#           |---- SCP/SSH ---->|
#           |                  |
#
#     Communication via VPC Private IP
#
# ------------------------------------------------


# ============================================================
# IMPORTANT COMMANDS SUMMARY
# ============================================================

# SSH Login:
ssh -i cloud-key.pem ec2-user@IP

# SCP Transfer:
scp -i cloud-key.pem file.txt ec2-user@PRIVATE_IP:/secure-share/

# Change File Permissions:
chmod 400 cloud-key.pem

# Change Folder Permissions:
chmod 700 /secure-share


# ============================================================
# VIVA QUESTIONS
# ============================================================

# Q1. What is EC2?
# Elastic Compute Cloud.
# AWS virtual machine service.

# Q2. What is SSH?
# Secure Shell protocol used for remote login.

# Q3. What is SCP?
# Secure Copy Protocol for secure file transfer.

# Q4. Difference between Public IP and Private IP?
# Public IP  -> accessible from internet
# Private IP -> internal VPC communication only

# Q5. Why use Private IP between EC2 instances?
# More secure and faster.

# Q6. What is a Security Group?
# Virtual firewall for EC2 instances.

# Q7. Why chmod 400 on PEM file?
# SSH requires private keys to have restricted permissions.

# Q8. What does chmod 700 mean?
# Owner gets full access.
# Others get no access.

# Q9. What is key-based authentication?
# Login using cryptographic key instead of password.

# Q10. Why disable password authentication?
# Improves server security.


# ============================================================
# EXPECTED OUTPUT
# ============================================================

# - Two Amazon Linux EC2 instances communicate securely.
# - File transferred successfully using SCP.
# - Communication happens using Private IP.
# - Secure directory permissions implemented.
# - SSH key authentication used.
# ============================================================
