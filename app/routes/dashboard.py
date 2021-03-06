# Import Flask and needed modules
from flask import Blueprint, render_template, session
# Import models
from app.models import Post
from app.db import get_db
# Import decorator function that protects routes.
from app.utils.auth import login_required

# Set up dashboard routes
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Get main dashboard page (protect with login_required).
@bp.route('/')
@login_required
def dash():
  # Connect to db, query all posts from the logged in user.
  db = get_db()
  posts = (
    db.query(Post)
    .filter(Post.user_id == session.get('user_id'))
    .order_by(Post.created_at.desc())
    .all()
  )
  # Render the dashboard page with the retrieved posts and session data.
  return render_template(
    'dashboard.html',
    posts=posts,
    loggedIn=session.get('loggedIn')
  )

# Get single post to edit (protect with login_required).
@bp.route('/edit/<id>')
@login_required
def edit(id):
  # Get post by id.
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  # Render the edit page with the retrieved post.
  return render_template(
    'edit-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )
