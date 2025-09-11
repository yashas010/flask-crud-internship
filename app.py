from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_change_in_production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max upload

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    photo = db.Column(db.String(120), nullable=True)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        mobile = request.form['mobile']
        photo = request.files['photo']
        
        # validations (simplified since frontend now handles validation)
        if not name or not dob or not email or not mobile:
            flash('All fields are required', 'error')
            return render_template('index.html')
        if not mobile or len(mobile) < 10:
            flash('Invalid mobile number format', 'error')
            return render_template('index.html')
        if '@' not in email or '.' not in email:
            flash('Invalid email format', 'error')
            return render_template('index.html')
            
        # Check for duplicate email
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered', 'error')
            return render_template('index.html')
            
        # Check for duplicate mobile
        existing_mobile = User.query.filter_by(mobile=mobile).first()
        if existing_mobile:
            flash('Mobile number already registered', 'error')
            return render_template('index.html')
            
        filename = None
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = User(name=name, dob=dob, email=email, mobile=mobile, photo=filename)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('index.html')

@app.route('/users')
def users():
    search = request.args.get('search', '')
    if search:
        users = User.query.filter(User.name.contains(search)).all()
    else:
        users = User.query.all()
    return render_template('users.html', users=users, search=search)

@app.route('/api/search')
def search_users():
    search = request.args.get('q', '')
    if search:
        users = User.query.filter(User.name.contains(search)).all()
    else:
        users = User.query.all()
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'name': user.name,
            'dob': user.dob,
            'email': user.email,
            'mobile': user.mobile,
            'photo': user.photo
        })
    return jsonify(users_data)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        mobile = request.form['mobile']
        photo = request.files['photo']
        
        # Validations
        if not name or not dob or not email or not mobile:
            flash('All fields are required', 'error')
            return redirect(url_for('edit', id=id))
        if not mobile or len(mobile) < 10:
            flash('Invalid mobile number format', 'error')
            return redirect(url_for('edit', id=id))
        if '@' not in email or '.' not in email:
            flash('Invalid email format', 'error')
            return redirect(url_for('edit', id=id))
            
        # Check for duplicate email (excluding current user)
        existing_email = User.query.filter(User.email == email, User.id != id).first()
        if existing_email:
            flash('Email already registered', 'error')
            return redirect(url_for('edit', id=id))
            
        # Check for duplicate mobile (excluding current user)
        existing_mobile = User.query.filter(User.mobile == mobile, User.id != id).first()
        if existing_mobile:
            flash('Mobile number already registered', 'error')
            return redirect(url_for('edit', id=id))
        
        user.name = name
        user.dob = dob
        user.email = email
        user.mobile = mobile
        
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.photo = filename
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)
    if user.photo:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.photo))
        except Exception:
            pass
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    app.run(debug=True)
