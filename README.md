# Flask CRUD Internship App - Deployment Ready

A modern CRUD web application built with Flask for internship demonstration.

## Features
- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ Advanced form validation with real-time feedback
- ✅ Country code phone number support
- ✅ Photo upload with preview
- ✅ Real-time search functionality
- ✅ Professional UI with gradients and animations
- ✅ Mobile responsive design
- ✅ SQLite database

## Tech Stack
- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **Deployment**: Render.com

## Local Development

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   python app.py
   ```
   Open http://localhost:5000

## Deployment on Render

This app is configured for easy deployment on Render.com:

1. Push code to GitHub
2. Connect GitHub repo to Render
3. Deploy automatically

## Live Demo
🔗 **[Live App URL]** - (Update this after deployment)

## Project Structure
```
├── app.py              # Main Flask application
├── wsgi.py             # WSGI entry point for production
├── requirements.txt    # Python dependencies
├── Procfile           # Process file for deployment
├── templates/         # HTML templates
├── static/           # CSS, JS, and uploaded files
└── README.md         # This file
```

## Form Fields & Validation
- **Name**: Required, text input
- **Email**: Required, email format validation with real-time feedback
- **Date of Birth**: Required, date picker
- **Mobile**: Required, country code + number with smart validation
- **Photo**: Optional, image upload with preview

## API Endpoints
- `GET /` - Home page with add user form
- `GET /users` - View all users with search
- `GET /api/search?q=term` - Real-time search API
- `POST /` - Create new user
- `GET /edit/<id>` - Edit user form  
- `POST /edit/<id>` - Update user
- `GET /delete/<id>` - Delete user

---
**Built for Internship Assignment**  
Demonstrates full-stack development skills with modern web technologies.
