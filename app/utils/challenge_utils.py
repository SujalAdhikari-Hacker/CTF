import logging
import random
import string
from flask import session
from app.models import UserProgress, Challenge
from app.extensions import db

logger = logging.getLogger(__name__)

def get_user_progress(user):
    """Get the progress of a user on all challenges"""
    progress_data = UserProgress.query.filter_by(user_id=user.id).all()
    completed_challenges = [p.challenge_id for p in progress_data if p.is_completed]
    
    # Get all challenges and sort by order
    challenges = Challenge.query.order_by(Challenge.order).all()
    
    progress = []
    for challenge in challenges:
        # Check if user is allowed to access this challenge
        is_accessible = True
        if challenge.order > 1:
            # Check if previous challenge is completed
            prev_challenge = Challenge.query.filter_by(order=challenge.order-1).first()
            if prev_challenge and prev_challenge.id not in completed_challenges:
                is_accessible = False
        
        # Find user progress for this challenge
        user_progress = next((p for p in progress_data if p.challenge_id == challenge.id), None)
        
        progress.append({
            'id': challenge.id,
            'name': challenge.name,
            'description': challenge.description,
            'category': challenge.category,
            'difficulty': challenge.difficulty,
            'is_completed': challenge.id in completed_challenges,
            'is_accessible': is_accessible,
            'attempts': user_progress.attempts if user_progress else 0
        })
    
    return progress

def mark_challenge_complete(user_id, challenge_id):
    """Mark a challenge as completed for a user"""
    progress = UserProgress.query.filter_by(
        user_id=user_id, 
        challenge_id=challenge_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            challenge_id=challenge_id
        )
        db.session.add(progress)
    
    progress.is_completed = True
    db.session.commit()
    
    logger.info(f"User {user_id} completed challenge {challenge_id}")
    return True

def increment_attempt(user_id, challenge_id):
    """Increment the attempt counter for a challenge"""
    progress = UserProgress.query.filter_by(
        user_id=user_id, 
        challenge_id=challenge_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            challenge_id=challenge_id,
            attempts=1
        )
        db.session.add(progress)
    else:
        progress.attempts += 1
    
    db.session.commit()
    
    logger.info(f"User {user_id} made attempt {progress.attempts} on challenge {challenge_id}")
    return progress.attempts

def generate_random_string(length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def is_challenge_accessible(user, challenge_id):
    """Check if a challenge is accessible to the user"""
    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return False
    
    # First challenge is always accessible
    if challenge.order == 1:
        return True
    
    # Check if previous challenges are completed
    progress = get_user_progress(user)
    for p in progress:
        if p['id'] == challenge_id:
            return p['is_accessible']
    
    return False