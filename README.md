# Flask Portfolio Website

A comprehensive, fully-featured portfolio website built with Flask, demonstrating all core Flask concepts and best practices.

## Features

### 🎯 Core Flask Concepts Implemented

#### 1. **Framework & Components**
- WSGI-compatible Flask application
- Werkzeug for request/response handling
- Jinja2 templating engine
- URL routing and variable rules

#### 2. **Routing & URL Building**
- Static routes (Home, About, Portfolio, etc.)
- Dynamic routes with variable rules (`/project/<int:project_id>`)
- URL building with `url_for()`
- RESTful routing patterns

#### 3. **HTTP Methods**
- GET requests for displaying pages
- POST requests for form submissions
- Form data handling
- File upload handling

#### 4. **Templates**
- Base template inheritance
- Template variables and loops
- Conditional rendering
- Context processors
- Flash message integration

#### 5. **Static Files**
- CSS stylesheets
- JavaScript files
- Image assets
- Proper static file serving

#### 6. **Request Object**
- Form data retrieval with `request.form`
- File uploads with `request.files`
- Query parameters with `request.args`
- Request methods and attributes

#### 7. **Forms & Data Handling**
- Contact form with validation
- Resume upload
- Feedback submission
- Form data processing

#### 8. **Cookies & Sessions**
- Session management
- User authentication
- Session persistence
- Login/Logout functionality
- Remember me functionality

#### 9. **Redirects & Error Handling**
- Redirect after form submission
- Login redirects
- Error pages (404, 403, 500)
- Error handlers
- Message flashing

#### 10. **File Uploading**
- Resume upload
- File type validation
- Secure filename handling
- File download functionality
- File size limits

## Pages & Functionality

### 📄 Pages Included

1. **Home** (`/`) - Landing page with featured projects
2. **About** (`/about`) - Professional profile and experience
3. **Portfolio** (`/portfolio`) - Complete project showcase
4. **Project Detail** (`/project/<id>`) - Individual project details
5. **Skills** (`/skills`) - Technical expertise and proficiencies
6. **Services** (`/services`) - Services offered with pricing
7. **Contact** (`/contact`) - Contact form and information
8. **Resume** (`/resume`) - Resume upload and display
9. **Feedback** (`/feedback`) - Feedback and testimonials
10. **Login** (`/login`) - User authentication
11. **Dashboard** (`/dashboard`) - User dashboard (requires login)
12. **Error Pages** - 404, 403, 500 error pages

### 🔐 Authentication & Authorization

- Login system with session management
- Protected routes using decorators
- Remember me functionality
- Logout functionality
- Demo credentials provided

### 📥 Form Handling

- Contact form with email, phone, subject, message
- Resume upload with file validation
- Feedback form with attachments
- Form validation and error messages
- Flash messages for user feedback

### 💾 Data Storage

- Session-based storage for demo purposes
- Contact message tracking
- File upload management
- User authentication

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
flask/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html              # Base template (layout)
│   ├── index.html             # Home page
│   ├── about.html             # About page
│   ├── portfolio.html         # Portfolio page
│   ├── project_detail.html    # Project details
│   ├── skills.html            # Skills page
│   ├── services.html          # Services page
│   ├── contact.html           # Contact page
│   ├── login.html             # Login page
│   ├── dashboard.html         # Dashboard (protected)
│   ├── resume.html            # Resume page
│   ├── feedback.html          # Feedback page
│   └── errors/
│       ├── 404.html           # Page not found
│       ├── 403.html           # Access forbidden
│       └── 500.html           # Server error
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── script.js          # JavaScript utilities
│   └── images/                # Image assets
└── uploads/                   # File uploads directory
```

## Usage

### Demo Credentials

- **Username:** `admin`
- **Password:** `password123`

Use these credentials to log in and access the dashboard.

### Key Features

#### 1. **Navigation**
- Sticky navigation bar
- Quick access to all pages
- Login/Logout functionality

#### 2. **Contact Form**
- Name, email, phone, subject, message fields
- Form validation
- Success flash messages
- Message storage in session

#### 3. **Resume Upload**
- Upload your resume (PDF, DOC, DOCX, TXT, PNG, JPG, GIF)
- Download uploaded files
- File size validation (max 16MB)

#### 4. **Project Portfolio**
- Display multiple projects
- Filter projects by category
- View detailed project information
- Technologies used for each project

#### 5. **Skills & Services**
- Organize skills by category
- Display proficiency levels
- Show certifications
- List services with pricing plans

#### 6. **Feedback System**
- Submit feedback with rating
- Optional file attachments
- View testimonials
- Session-based storage

#### 7. **Dashboard** (Protected)
- View website statistics
- Monitor received messages
- User session information

## Flask Concepts Demonstration

### 1. **Routing**
```python
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', projects=PORTFOLIO_ITEMS)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    # Variable rules example
    project = next((p for p in PORTFOLIO_ITEMS if p['id'] == project_id), None)
    return render_template('project_detail.html', project=project)
```

### 2. **Form Handling & Request Object**
```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        # Process form data
        return redirect(url_for('contact'))
    return render_template('contact.html')
```

### 3. **File Upload**
```python
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        file = request.files['resume_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('resume'))
    return render_template('resume.html')
```

### 4. **Sessions & Cookies**
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password == 'password123':
            session['user'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')
```

### 5. **Error Handling**
```python
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
```

### 6. **Context Processors**
```python
@app.context_processor
def inject_user():
    return {
        'current_user': session.get('user'),
        'is_logged_in': 'user' in session
    }
```

### 7. **Decorators**
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

## Configuration

### Environment Variables
```python
app.secret_key = 'your_secret_key_here_change_in_production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'}
```

## Security Notes

⚠️ **Important:** This is a demo application. For production use:

1. Change the secret key to a strong, random value
2. Use environment variables for sensitive configuration
3. Implement proper database for data persistence
4. Use proper authentication library (e.g., Flask-Login)
5. Implement CSRF protection (Flask-WTF)
6. Add rate limiting
7. Use HTTPS
8. Validate and sanitize all user inputs
9. Implement proper password hashing
10. Add logging and monitoring

## Styling & UI

- **Responsive Design:** Mobile-friendly layout
- **Modern CSS:** Grid, flexbox, gradients
- **Smooth Animations:** Page transitions and hover effects
- **Color Scheme:** Professional blue and gray palette
- **Typography:** Clear hierarchy and readable fonts
- **Accessibility:** Semantic HTML and ARIA attributes

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Customization

### Change Portfolio Items

Edit the `PORTFOLIO_ITEMS` list in `app.py`:

```python
PORTFOLIO_ITEMS = [
    {
        'id': 1,
        'title': 'Your Project Title',
        'description': 'Project description',
        'image': 'image.jpg',
        'technologies': ['Tech1', 'Tech2']
    }
]
```

### Add New Pages

1. Create a new template in `templates/`
2. Add a route in `app.py`
3. Add navigation link in `base.html`

### Customize Styling

Edit `static/css/style.css` to change colors, fonts, and layout.

## Technologies Used

- **Backend:** Flask, Werkzeug, Jinja2
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Storage:** Session-based (SQLite-compatible for production)
- **File Handling:** Werkzeug secure file handling

## Learning Resources

- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)
- [Python File Handling](https://docs.python.org/3/tutorial/inputoutput.html)

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='localhost', port=5001)
```

### File Upload Issues
- Check file size (max 16MB)
- Verify file type is allowed
- Ensure `uploads/` directory exists
- Check folder permissions

### Session Issues
- Clear browser cookies
- Restart Flask application
- Check secret key configuration

## Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Email notifications
- [ ] Admin panel
- [ ] Search functionality
- [ ] Comment system
- [ ] Rating system
- [ ] API endpoints
- [ ] WebSocket support
- [ ] Payment integration
- [ ] Analytics tracking

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please refer to the Flask documentation or create an issue in the repository.

---

**Happy Coding! 🚀**
