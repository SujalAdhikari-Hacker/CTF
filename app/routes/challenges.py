import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user

from app.models import Challenge, UserProgress
from app.extensions import db
from app.utils.flag_utils import validate_flag
from app.utils.challenge_utils import get_user_progress, mark_challenge_complete, increment_attempt, is_challenge_accessible

challenges_bp = Blueprint('challenges', __name__)
logger = logging.getLogger(__name__)

@challenges_bp.route('/')
@login_required
def index():
    """List all challenges"""
    progress = get_user_progress(current_user)
    return render_template('challenges/index.html', progress=progress)

@challenges_bp.route('/<int:challenge_id>')
@login_required
def view(challenge_id):
    """View a specific challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    
    # Check if the challenge is accessible
    if not is_challenge_accessible(current_user, challenge_id):
        flash('You need to complete previous challenges first!', 'warning')
        return redirect(url_for('challenges.index'))
    
    # Get user progress
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id
    ).first()
    
    attempts = 0
    completed = False
    if progress:
        attempts = progress.attempts
        completed = progress.is_completed
    
    return render_template(f'challenges/{challenge.id}.html',
                          challenge=challenge,
                          attempts=attempts,
                          completed=completed)

@challenges_bp.route('/submit/<int:challenge_id>', methods=['POST'])
@login_required
def submit(challenge_id):
    """Submit a flag for a challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    
    # Check if the challenge is accessible
    if not is_challenge_accessible(current_user, challenge_id):
        return jsonify({'status': 'error', 'message': 'Challenge not accessible'})
    
    # Get user progress
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id
    ).first()
    
    # Check if already completed
    if progress and progress.is_completed:
        return jsonify({'status': 'success', 'message': 'Challenge already completed'})
    
    # Get the submitted flag
    flag = request.form.get('flag', '').strip()
    
    # Increment attempt counter
    attempts = increment_attempt(current_user.id, challenge_id)
    
    # Validate the flag
    flag_id = f'flag{challenge.order}'
    if validate_flag(flag_id, flag):
        mark_challenge_complete(current_user.id, challenge_id)
        logger.info(f'User {current_user.username} completed challenge {challenge_id}')
        
        # Get next challenge
        next_challenge = Challenge.query.filter_by(order=challenge.order + 1).first()
        
        return jsonify({
            'status': 'success',
            'message': 'Flag is correct! Challenge completed.',
            'next_challenge': next_challenge.id if next_challenge else None
        })
    else:
        logger.info(f'User {current_user.username} failed attempt on challenge {challenge_id}')
        return jsonify({
            'status': 'error',
            'message': 'Incorrect flag. Try again!',
            'attempts': attempts
        })

@challenges_bp.route('/hint/<int:challenge_id>')
@login_required
def hint(challenge_id):
    """Get a hint for a challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    
    # Check if the challenge is accessible
    if not is_challenge_accessible(current_user, challenge_id):
        return jsonify({'status': 'error', 'message': 'Challenge not accessible'})
    
    # Return the hint if available
    if challenge.hint:
        return jsonify({
            'status': 'success',
            'hint': challenge.hint
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No hint available for this challenge'
        })