# 🚀 Server Deployment Guide for yt-dlp Extractor

## 🤖 Common Server Issues & Solutions

### Problem: "Sign in to confirm you're not a bot"
This error occurs because YouTube's bot detection is more aggressive for server IPs.

## 🛠️ Solutions

### 1. **Extract Fresh Cookies on Server** (Recommended)

#### Method A: Browser Extension
```bash
# On your server, install a browser and extract cookies
sudo apt update
sudo apt install chromium-browser

# Extract cookies using yt-dlp
yt-dlp --cookies-from-browser chromium --dump-json "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### Method B: Manual Cookie Extraction
1. On your local machine, visit YouTube in browser
2. Export cookies using browser extension like "Get cookies.txt LOCALLY"
3. Upload the cookies file to your server

### 2. **Update Server Configuration**

#### Environment Variables
```bash
# Add to your server environment
export PYTHONPATH="/path/to/your/app"
export FLASK_ENV="production"
export YT_DLP_CONFIG_DIR="/path/to/cookies"
```

#### Nginx Configuration (if using)
```nginx
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

### 3. **Cookie Refresh Script**

Create an automated cookie refresh script:

```bash
#!/bin/bash
# cookie_refresh.sh

echo "🍪 Refreshing YouTube cookies..."

# Backup old cookies
cp www.youtube.com_cookies.txt www.youtube.com_cookies.txt.backup

# Extract fresh cookies (requires headless browser setup)
yt-dlp --cookies-from-browser chrome --cookies cookies_temp.txt --dump-json "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    mv cookies_temp.txt www.youtube.com_cookies.txt
    echo "✅ Cookies updated successfully"
    # Restart your application
    sudo systemctl restart ytdlp-extractor
else
    echo "❌ Cookie update failed, keeping old cookies"
    rm -f cookies_temp.txt
fi
```

### 4. **Systemd Service Configuration**

```ini
# /etc/systemd/system/ytdlp-extractor.service
[Unit]
Description=yt-dlp JSON Extractor
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/venv/bin
Environment=FLASK_ENV=production
ExecStart=/path/to/your/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5. **Server-Specific Optimizations**

#### Use Different User Agents
The app now tries multiple user agents:
- Mobile Safari (iPhone)
- Desktop Chrome (Linux)
- Minimal yt-dlp agent

#### Geographic Bypass
Added `--geo-bypass` and `--geo-bypass-country` options for region-locked content.

#### Retry Logic
Enhanced retry mechanisms with:
- `--extractor-retries 5`
- `--fragment-retries 3`
- `--retry-sleep 5`

## 🔄 Regular Maintenance

### Daily Cookie Refresh (Cron Job)
```bash
# Add to crontab
0 2 * * * /path/to/cookie_refresh.sh >> /var/log/ytdlp-cookies.log 2>&1
```

### Monitor Application Logs
```bash
# View real-time logs
sudo journalctl -u ytdlp-extractor -f

# Check for bot detection errors
grep "bot" /var/log/ytdlp-extractor.log
```

## 🆘 Troubleshooting

### If Still Getting Bot Errors:

1. **Use a VPN on server** to get residential IP
2. **Implement request throttling** (longer sleep intervals)
3. **Use rotating proxies** for high-volume usage
4. **Consider YouTube API** for commercial applications

### Emergency Fallback:
The app now has 3 fallback strategies that try different approaches when the primary method fails.

## 📊 Production Tips

1. **Monitor success rates** - log extraction success/failure
2. **Implement caching** - avoid re-extracting same videos
3. **Use load balancer** - distribute requests across multiple servers
4. **Set up alerts** - notify when bot detection increases

## 🔐 Security Notes

- Keep cookies files secure (chmod 600)
- Use environment variables for sensitive config
- Regularly rotate cookies
- Monitor for unauthorized access
