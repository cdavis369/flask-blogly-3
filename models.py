from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

"""Models for Blogly."""
def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    
class User(db.Model):
  __tablename__ = "users"
  
  id = db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True)
  
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  full_name = f"{first_name} {last_name}"
  image_url = db.Column(db.String(50000), nullable=True)
  
  def __repr__(self):
    u = self
    return f"<User id={u.id} first={u.first_name} last={u.last_name} pic={u.image_url}"
  
  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"
  
  