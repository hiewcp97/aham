from datetime import datetime, date, timezone
import uuid
from app.extensions import db

class Fund(db.Model):
    __tablename__ = 'funds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    fund_name = db.Column(db.String(100), unique=True, nullable=False)
    fund_manager_name = db.Column(db.String(100), nullable=False)
    fund_description = db.Column(db.Text)
    fund_nav = db.Column(db.Numeric(20, 2))
    fund_creation_date = db.Column(db.Date, nullable=False, default=lambda: date.today())
    fund_performance = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
