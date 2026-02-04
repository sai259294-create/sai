# Installation & Execution Guide

## 📦 Prerequisites

- **Python 3.7 or higher** - [Download](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Text Editor** (VS Code, PyCharm, Sublime, etc.)
- **Web Browser** (Chrome, Firefox, Edge, Safari)

---

## 🚀 Quick Start (Windows)

### Step 1: Open PowerShell or Command Prompt

Navigate to the project folder:
```powershell
cd "C:\Users\masir\OneDrive\Desktop\MTIS\flask"
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# If using Command Prompt instead of PowerShell
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.2 Werkzeug-2.3.6 Jinja2-3.1.2 click-8.1.3 itsdangerous-2.1.2
```

### Step 4: Run the Application

```powershell
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

### Step 5: Open in Web Browser

Visit: **http://localhost:5000**

---

## 🔓 Demo Account

Once the application is running:

1. Click **"Login"** in the navigation bar
2. Enter credentials:
   - **Username:** `admin`
   - **Password:** `password123`
3. Click **"Login"**
4. You'll be redirected to the dashboard

---

## 📁 Project Structure After Installation

```
flask/
├── venv/                    (Virtual environment - if created)
├── uploads/                 (User uploads storage)
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── ... (other templates)
│   └── errors/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── CONCEPTS.md
├── PROJECT_SUMMARY.md
└── ... (other files)
```

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution:**
- Install Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart your terminal

### Issue: "Module not found"
**Solution:**
```powershell
# Make sure you're in the project directory
cd "C:\Users\masir\OneDrive\Desktop\MTIS\flask"

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:**

Open `app.py` and change the port:
```python
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)  # Changed from 5000 to 5001
```

Then visit: **http://localhost:5001**

### Issue: "Permission denied on upload"
**Solution:**
- Check `uploads/` folder exists
- Right-click folder > Properties > Security > Edit
- Give your user Write permissions

### Issue: "Session errors"
**Solution:**
- Clear browser cookies
- Close all browser tabs
- Restart Flask application

---

## 🧪 Testing All Features

### 1. Homepage
- [x] Visit http://localhost:5000
- [x] See hero section
- [x] Click featured projects
- [x] Scroll to see all sections

### 2. Navigation
- [x] Click "Home" - redirects to homepage
- [x] Click "About" - shows about page
- [x] Click "Portfolio" - shows all projects
- [x] Click "Skills" - shows technical skills
- [x] Click "Services" - shows services offered
- [x] Click "Contact" - shows contact form

### 3. Contact Form
- [x] Go to Contact page
- [x] Fill in name, email, subject, message
- [x] Click "Send Message"
- [x] See success flash message
- [x] Login to see message in dashboard

### 4. Resume Upload
- [x] Go to Resume page
- [x] Drag or click to upload a PDF/image
- [x] See success message
- [x] Click download to retrieve file

### 5. User Authentication
- [x] Click "Login"
- [x] Enter: username=`admin`, password=`password123`
- [x] Click "Login"
- [x] See dashboard with statistics
- [x] Click "Logout"

### 6. Feedback Form
- [x] Go to Feedback page
- [x] Submit feedback with rating
- [x] Optionally attach a file
- [x] See success message

### 7. Error Pages
- [x] Visit http://localhost:5000/nonexistent
- [x] See 404 error page
- [x] Click back link

---

## 📊 Page Checklist

| Page | URL | Status |
|------|-----|--------|
| Home | http://localhost:5000/ | ✅ |
| About | http://localhost:5000/about | ✅ |
| Portfolio | http://localhost:5000/portfolio | ✅ |
| Project 1 | http://localhost:5000/project/1 | ✅ |
| Skills | http://localhost:5000/skills | ✅ |
| Services | http://localhost:5000/services | ✅ |
| Contact | http://localhost:5000/contact | ✅ |
| Resume | http://localhost:5000/resume | ✅ |
| Feedback | http://localhost:5000/feedback | ✅ |
| Login | http://localhost:5000/login | ✅ |
| Dashboard | http://localhost:5000/dashboard | ✅ |
| Logout | http://localhost:5000/logout | ✅ |
| 404 Error | http://localhost:5000/invalid | ✅ |

---

## 📝 Configuration Options

### Change Debug Mode
In `app.py`:
```python
app.run(debug=False)  # Set to False for production
```

### Change Host & Port
In `app.py`:
```python
app.run(host='0.0.0.0', port=8000)  # Accessible from other computers
```

### Increase Upload Size
In `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

### Change Session Timeout
In `app.py`:
```python
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=30)
```

---

## 🔒 Production Deployment

### Using Gunicorn (Recommended)

```powershell
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Python Built-in Server (Not Recommended for Production)

```powershell
python app.py
```

### Using Windows WSGI (IIS)

1. Install `pywin32` and IIS
2. Create FastCGI handler for Python
3. Configure application pool

---

## 🌐 Making the App Accessible from Other Computers

### Local Network Access

In `app.py`, change:
```python
app.run(host='0.0.0.0', port=5000)
```

Then access from another computer:
```
http://<your-computer-ip>:5000
```

To find your IP address:
```powershell
ipconfig
# Look for "IPv4 Address: 192.168.x.x"
```

---

## 📊 Monitor Application

### View Console Logs
- Watch the terminal for requests
- See any errors or warnings
- Monitor performance

### Check Flask Debug Mode
- Template errors show source code
- Debugger available in browser
- Automatic reloader on file changes

### Disable Debug Mode
```python
app.run(debug=False)  # For production
```

---

## 🧹 Cleanup & Maintenance

### Clear Sessions
```powershell
# Stop the app (Ctrl+C)
# Delete browser cookies
# Restart the app
```

### Clear Uploads
```powershell
# Delete files in uploads/ folder (not .gitkeep)
```

### Reset Database (Session Storage)
```powershell
# Sessions are stored in browser cookies
# Clear browser cookies to reset
```

---

## 🔄 Updating Dependencies

### Check for Updates
```powershell
pip list --outdated
```

### Update All
```powershell
pip install --upgrade -r requirements.txt
```

### Freeze Current Environment
```powershell
pip freeze > requirements.txt
```

---

## 🎯 Development Workflow

### 1. Start Development
```powershell
cd "C:\Users\masir\OneDrive\Desktop\MTIS\flask"
.\venv\Scripts\Activate  # Activate virtual environment
python app.py            # Start Flask
```

### 2. Make Changes
- Edit Python files (auto-reloads)
- Edit HTML templates (refresh browser)
- Edit CSS files (refresh browser)
- Edit JavaScript (hard refresh: Ctrl+Shift+R)

### 3. Test Changes
- Open browser to http://localhost:5000
- Test all functionality
- Check browser console (F12)

### 4. Stop Application
```powershell
# In terminal: Ctrl+C
```

### 5. Deactivate Virtual Environment
```powershell
deactivate
```

---

## 💡 Tips & Best Practices

### Use Virtual Environment
```powershell
# Always use virtual environment
.\venv\Scripts\Activate

# Keep dependencies isolated
pip freeze > requirements.txt
```

### Enable Debug Mode During Development
```python
app.run(debug=True)  # Only for development!
```

### Check File Permissions
- Ensure `uploads/` folder is writable
- Check `venv/` folder accessibility

### Use Browser DevTools
- F12 to open developer tools
- Check Console for JavaScript errors
- Check Network tab for requests

### Monitor Application Logs
- Watch terminal for errors
- Use Flask logging for debugging
- Enable verbose mode if needed

---

## 📚 Additional Resources

### Official Documentation
- [Flask Official Docs](https://flask.palletsprojects.com/)
- [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)

### Tutorials
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Real Python Flask](https://realpython.com/python-web-server-with-flask/)

### Community
- [Flask Discord](https://discord.gg/flask)
- [Stack Overflow - Flask](https://stackoverflow.com/questions/tagged/flask)

---

## ✅ Quick Checklist

Before running the application:

- [ ] Python installed (3.7+)
- [ ] Project folder accessible
- [ ] requirements.txt exists
- [ ] templates/ folder exists
- [ ] static/ folder exists
- [ ] uploads/ folder exists

After installing dependencies:

- [ ] Flask installed successfully
- [ ] All imports working
- [ ] app.py runs without errors
- [ ] Browser opens to localhost:5000
- [ ] All pages load correctly

---

## 🆘 Getting Help

### Check Logs
1. Look at terminal output
2. Check browser console (F12)
3. Review error messages carefully

### Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| ModuleNotFoundError | Missing dependency | `pip install -r requirements.txt` |
| Port already in use | Port 5000 busy | Change port in app.py |
| Template not found | Missing file | Check file path |
| 404 error | Route not found | Check URL spelling |
| File upload fails | Permission issue | Check folder permissions |

---

## 🚀 You're Ready!

Everything is set up. Now:

1. **Start the application:**
   ```powershell
   python app.py
   ```

2. **Open browser:**
   ```
   http://localhost:5000
   ```

3. **Explore the website:**
   - Navigate through all pages
   - Test all forms
   - Try all features

4. **Login (optional):**
   - Username: `admin`
   - Password: `password123`

---

**Enjoy your Flask portfolio website! 🎉**
