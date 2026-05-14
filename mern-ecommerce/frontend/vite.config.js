import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
})

```js
// COMPLETE MERN STACK DEPLOYMENT GUIDE ON AWS
// ===========================================

// ARCHITECTURE
// React Frontend (Vite)
//        ↓
// AWS S3 Static Hosting
//        ↓ API Calls
// Node.js + Express Backend
//        ↓
// AWS EC2 Virtual Machine
//        ↓
// MongoDB Atlas Cloud Database

// =====================================================
// PART 1 — CREATE AWS ACCOUNT
// =====================================================

// 1. Go to AWS.
// 2. Create AWS account.
// 3. Add billing information.
// 4. Login to AWS Console.

// NOTE:
// AWS free tier is limited.
// EC2/S3 may incur charges later.

// =====================================================
// PART 2 — CREATE EC2 INSTANCE
// =====================================================

// AWS Console → EC2 → Launch Instance

// Name:
// mern-backend-server

// AMI:
// Amazon Linux 2023
// OR Ubuntu 22.04

// Instance Type:
// t2.micro

// Create Key Pair:
// mern-key.pem

// IMPORTANT:
// Download and save PEM file.
// Used for SSH login.

// SECURITY GROUP PORTS:
// 22   → SSH
// 80   → HTTP
// 5000 → Backend API

// Launch instance.

// =====================================================
// PART 3 — CONNECT TO EC2
// =====================================================

// Open terminal.

// Go to Downloads:
// cd Downloads

// Give PEM correct permissions:
// chmod 400 mern-key.pem

// SSH into EC2:
// ssh -i mern-key.pem ec2-user@YOUR_PUBLIC_IP

// Example:
// ssh -i mern-key.pem ec2-user@3.27.91.5

// If Ubuntu:
// ssh -i mern-key.pem ubuntu@YOUR_PUBLIC_IP

// =====================================================
// PART 4 — INSTALL REQUIRED SOFTWARE
// =====================================================

// AMAZON LINUX:
// Install Git:
// sudo yum install git -y

// Install Node.js:
// curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
// sudo yum install nodejs -y

// UBUNTU:
// sudo apt update
// sudo apt install git -y
// curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
// sudo apt install nodejs -y

// Verify installation:
// node -v
// npm -v

// =====================================================
// PART 5 — CLONE PROJECT
// =====================================================

// Clone GitHub repo:
// git clone YOUR_GITHUB_REPO

// Example:
// git clone https://github.com/username/project.git

// Go backend folder:
// cd project/backend

// Install dependencies:
// npm install

// =====================================================
// PART 6 — SETUP MONGODB ATLAS
// =====================================================

// MongoDB Atlas = cloud-hosted MongoDB database.

// 1. Create Atlas account.
// 2. Create free M0 cluster.
// 3. Create database user.

// Example:
// Username: admin
// Password: mern123

// 4. Go Network Access.
// Add:
// 0.0.0.0/0

// Meaning:
// Allow access from anywhere.

// 5. Get connection string:
// Cluster → Connect → Drivers

// Example:
// mongodb+srv://admin:mern123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

// =====================================================
// PART 7 — CREATE .ENV FILE
// =====================================================

// Inside backend folder:
// nano .env

// Example:
// PORT=5000
// MONGO_URI=mongodb+srv://admin:mern123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
// JWT_SECRET=secret

// Save Nano:
// CTRL + O
// ENTER
// CTRL + X

// =====================================================
// PART 8 — SETUP PM2
// =====================================================

// PM2 keeps backend alive continuously.

// Install PM2:
// sudo npm install -g pm2

// Start backend:
// pm2 start server.js

// OR:
// pm2 start app.js

// Check status:
// pm2 status

// Enable auto startup:
// pm2 save
// pm2 startup

// Run command PM2 gives.

// =====================================================
// PART 9 — TEST BACKEND
// =====================================================

// Open browser:
// http://YOUR_PUBLIC_IP:5000

// Example:
// http://3.27.91.5:5000

// =====================================================
// PART 10 — FRONTEND SETUP
// =====================================================

// On local machine:
// cd frontend

// Install frontend dependencies:
// npm install

// Create/Edit .env:
// nano .env

// IMPORTANT:
// Use PUBLIC IP.
// DO NOT use localhost.

// Example:
// VITE_API_URL=http://3.27.91.5:5000/api/blogs

// Build frontend:
// npm run build

// dist/ folder gets created.

// =====================================================
// PART 11 — S3 FRONTEND HOSTING
// =====================================================

// AWS Console → S3

// Create bucket:
// Example:
// mern-frontend-app

// Disable:
// Block all public access

// Enable:
// Static Website Hosting

// Index document:
// index.html

// Add bucket policy:

// {
//   "Version": "2012-10-17",
//   "Statement": [
//     {
//       "Sid": "PublicRead",
//       "Effect": "Allow",
//       "Principal": "*",
//       "Action": "s3:GetObject",
//       "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
//     }
//   ]
// }

// Upload ALL contents INSIDE dist/:
// index.html
// assets/

// IMPORTANT:
// Do NOT upload dist folder itself.

// Open:
// Bucket → Properties → Static Website Hosting

// Copy endpoint URL.

// =====================================================
// PART 12 — CORS SETUP
// =====================================================

// In backend server.js:

// const cors = require('cors');

// app.use(cors({
//   origin: '*',
//   methods: ['GET', 'POST', 'PUT', 'DELETE'],
//   credentials: true
// }));

// Restart backend:
// pm2 restart all

// =====================================================
// COMMON ERRORS + FIXES
// =====================================================

// ERROR:
// Permission denied (publickey)

// FIX:
// chmod 400 key.pem

// -----------------------------------------------------

// ERROR:
// apt command not found

// CAUSE:
// Using Amazon Linux.

// FIX:
// Use yum instead of apt.

// -----------------------------------------------------

// ERROR:
// bad auth : authentication failed

// FIX:
// Wrong MongoDB username/password.

// -----------------------------------------------------

// ERROR:
// Network Error in frontend

// FIXES:
// 1. Backend not running
// 2. Wrong VITE_API_URL
// 3. CORS issue

// -----------------------------------------------------

// ERROR:
// Blank S3 page

// FIX:
// Upload BOTH:
// index.html
// assets/

// -----------------------------------------------------

// ERROR:
// Vite requires newer Node version

// FIX:
// nvm install 22
// nvm use 22

// =====================================================
// IMPORTANT COMMANDS
// =====================================================

// PM2:
// pm2 status
// pm2 logs
// pm2 restart all
// pm2 stop all

// Linux:
// ls
// cd
// pwd
// nano filename
// cat filename

// Network:
// sudo lsof -i :5000

// =====================================================
// THEORY QUESTIONS
// =====================================================

// What is EC2?
// Cloud virtual machine service.

// What is S3?
// Object storage for static files.

// What is PM2?
// Node.js process manager.

// What is MongoDB Atlas?
// Cloud-hosted MongoDB database.

// What is CORS?
// Allows frontend and backend on different origins to communicate.

// What is SSH?
// Secure remote login protocol.

// What is Vite?
// Frontend build tool.

// =====================================================
// VIVA QUESTIONS
// =====================================================

// 1. What is MERN stack?
// 2. Why use MongoDB?
// 3. Difference between SQL and MongoDB?
// 4. What is Express.js?
// 5. What is PM2?
// 6. What is EC2?
// 7. What is S3?
// 8. Why separate frontend and backend?
// 9. What is static website hosting?
// 10. What is a security group?
// 11. Why use environment variables?
// 12. What is CORS?
// 13. Why does localhost fail after deployment?
// 14. Difference between HTTP and HTTPS?
// 15. What is a virtual machine?

// =====================================================
// FINAL DEPLOYMENT FLOW
// =====================================================

// 1. Create EC2
// 2. Open ports
// 3. SSH into EC2
// 4. Install Node.js + Git
// 5. Clone backend
// 6. Setup MongoDB Atlas
// 7. Create .env
// 8. Start backend using PM2
// 9. Test backend
// 10. Configure frontend API URL
// 11. Build frontend
// 12. Create S3 bucket
// 13. Enable static hosting
// 14. Upload dist files
// 15. Test frontend/backend communication

// =====================================================
// FINAL RESULT
// =====================================================

// Frontend → AWS S3
// Backend → AWS EC2
// Database → MongoDB Atlas

// Standard real-world MERN deployment architecture.
```

