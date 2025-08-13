# 🔒 Important Files to Keep Private

## ⚠️ **NEVER COMMIT THESE FILES:**

### 🍪 **Cookie Files** (SENSITIVE)
```
www.youtube.com_cookies.txt
www.instagram.com_cookies.txt  
www.facebook.com_cookies.txt
```
**Why**: Contains authentication tokens and session data

### 📁 **Virtual Environment**
```
source/
venv/
env/
```
**Why**: Large files, platform-specific, should be recreated

### 🐍 **Python Cache**
```
__pycache__/
*.pyc
*.pyo
```
**Why**: Compiled bytecode, regenerated automatically

### 📊 **Data Files**
```
*.json (except config files)
gt.json
new.json
```
**Why**: May contain extracted video data or temporary results

### 📝 **Log Files**
```
*.log
logs/
```
**Why**: Runtime logs, may contain sensitive URLs or errors

## ✅ **Safe to Commit:**

- Application code (`app/`, `config/`, `static/`)
- Requirements (`requirements.txt`)
- Documentation (`README.md`, `*.md`)
- Entry point (`run.py`)
- Configuration templates (without sensitive data)

## 🛠️ **Setup for New Developers:**

1. Clone the repository
2. Create virtual environment: `python -m venv source`
3. Activate: `source/Scripts/activate` (Windows) or `source source/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Add your own cookie files (don't commit them!)
6. Run: `python run.py`

## 🔐 **Security Best Practices:**

- **Never share cookie files** - they contain login sessions
- **Use environment variables** for API keys and secrets
- **Regular cookie refresh** - cookies expire and need updating
- **Different cookies per environment** - dev/staging/production
