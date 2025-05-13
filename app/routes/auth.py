from datetime import datetime
import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app.models import User, LoginAttempt
from app.extensions import db
from app.forms.auth_forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Record login attempt
        login_attempt = LoginAttempt(
            username=form.username.data,
            ip_address=request.remote_addr,
            success=False
        )
        
        if user is None or not user.check_password(form.password.data):
            db.session.add(login_attempt)
            db.session.commit()
            
            flash('Invalid username or password', 'danger')
            logger.warning(f'Failed login attempt for user: {form.username.data}')
            return redirect(url_for('auth.login'))
        
        # Update login attempt to success
        login_attempt.success = True
        db.session.add(login_attempt)
        
        # Update user's last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Login the user
        login_user(user, remember=form.remember_me.data)
        logger.info(f'User logged in: {user.username}')
        
        # Redirect to the requested page or dashboard
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
def logout():
    """Log out the current user"""
    if current_user.is_authenticated:
        logger.info(f'User logged out: {current_user.username}')
        logout_user()
        flash('You have been logged out', 'info')
    
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'New user registered: {user.username}')
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    from app.utils.challenge_utils import get_user_progress
    
    progress = get_user_progress(current_user)
    completed_count = sum(1 for p in progress if p['is_completed'])
    
    return render_template('auth/profile.html', 
                          user=current_user,
                          progress=progress,
                          completed_count=completed_count,
                          total_count=len(progress))