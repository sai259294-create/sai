# Flask Concepts Coverage - Detailed Documentation

This document maps all Flask concepts covered in this portfolio website.

---

## 1. Flask Web Framework & WSGI

### What is Covered:
- ✅ Flask application initialization
- ✅ WSGI compliance (werkzeug)
- ✅ Request-response cycle
- ✅ Application routing

### Files:
- `app.py` - Main Flask application

### Code Example:
```python
from flask import Flask

app = Flask(__name__)

# WSGI-compliant application
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
```

---

## 2. Werkzeug & WSGI

### What is Covered:
- ✅ Werkzeug for HTTP utilities
- ✅ Secure filename handling
- ✅ File upload processing
- ✅ Request/Response objects
- ✅ Exception handling

### Files:
- `app.py` - File upload handling
- `templates/resume.html` - File input handling

### Code Example:
```python
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Secure filename handling
filename = secure_filename(file.filename)
file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

---

## 3. Jinja2 Template Engine

### What is Covered:
- ✅ Template variables: `{{ variable }}`
- ✅ Template loops: `{% for item in items %}`
- ✅ Conditionals: `{% if condition %}`
- ✅ Template inheritance: `{% extends %}`
- ✅ Template blocks: `{% block %}`
- ✅ Template filters: `{{ text|length }}`
- ✅ Context processors: `@app.context_processor`

### Files:
- `templates/base.html` - Base template with blocks
- All template files - Template inheritance

### Code Example:
```html
<!-- base.html -->
{% for project in projects %}
    <div class="project">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description }}</p>
        {% if project.image %}
            <img src="{{ project.image }}" alt="{{ project.title }}">
        {% endif %}
    </div>
{% endfor %}
```

```python
# Context processor
@app.context_processor
def inject_user():
    return {
        'current_user': session.get('user'),
        'is_logged_in': 'user' in session
    }
```

---

## 4. Flask Application Components

### What is Covered:
- ✅ Application initialization
- ✅ Configuration management
- ✅ Secret key setup
- ✅ Error handlers
- ✅ Context processors
- ✅ Decorators

### Files:
- `app.py` - Application setup
- `config.py` - Configuration classes

### Code Example:
```python
# Application initialization
app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
```

---

## 5. Routing

### What is Covered:
- ✅ Basic routes: `@app.route('/')`
- ✅ Multiple HTTP methods: `@app.route('/', methods=['GET', 'POST'])`
- ✅ URL building: `url_for()`
- ✅ Redirect: `redirect()`
- ✅ Route organization
- ✅ Error routes

### Files:
- `app.py` - All routes
- `templates/base.html` - URL building with url_for()

### Code Example:
```python
# Simple route
@app.route('/')
def index():
    return render_template('index.html')

# Route with multiple methods
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle POST
        return redirect(url_for('contact'))
    return render_template('contact.html')

# URL building in templates
<a href="{{ url_for('portfolio') }}">Portfolio</a>
<a href="{{ url_for('project_detail', project_id=1) }}">View Project</a>
```

---

## 6. Variable Rules (Dynamic Routes)

### What is Covered:
- ✅ Integer variable: `<int:id>`
- ✅ String variable: `<name>`
- ✅ Path variable: `<path:filepath>`
- ✅ UUID variable: `<uuid:id>`
- ✅ Converters: Custom type conversion

### Files:
- `app.py` - project_detail route

### Code Example:
```python
# Variable rule with integer converter
@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = next((p for p in PORTFOLIO_ITEMS if p['id'] == project_id), None)
    if project is None:
        flash('Project not found!', 'danger')
        return redirect(url_for('portfolio'))
    return render_template('project_detail.html', project=project)

# In template
{% for project in projects %}
    <a href="{{ url_for('project_detail', project_id=project.id) }}">
        {{ project.title }}
    </a>
{% endfor %}
```

---

## 7. URL Building

### What is Covered:
- ✅ url_for() function
- ✅ Dynamic URL generation
- ✅ URL parameters
- ✅ Anchor tags with URLs
- ✅ Form action URLs

### Files:
- All template files - Heavy use of url_for()
- `app.py` - redirect() with url_for()

### Code Example:
```html
<!-- Template -->
<a href="{{ url_for('index') }}">Home</a>
<a href="{{ url_for('portfolio') }}">Portfolio</a>
<a href="{{ url_for('project_detail', project_id=1) }}">Project 1</a>

<!-- Form action -->
<form method="POST" action="{{ url_for('contact') }}">
    <!-- form fields -->
</form>

<!-- Redirect -->
{{ url_for('contact') }}?message=Success
```

```python
# Python
return redirect(url_for('dashboard'))
return redirect(url_for('index', message='Welcome!'))
```

---

## 8. HTTP Methods

### What is Covered:
- ✅ GET requests
- ✅ POST requests
- ✅ Method checking: `request.method`
- ✅ Form submission
- ✅ File upload (multipart/form-data)
- ✅ Redirect after POST

### Files:
- `app.py` - All routes with methods
- All form templates - GET/POST handling

### Code Example:
```python
# GET - Display form
# POST - Process form data
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Process and save
        flash(f'Thank you {name}!', 'success')
        return redirect(url_for('contact'))
    
    # GET request - display form
    return render_template('contact.html')

# POST with file upload
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        if 'resume_file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(url_for('resume'))
        
        file = request.files['resume_file']
        # Process file
        return redirect(url_for('resume'))
    
    return render_template('resume.html')
```

---

## 9. Templates

### What is Covered:
- ✅ Template rendering: `render_template()`
- ✅ Template inheritance
- ✅ Template blocks
- ✅ Template variables
- ✅ Template loops and conditionals
- ✅ Filters
- ✅ Macros
- ✅ Static file references

### Files:
- `templates/base.html` - Base template
- All other template files - Child templates

### Code Example:
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    {% block content %}{% endblock %}
</body>
</html>

<!-- Child template -->
{% extends "base.html" %}

{% block title %}Home - My Portfolio{% endblock %}

{% block content %}
    <h1>Welcome</h1>
    {% for project in projects %}
        <div class="project">
            <h2>{{ project.title }}</h2>
            <p>{{ project.description|truncate(100) }}</p>
        </div>
    {% endfor %}
{% endblock %}
```

```python
# Python
from flask import render_template

@app.route('/')
def index():
    projects = get_projects()
    return render_template('index.html', projects=projects)
```

---

## 10. Static Files

### What is Covered:
- ✅ CSS files serving
- ✅ JavaScript files serving
- ✅ Image serving
- ✅ Static file configuration
- ✅ url_for() for static files

### Files:
- `static/css/style.css` - Stylesheet
- `static/js/script.js` - JavaScript
- `static/images/` - Image directory
- All templates - Static file references

### Code Example:
```html
<!-- Template -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

```python
# Configuration
app.static_folder = 'static'
app.static_url_path = '/static'
```

---

## 11. Request Object

### What is Covered:
- ✅ Form data: `request.form`
- ✅ Files: `request.files`
- ✅ Query parameters: `request.args`
- ✅ Method: `request.method`
- ✅ Headers: `request.headers`
- ✅ Cookies: `request.cookies`

### Files:
- `app.py` - All routes using request object

### Code Example:
```python
from flask import request

# Form data
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    
# File upload
@app.route('/resume', methods=['POST'])
def resume():
    if 'resume_file' in request.files:
        file = request.files['resume_file']
    
# Query parameters
@app.route('/')
def index():
    message = request.args.get('message', 'Default')
    
# Check method
if request.method == 'POST':
    # Process POST
    pass

# Headers
user_agent = request.headers.get('User-Agent')

# Cookies
session_id = request.cookies.get('session_id')
```

---

## 12. Form Data Processing

### What is Covered:
- ✅ GET form data
- ✅ POST form data
- ✅ Form validation
- ✅ File upload handling
- ✅ Error handling
- ✅ Data storage (session)

### Files:
- `app.py` - contact(), resume(), feedback() routes
- All form templates

### Code Example:
```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Validate
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not all([name, email]):
            flash('Please fill all fields!', 'danger')
            return redirect(url_for('contact'))
        
        # Process
        contact_data = {
            'name': name,
            'email': email,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Store in session
        contacts = session.get('contacts', [])
        contacts.append(contact_data)
        session['contacts'] = contacts
        
        flash('Thank you!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')
```

---

## 13. Sending Form Data to Templates

### What is Covered:
- ✅ Passing variables to templates
- ✅ Data structures: lists, dicts
- ✅ Context data
- ✅ Default values

### Files:
- All routes and templates

### Code Example:
```python
# Pass single variable
@app.route('/about')
def about():
    user_name = session.get('user', 'Guest')
    return render_template('about.html', user_name=user_name)

# Pass multiple variables
@app.route('/')
def index():
    projects = PORTFOLIO_ITEMS[:3]
    skills = SKILLS
    return render_template('index.html', projects=projects, skills=skills)

# Pass complex data
@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    contacts = session.get('contacts', [])
    visits = session.get('visits', 0)
    return render_template('dashboard.html', user=user, contacts=contacts, visits=visits)
```

```html
<!-- Template -->
{{ user_name }}

{% for project in projects %}
    {{ project.title }}
{% endfor %}

{% for category, skill_list in skills.items() %}
    <h3>{{ category }}</h3>
{% endfor %}
```

---

## 14. Cookies

### What is Covered:
- ✅ Reading cookies: `request.cookies`
- ✅ Session vs cookies
- ✅ Session configuration
- ✅ Secure cookie handling

### Files:
- `app.py` - Session configuration
- All routes using sessions

### Code Example:
```python
# Session (uses cookies internally)
from flask import session

# Store in session
session['user'] = username
session['visits'] = visits + 1

# Read from session
current_user = session.get('user')

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # JS can't access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
```

---

## 15. Sessions

### What is Covered:
- ✅ Session creation
- ✅ Session storage
- ✅ Session access
- ✅ Session clearing
- ✅ Permanent sessions
- ✅ Session expiration
- ✅ User authentication

### Files:
- `app.py` - Session management in login, logout, dashboard
- All templates accessing session data

### Code Example:
```python
from flask import session
from datetime import timedelta

# Configure session
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(days=7)

# Store in session
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password == 'password123':
        session['user'] = username
        
        # Remember me
        if request.form.get('remember'):
            session.permanent = True
        
        return redirect(url_for('dashboard'))

# Access session data
@app.before_request
def load_logged_in_user():
    user_id = session.get('user')

# Clear session (logout)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# In templates
{% if 'user' in session %}
    Welcome, {{ session['user'] }}!
{% endif %}
```

---

## 16. Redirects

### What is Covered:
- ✅ Redirect to routes: `redirect(url_for())`
- ✅ Redirect with parameters
- ✅ Redirect after form submission (PRG pattern)
- ✅ Conditional redirects
- ✅ Login redirects

### Files:
- `app.py` - Multiple routes using redirect()

### Code Example:
```python
from flask import redirect, url_for

# Simple redirect
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Redirect with message
return redirect(url_for('index', message='Welcome!'))

# Redirect with flash message
flash('Login successful!', 'success')
return redirect(url_for('dashboard'))

# Conditional redirect
if 'user' not in session:
    flash('Please login first!', 'warning')
    return redirect(url_for('login'))

# Post-Redirect-Get pattern (prevent duplicate submissions)
@app.route('/contact', methods=['POST'])
def contact():
    # Process form
    flash('Message sent!', 'success')
    return redirect(url_for('contact'))
```

---

## 17. Message Flashing

### What is Covered:
- ✅ Flash messages: `flash()`
- ✅ Message categories (success, danger, warning, info)
- ✅ Display flashed messages in templates
- ✅ Auto-dismiss alerts with JavaScript

### Files:
- `app.py` - flash() calls throughout
- `templates/base.html` - Flash message display
- `static/js/script.js` - Alert auto-dismiss

### Code Example:
```python
from flask import flash

# Flash messages
flash('Welcome back!', 'success')
flash('Invalid credentials!', 'danger')
flash('Please fill all fields!', 'warning')
flash('Here\'s some information.', 'info')

# Redirect with flash
flash('Your message has been sent!', 'success')
return redirect(url_for('contact'))
```

```html
<!-- Display flashed messages -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
                <button onclick="this.parentElement.style.display='none';">&times;</button>
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

```javascript
// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});
```

---

## 18. Error Handling

### What is Covered:
- ✅ Error handlers: `@app.errorhandler()`
- ✅ 404 Not Found
- ✅ 403 Forbidden
- ✅ 500 Server Error
- ✅ Custom error pages
- ✅ Error logging

### Files:
- `app.py` - Error handlers
- `templates/errors/` - Error page templates

### Code Example:
```python
from flask import render_template

# 404 Error Handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

# 403 Error Handler
@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

# 500 Error Handler
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# Handle specific errors in routes
@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = next((p for p in PORTFOLIO_ITEMS if p['id'] == project_id), None)
    if project is None:
        flash('Project not found!', 'danger')
        return redirect(url_for('portfolio'))
    return render_template('project_detail.html', project=project)
```

---

## 19. File Uploading

### What is Covered:
- ✅ File input in HTML
- ✅ Multipart form data
- ✅ File validation
- ✅ Secure filename: `secure_filename()`
- ✅ File saving
- ✅ File download
- ✅ File size limits

### Files:
- `app.py` - resume() and feedback() routes
- `templates/resume.html` - Resume upload
- `templates/feedback.html` - Feedback with attachment

### Code Example:
```python
from werkzeug.utils import secure_filename
import os

# Configuration
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Validation function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# File upload
@app.route('/resume', methods=['POST'])
def resume():
    if 'resume_file' not in request.files:
        flash('No file selected!', 'danger')
        return redirect(url_for('resume'))
    
    file = request.files['resume_file']
    
    if file.filename == '':
        flash('No file selected!', 'danger')
        return redirect(url_for('resume'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        flash('Resume uploaded successfully!', 'success')
        return redirect(url_for('resume'))
    else:
        flash('Invalid file type!', 'danger')
        return redirect(url_for('resume'))

# File download
@app.route('/download/<filename>')
def download(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('resume'))
```

```html
<!-- Template -->
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="resume_file" accept=".pdf,.doc,.docx" required>
    <button type="submit">Upload</button>
</form>
```

---

## 20. Additional Features Implemented

### Decorators
```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

### Context Processors
```python
@app.context_processor
def inject_user():
    return {
        'current_user': session.get('user'),
        'is_logged_in': 'user' in session
    }
```

### Data Management (Session-based)
```python
# Store data in session
contacts = session.get('contacts', [])
contacts.append(contact_data)
session['contacts'] = contacts

# Retrieve from session
contacts = session.get('contacts', [])
```

---

## Summary

This Flask Portfolio Website demonstrates:

✅ **Framework Concepts**
- Flask application structure
- WSGI compliance via Werkzeug
- Jinja2 templating

✅ **Routing**
- Static and dynamic routes
- Variable rules with type converters
- URL building with url_for()
- Redirects and error handling

✅ **HTTP & Requests**
- GET and POST methods
- Form data handling
- File uploads
- Query parameters

✅ **Templates**
- Template inheritance
- Jinja2 syntax (loops, conditionals)
- Static file serving
- Context processors

✅ **User State Management**
- Sessions for user authentication
- Cookies configuration
- Login/Logout functionality
- Protected routes with decorators

✅ **Data Handling**
- Form validation
- Flash messages
- File upload and download
- Session-based data storage

✅ **Error Handling**
- Custom error pages
- Error handlers
- Flash messages for errors

---

**This portfolio website is a comprehensive learning resource for Flask development!**
