from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the index page"""
    return render_template('index.html', 
                          club_name=current_app.config['CLUB_NAME'],
                          author_name=current_app.config['AUTHOR_NAME'],
                          discord_link=current_app.config['DISCORD_LINK'])

@main_bp.route('/scoreboard')
def scoreboard():
    """Render the scoreboard page"""
    from app.models import User, UserProgress
    
    # Get users and their progress
    users = User.query.all()
    
    scoreboard_data = []
    for user in users:
        completed_challenges = UserProgress.query.filter_by(
            user_id=user.id, 
            is_completed=True
        ).count()
        
        scoreboard_data.append({
            'username': user.username,
            'completed_challenges': completed_challenges,
            'last_login': user.last_login
        })
    
    # Sort by number of completed challenges (descending)
    scoreboard_data.sort(key=lambda x: x['completed_challenges'], reverse=True)
    
    return render_template('scoreboard.html', 
                          scoreboard=scoreboard_data)

@main_bp.route('/dashboard')
def dashboard():
    """Render the dashboard page or redirect to login"""
    if current_user.is_authenticated:
        from app.utils.challenge_utils import get_user_progress
        
        progress = get_user_progress(current_user)
        completed_count = sum(1 for p in progress if p['is_completed'])
        
        return render_template('dashboard.html', 
                              progress=progress,
                              completed_count=completed_count,
                              total_count=len(progress))
    else:
        return redirect(url_for('auth.login'))

@main_bp.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html',
                          club_name=current_app.config['CLUB_NAME'],
                          author_name=current_app.config['AUTHOR_NAME'],
                          discord_link=current_app.config['DISCORD_LINK'])