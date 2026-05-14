const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
const blogRoutes = require('./routes/blogRoutes');
app.use('/api/blogs', blogRoutes);

// Root Route
app.get('/', (req, res) => {
    res.send('MERN Blog API is running on VM...');
});

// MongoDB Connection (Local Instance)
mongoose.connect(process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/mern-blog')
    .then(() => {
        console.log('Connected to Local MongoDB');
        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });
    })
    .catch(err => {
        console.error('Database connection error:', err);
    });



/******************************************************************
 * AZURE MERN DEPLOYMENT GUIDE (BEGINNER FRIENDLY)
 *
 * STACK:
 * Frontend  -> React + Axios
 * Backend   -> Node.js + Express
 * Database  -> MongoDB
 * Process   -> PM2
 * Webserver -> Nginx
 * OS        -> Ubuntu VM on Azure
 ******************************************************************/

/******************************************************************
 * STEP 1 — CREATE AZURE VM
 ******************************************************************/

// 1. Open Azure Portal
// https://portal.azure.com

// 2. Create Virtual Machine

/*
Recommended Settings:

VM Name:
mern-vm

Image:
Ubuntu Server 24.04 LTS - x64 Gen2

Size:
B1s / B2ats_v2 (free/student friendly)

Authentication:
SSH Public Key

Open Ports:
22 -> SSH
80 -> HTTP
*/

// 3. Create SSH key on your local machine

/*
Mac/Linux:
ssh-keygen

Show public key:
cat ~/.ssh/id_rsa.pub

Copy ENTIRE output and paste into Azure SSH key field
*/

// 4. Click Create

/******************************************************************
 * STEP 2 — CONNECT TO VM
 ******************************************************************/

// After VM deployment finishes:

// Find:
// VM -> Overview -> Public IP

// Connect using SSH:

/*
ssh azureuser@YOUR_PUBLIC_IP
*/

// Example:
/*
ssh azureuser@20.244.xx.xx
*/

// First time:
// Type "yes"

// If terminal becomes:
/*
azureuser@mern-vm:~$
*/

// You are now inside Ubuntu cloud server

/******************************************************************
 * STEP 3 — UPDATE UBUNTU
 ******************************************************************/

/*
sudo apt update
sudo apt upgrade -y
*/

/******************************************************************
 * STEP 4 — INSTALL GIT
 ******************************************************************/

/*
sudo apt install git -y
*/

/******************************************************************
 * STEP 5 — INSTALL NODE.JS
 ******************************************************************/

// Download Node.js setup

/*
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
*/

// Install Node.js

/*
sudo apt install -y nodejs
*/

// Verify installation

/*
node -v
npm -v
*/

/******************************************************************
 * STEP 6 — INSTALL PM2
 ******************************************************************/

// PM2 keeps backend running even if terminal closes

/*
sudo npm install -g pm2
*/

// Verify

/*
pm2 -v
*/

/******************************************************************
 * STEP 7 — INSTALL MONGODB
 ******************************************************************/

// Import MongoDB key

/*
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
--dearmor
*/

// Add MongoDB repository

/*
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
*/

// Update packages

/*
sudo apt update
*/

// Install MongoDB

/*
sudo apt install -y mongodb-org
*/

// Start MongoDB

/*
sudo systemctl start mongod
sudo systemctl enable mongod
*/

// Check status

/*
sudo systemctl status mongod
*/

/******************************************************************
 * STEP 8 — CLONE YOUR PROJECT
 ******************************************************************/

// Upload code to GitHub first

// Then clone inside VM

/*
git clone YOUR_GITHUB_REPO_URL
*/

// Example:
/*
git clone https://github.com/username/project.git
*/

// Enter project

/*
cd project
*/

/******************************************************************
 * EXPECTED PROJECT STRUCTURE
 ******************************************************************/

/*
project/
│
├── backend/
│   ├── server.js
│   ├── package.json
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
*/

/******************************************************************
 * STEP 9 — SETUP BACKEND
 ******************************************************************/

// Enter backend folder

/*
cd backend
*/

// Install dependencies

/*
npm install
*/

// Create environment file

/*
nano .env
*/

// Example .env content:

/*
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/eventdb
*/

// Save nano:
/*
CTRL + X
Y
ENTER
*/

/******************************************************************
 * STEP 10 — START BACKEND USING PM2
 ******************************************************************/

// Start backend

/*
pm2 start server.js --name backend
*/

// View running processes

/*
pm2 list
*/

// Save PM2 configuration

/*
pm2 startup
pm2 save
*/

/******************************************************************
 * STEP 11 — SETUP FRONTEND
 ******************************************************************/

// Go frontend

/*
cd ../frontend
*/

// Install dependencies

/*
npm install
*/

// Build React app

/*
npm run build
*/

/******************************************************************
 * STEP 12 — INSTALL NGINX
 ******************************************************************/

/*
sudo apt install nginx -y
*/

/******************************************************************
 * STEP 13 — DEPLOY REACT BUILD
 ******************************************************************/

// Remove default nginx files

/*
sudo rm -rf /var/www/html/*
*/

// Copy React build files

/*
sudo cp -r build/* /var/www/html/
*/

/******************************************************************
 * STEP 14 — CONFIGURE NGINX
 ******************************************************************/

// Open nginx config

/*
sudo nano /etc/nginx/sites-available/default
*/

// Replace with:

/*

server {
    listen 80;

    location / {
        root /var/www/html;
        index index.html;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
    }
}

*/

// Save:
/*
CTRL + X
Y
ENTER
*/

/******************************************************************
 * STEP 15 — RESTART NGINX
 ******************************************************************/

/*
sudo systemctl restart nginx
*/

/******************************************************************
 * STEP 16 — OPEN WEBSITE
 ******************************************************************/

// Browser:

/*
http://YOUR_PUBLIC_IP
*/

// Your MERN app is now live

/******************************************************************
 * USEFUL COMMANDS
 ******************************************************************/

// Check backend logs

/*
pm2 logs
*/

// Restart backend

/*
pm2 restart backend
*/

// Stop backend

/*
pm2 stop backend
*/

// Check nginx status

/*
sudo systemctl status nginx
*/

// Restart nginx

/*
sudo systemctl restart nginx
*/

// Check MongoDB status

/*
sudo systemctl status mongod
*/

/******************************************************************
 * IMPORTANT VIVA QUESTIONS
 ******************************************************************/

/*

Q. What is PM2?
A. PM2 is a Node.js process manager used to keep backend
   applications running continuously.

Q. What is Nginx?
A. Nginx is a web server and reverse proxy used to serve
   frontend files and forward API requests.

Q. Why use port 80?
A. Port 80 is used for HTTP web traffic.

Q. Why use SSH?
A. SSH provides secure remote login into the VM.

Q. What is MongoDB?
A. MongoDB is a NoSQL database used to store application data.

Q. What is a VM?
A. A Virtual Machine is a cloud-hosted virtual computer.

*/

/******************************************************************
 * AFTER PRACTICE
 ******************************************************************/

// VERY IMPORTANT

// Stop VM from Azure portal after use
// otherwise credits may continue being consumed

/*
Azure Portal
-> Virtual Machine
-> Stop
*/

/******************************************************************
 * END
 ******************************************************************/
 
