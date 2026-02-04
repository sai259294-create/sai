# Flask Portfolio Website - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://localhost:5000`

---

## 🔓 Login Details
- **Username:** `admin`
- **Password:** `password123`

---

## 📚 What You'll Learn

### Flask Fundamentals
✅ **Routing** - Map URLs to functions
✅ **Templates** - Use Jinja2 for dynamic HTML
✅ **Static Files** - Serve CSS, JS, images
✅ **Forms** - Handle POST requests & validation

### Advanced Features
✅ **Sessions** - User authentication & state
✅ **File Upload** - Upload and manage files
✅ **Error Handling** - Custom 404, 500 pages
✅ **Redirects** - URL redirection & flashing

### Request Handling
✅ **Request Object** - Get form data & files
✅ **HTTP Methods** - GET, POST methods
✅ **Cookies** - Store client-side data
✅ **Variable Routes** - Dynamic URL parameters

---

## 📁 Project Structure

```
flask/
├── app.py                 ← Main application
├── config.py             ← Configuration
├── requirements.txt      ← Dependencies
├── README.md             ← Full documentation
│
├── templates/            ← HTML files
│   ├── base.html        ← Layout template
│   ├── index.html       ← Home page
│   ├── about.html       ← About page
│   ├── portfolio.html   ← Projects showcase
│   ├── contact.html     ← Contact form
│   ├── login.html       ← Login page
│   ├── dashboard.html   ← User dashboard
│   ├── resume.html      ← Resume upload/download
│   ├── feedback.html    ← Feedback form
│   ├── skills.html      ← Skills showcase
│   ├── services.html    ← Services page
│   ├── project_detail.html
│   └── errors/          ← Error pages
│       ├── 404.html
│       ├── 403.html
│       └── 500.html
│
├── static/              ← Static files
│   ├── css/
│   │   └── style.css   ← All styling
│   ├── js/
│   │   └── script.js   ← JavaScript utilities
│   └── images/         ← Image assets
│
└── uploads/            ← Uploaded files storage
```

---

## 🔥 Key Features Implemented

### 1. **Routing** 
Different URL routes for each page:
- `/` - Home
- `/portfolio` - Projects
- `/project/1` - Single project details (variable rule)
- `/contact` - Contact form
- `/login` - Authentication
- `/dashboard` - Protected page

### 2. **Templates**
- Base template inheritance
- Template variables: `{{ variable }}`
- Loops: `{% for item in items %}`
- Conditionals: `{% if condition %}`
- URL generation: `{{ url_for('function_name') }}`

### 3. **Forms & Request Handling**
```python
# Get form data
name = request.form.get('name')

# Get file uploads
file = request.files['resume_file']

# Redirect after form submission
return redirect(url_for('contact'))
```

### 4. **Sessions & Cookies**
```python
# Store user in session
session['user'] = username

# Check if logged in
if 'user' in session:
    current_user = session['user']

# Clear session (logout)
session.clear()
```

### 5. **File Upload**
```python
from werkzeug.utils import secure_filename

# Validate file type
if allowed_file(filename):
    filename = secure_filename(filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

### 6. **Error Handling**
```python
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
```

### 7. **Flash Messages**
```python
flash('Welcome back!', 'success')
return redirect(url_for('home'))

# In template:
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

---

## 🎨 Available Pages

| Page | URL | Features |
|------|-----|----------|
| Home | `/` | Hero section, featured projects |
| About | `/about` | Bio, experience timeline |
| Portfolio | `/portfolio` | All projects, filtering |
| Project Detail | `/project/1` | Individual project info |
| Skills | `/skills` | Tech stack, certifications |
| Services | `/services` | Services offered, pricing |
| Contact | `/contact` | Contact form, information |
| Resume | `/resume` | Upload/download resume |
| Feedback | `/feedback` | Feedback form, testimonials |
| Login | `/login` | Authentication |
| Dashboard | `/dashboard` | Messages, statistics (protected) |

---

## 💡 Code Examples

### Example 1: Simple Route
```python
@app.route('/about')
def about():
    user_name = session.get('user', 'Guest')
    return render_template('about.html', user_name=user_name)
```

### Example 2: Variable Route
```python
@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = next((p for p in PORTFOLIO_ITEMS if p['id'] == project_id), None)
    return render_template('project_detail.html', project=project)
```

### Example 3: Form Handling
```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Process form data
        flash(f'Thanks {name}!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')
```

### Example 4: Protected Route
```python
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

---

## 🔧 Customization

### Change Site Title
Edit in `base.html`:
```html
<title>{% block title %}My Portfolio{% endblock %}</title>
```

### Add New Project
Edit `app.py` - `PORTFOLIO_ITEMS` list:
```python
PORTFOLIO_ITEMS = [
    {
        'id': 4,
        'title': 'New Project',
        'description': 'Description here',
        'image': 'image.jpg',
        'technologies': ['Python', 'Flask']
    }
]
```

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #2563eb;  /* Change this */
    --secondary-color: #64748b;
    /* ... */
}
```

---

## 🚀 Deployment Ready

To deploy to production:

1. **Change SECRET_KEY** in `app.py`
```python
app.secret_key = 'your-secure-random-key-here'
```

2. **Use Production Config**
```python
from config import ProductionConfig
app.config.from_object(ProductionConfig)
```

3. **Run with WSGI Server**
```bash
pip install gunicorn
gunicorn app:app
```

4. **Enable HTTPS** and set:
```python
SESSION_COOKIE_SECURE = True
```

---

## 📞 Support

### Troubleshooting

**Port Already in Use?**
```bash
python app.py
# Change port in app.py: app.run(port=5001)
```

**Module Not Found?**
```bash
pip install Flask==2.3.2
```

**Can't Upload Files?**
- Check `uploads/` folder exists
- Verify file size < 16MB
- Check file type is allowed

---

## 🎓 Learning Path

1. **Start Here:** Understand routing in `app.py`
2. **Templates:** Explore `templates/` folder
3. **Styling:** Check `static/css/style.css`
4. **Features:** Add new routes and templates
5. **Databases:** Upgrade from session to SQLite
6. **Security:** Add proper authentication

---

## 📖 Resources

- [Flask Docs](https://flask.palletsprojects.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [Werkzeug](https://werkzeug.palletsprojects.com/)
- [Python Docs](https://docs.python.org/3/)

---

**Ready to build? Start with `python app.py` 🚀**
