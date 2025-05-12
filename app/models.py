from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    # MPESA and Budget Settings
    transfer_time = db.Column(db.Time, default=datetime.strptime('06:00', '%H:%M').time())
    monthly_limit = db.Column(db.Float, default=0.0)
    daily_limit = db.Column(db.Float, default=0.0)
    budget_lock_date = db.Column(db.DateTime, nullable=True)  # When the budget was last set
    next_budget_date = db.Column(db.DateTime, nullable=True)  # When budget can be modified again
    two_factor_enabled = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can_modify_budget(self):
        """Check if user can modify their budget"""
        if not self.next_budget_date:
            return True
        return datetime.utcnow() >= self.next_budget_date

    def set_budget(self, monthly_limit, daily_limit):
        """Set budget and lock it until next month"""
        if not self.can_modify_budget():
            return False, "Budget cannot be modified until next month"
        
        now = datetime.utcnow()
        next_month = datetime(now.year + (now.month == 12), 
                            (now.month % 12) + 1, 
                            1)  # First day of next month
        
        self.monthly_limit = monthly_limit
        self.daily_limit = daily_limit
        self.budget_lock_date = now
        self.next_budget_date = next_month
        return True, "Budget set successfully"
        
    def __repr__(self):
        return f'<User {self.phone_number}>'

class BudgetCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    daily_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with User
    user = db.relationship('User', backref=db.backref('budget_categories', lazy=True))

    def __repr__(self):
        return f'<BudgetCategory {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('budget_category.id'))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'credit' or 'debit'
    description = db.Column(db.String(256))
    mpesa_reference = db.Column(db.String(64), unique=True, nullable=True)  # Allow null for non-MPESA transactions
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    category = db.relationship('BudgetCategory', backref=db.backref('transactions', lazy=True))