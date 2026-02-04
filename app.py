import pkgutil
import importlib.util

# Compatibility shim: Python 3.14 removed pkgutil.get_loader; provide a fallback
if not hasattr(pkgutil, 'get_loader'):
    def _compat_get_loader(name):
        try:
            spec = importlib.util.find_spec(name)
            return getattr(spec, 'loader', None) if spec is not None else None
        except Exception:
            return None
    pkgutil.get_loader = _compat_get_loader

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort, Response
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import logging
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
 
# Load environment variables

load_dotenv()   # MUST be before os.getenv

# Read email credentials from environment (strip extra whitespace)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
if isinstance(EMAIL_ADDRESS, str):
    EMAIL_ADDRESS = EMAIL_ADDRESS.strip()
if isinstance(EMAIL_PASSWORD, str):
    EMAIL_PASSWORD = EMAIL_PASSWORD.strip()

# Path for pending contacts fallback storage
PENDING_CONTACTS_FILE = os.path.join(os.path.dirname(__file__), 'pending_contacts.json')


def persist_pending_contact(contact):
    try:
        data = {}
        if os.path.exists(PENDING_CONTACTS_FILE):
            with open(PENDING_CONTACTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f) or {}
    except Exception:
        data = {}

    # Use a timestamp key to avoid collisions
    key = f"{contact.get('email','unknown')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    data[key] = contact
    try:
        with open(PENDING_CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Failed to persist pending contact:', e)

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Debug SMTP route protection key (set in Render as DEBUG_SMTP_KEY)
DEBUG_SMTP_KEY = os.getenv('DEBUG_SMTP_KEY')
 

app = Flask(__name__)

# Configuration - Use environment variables in production
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here_change_in_production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'}

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample portfolio data
PORTFOLIO_ITEMS = [
    {
        'id': 1,
        'title': 'E-Commerce Platform',
        'description': 'A full-stack e-commerce platform with payment integration',
        'image': 'project1.jpg',
        'technologies': ['Python', 'Flask', 'PostgreSQL', 'Stripe']
    },
    {
        'id': 2,
        'title': 'Social Media Dashboard',
        'description': 'Real-time analytics dashboard for social media management',
        'image': 'project2.jpg',
        'technologies': ['React', 'Node.js', 'MongoDB', 'Chart.js']
    },
    {
        'id': 3,
        'title': 'Task Management App',
        'description': 'Collaborative task management application with real-time updates',
        'image': 'project3.jpg',
        'technologies': ['Vue.js', 'Django', 'Redis', 'PostgreSQL']
    }
]

SKILLS = {
    'Backend': ['Python', 'Flask', 'Django', 'Node.js', 'SQL'],
    'Frontend': ['HTML5', 'CSS3', 'JavaScript', 'React', 'Vue.js'],
    'Databases': ['PostgreSQL', 'MongoDB', 'MySQL', 'Redis'],
    'Tools': ['Git', 'Docker', 'Jenkins', 'AWS', 'Linux']
}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page with portfolio overview"""
    visits = session.get('visits', 0)
    visits += 1
    session['visits'] = visits
    
    # Check for flash messages
    message = request.args.get('message', None)
    if message:
        flash(message, 'info')
    
    return render_template('index.html', projects=PORTFOLIO_ITEMS[:3], skills=SKILLS)

@app.route('/about')
def about():
    """About page"""
    user_name = session.get('user', 'Guest')
    return render_template('about.html', user_name=user_name)

@app.route('/portfolio')
def portfolio():
    """Portfolio/Projects page"""
    return render_template('portfolio.html', projects=PORTFOLIO_ITEMS, skills=SKILLS)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Individual project detail page with variable rule"""
    project = next((p for p in PORTFOLIO_ITEMS if p['id'] == project_id), None)
    if project is None:
        flash('Project not found!', 'danger')
        return redirect(url_for('portfolio'))
    return render_template('project_detail.html', project=project)

 
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([name, email, subject, message]):
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('contact'))

        try:
            # Email to YOU
            admin_msg = EmailMessage()
            admin_msg['From'] = EMAIL_ADDRESS
            admin_msg['To'] = EMAIL_ADDRESS
            admin_msg['Subject'] = f"New Contact: {subject}"
            admin_msg.set_content(
                f"""
Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""
            )

            # Auto-reply to USER
            user_msg = EmailMessage()
            user_msg['From'] = EMAIL_ADDRESS
            user_msg['To'] = email
            user_msg['Subject'] = "Thank you for contacting me!"
            user_msg.set_content(
                f"""
Hi {name},

Thank you for contacting me.
I have received your message and will reply shortly.

Best regards,
Sai Kumar
"""
            )

            # Ensure credentials are present
            if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
                raise RuntimeError('Email credentials are not configured (EMAIL_ADDRESS/EMAIL_PASSWORD).')

            # Use STARTTLS on port 587 which is commonly allowed by hosting providers
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(admin_msg)
                smtp.send_message(user_msg)

            flash('Message sent successfully! Check your email.', 'success')

        except Exception as e:
            logging.exception('EMAIL ERROR:')
            # Persist the submission to pending contacts for later delivery
            try:
                contact_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'subject': subject,
                    'message': message,
                    'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                persist_pending_contact(contact_data)
                flash('Error sending email. Your message was saved and will be delivered later.', 'warning')
            except Exception as ex:
                print('Failed to save pending contact:', ex)
                flash('Error sending email. Please try again later.', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/skills')
def skills():
    """Skills page"""
    return render_template('skills.html', skills=SKILLS)

@app.route('/services')
def services():
    """Services page"""
    services_list = [
        {
            'title': 'Web Development',
            'description': 'Full-stack web development with modern frameworks',
            'icon': '💻'
        },
        {
            'title': 'API Development',
            'description': 'RESTful and GraphQL API development',
            'icon': '⚙️'
        },
        {
            'title': 'Database Design',
            'description': 'Database architecture and optimization',
            'icon': '🗄️'
        },
        {
            'title': 'Consulting',
            'description': 'Technical consulting and code review',
            'icon': '📋'
        }
    ]
    return render_template('services.html', services=services_list)



@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user = session.get('user')
    contacts = session.get('contacts', [])
    visits = session.get('visits', 0)
    
    return render_template('dashboard.html', user=user, contacts=contacts, visits=visits)

@app.route('/logout')
def logout():
    """Logout user"""
    user = session.get('user', 'User')
    session.clear()
    flash(f'Goodbye, {user}! You have been logged out.', 'info')
    return redirect(url_for('index', message=f'{user} logged out successfully!'))

@app.route('/resume', methods=['GET', 'POST'])
def resume():
    """Resume upload and download page"""
    if request.method == 'POST':
        # Check if file is in request
        if 'resume_file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(url_for('resume'))
        
        file = request.files['resume_file']
        
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(url_for('resume'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Store in session
            uploaded_files = session.get('uploaded_files', [])
            uploaded_files.append({
                'filename': filename,
                'original_name': request.files['resume_file'].filename,
                'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            session['uploaded_files'] = uploaded_files
            
            flash('Resume uploaded successfully!', 'success')
            return redirect(url_for('resume'))
        else:
            flash('Invalid file type! Allowed types: pdf, txt, doc, docx, png, jpg, jpeg, gif', 'danger')
    
    uploaded_files = session.get('uploaded_files', [])
    return render_template('resume.html', uploaded_files=uploaded_files)

@app.route('/download/<filename>')
def download(filename):
    """Download uploaded file"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found!', 'danger')
            return redirect(url_for('resume'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('resume'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Feedback form with file upload"""
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        rating = request.form.get('rating')
        
        if not feedback_text:
            flash('Please provide feedback!', 'danger')
            return redirect(url_for('feedback'))
        
        feedback_data = {
            'feedback': feedback_text,
            'rating': rating,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Handle optional file upload
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    feedback_data['attachment'] = filename
        
        # Store feedback
        feedbacks = session.get('feedbacks', [])
        feedbacks.append(feedback_data)
        session['feedbacks'] = feedbacks
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
    
    return render_template('feedback.html')

# ==================== Error Handlers ====================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template('errors/403.html'), 403


@app.route('/debug-smtp')
def debug_smtp():
    """Protected server-side SMTP connectivity test.

    Use by visiting: /debug-smtp?key=<DEBUG_SMTP_KEY>
    Returns simple plain-text success/failure so you can verify SMTP from Render.
    """
    # Require the secret key
    key = request.args.get('key')
    if not DEBUG_SMTP_KEY or key != DEBUG_SMTP_KEY:
        abort(403)

    # Check credentials
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        msg = 'Missing EMAIL_ADDRESS or EMAIL_PASSWORD environment variables.'
        logging.error(msg)
        return Response(msg, status=400, mimetype='text/plain')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.quit()
        return Response('SMTP connection and login successful.', mimetype='text/plain')
    except Exception as e:
        logging.exception('Debug SMTP failed')
        return Response(f'Debug SMTP failed: {e}', status=500, mimetype='text/plain')

# ==================== Context Processors ====================

@app.context_processor
def inject_user():
    """Inject user data into all templates"""
    return {
        'current_user': session.get('user'),
        'is_logged_in': 'user' in session
    }

# ==================== Main ====================

if __name__ == '__main__':
    # When running locally use default; in Render the PORT env var is provided and host must be 0.0.0.0
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
