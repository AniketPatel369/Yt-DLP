# 🚀 Server Setup Guide - Fix YouTube Extraction Errors

## 🔧 **Quick Fix for Your Server Error**

Your error indicates missing cookies and server-specific issues. Here's how to fix it:

### **1. Update Your Server Code**
Upload the updated `multi_platform_service.py` with the cookie-handling fixes.

### **2. Server Commands to Run**

#### **Option A: Extract Cookies on Server (Recommended)**
```bash
# Install browser on server
sudo apt update
sudo apt install chromium-browser xvfb

# Extract cookies using yt-dlp
yt-dlp --cookies-from-browser chromium --dump-json "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > /dev/null
```

#### **Option B: Create Empty Cookie Files (Temporary)**
```bash
# Navigate to your app directory
cd /path/to/your/app

# Create empty cookie files to prevent errors
touch www.youtube.com_cookies.txt
touch www.instagram.com_cookies.txt
touch www.facebook.com_cookies.txt

# Restart your application
sudo systemctl restart your-app-service
```

#### **Option C: Test Without Cookies**
```bash
# Test yt-dlp directly on your server
yt-dlp --dump-json --no-warnings "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### **3. Server Environment Setup**

#### **Install Required Packages**
```bash
# Update system
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install yt-dlp globally
pip3 install yt-dlp

# Or via system package manager
sudo apt install yt-dlp
```

#### **Create Virtual Environment**
```bash
cd /path/to/your/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **4. Production Deployment**

#### **Using Systemd Service**
Create `/etc/systemd/system/ytdlp-extractor.service`:
```ini
[Unit]
Description=yt-dlp JSON Extractor
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
ExecStart=/path/to/your/app/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then run:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ytdlp-extractor
sudo systemctl start ytdlp-extractor
sudo systemctl status ytdlp-extractor
```

#### **Using Nginx (Optional)**
Create `/etc/nginx/sites-available/ytdlp-extractor`:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### **5. Debug Commands**

#### **Check if yt-dlp works**
```bash
python3 -m yt_dlp --version
python3 -m yt_dlp --dump-json "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### **Check your app**
```bash
# Test the health endpoint
curl http://localhost:5000/health

# Test YouTube extraction
curl "http://localhost:5000/?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### **Check logs**
```bash
# Application logs
sudo journalctl -u ytdlp-extractor -f

# Nginx logs (if using)
sudo tail -f /var/log/nginx/error.log
```

### **6. Cookie Management for Production**

#### **Extract Cookies Safely**
```bash
# Create a script to refresh cookies
#!/bin/bash
# refresh-cookies.sh

echo "Refreshing YouTube cookies..."
cd /path/to/your/app

# Use a headless browser to get fresh cookies
yt-dlp --cookies-from-browser chrome --dump-json "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Cookies refreshed successfully"
    sudo systemctl restart ytdlp-extractor
else
    echo "❌ Cookie refresh failed"
fi
```

#### **Automated Cookie Refresh (Cron)**
```bash
# Add to crontab: crontab -e
0 2 * * * /path/to/refresh-cookies.sh >> /var/log/cookie-refresh.log 2>&1
```

### **7. Testing Your Fixed Setup**

```bash
# Test the specific URL that was failing
curl -X GET "http://localhost:5000/?url=https://www.youtube.com/watch?v=m4_9TFeMfJE"

# Should return JSON with video metadata, not an error
```

## 🆘 **If Still Having Issues:**

1. **Check server IP**: Use a VPN or different server location
2. **Use residential proxy**: For high-volume extraction
3. **Enable debug logging**: Add more verbose logging to see exact errors
4. **Consider YouTube API**: For commercial use with higher reliability

The updated code I provided will handle missing cookies gracefully and use multiple fallback strategies! 🎯
