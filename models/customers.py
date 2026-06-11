from extensions import db
from datetime import datetime

class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    mobile = db.Column(
        db.String(15),
        nullable=False
    )

    address = db.Column(
        db.Text
    )

    opening_balance = db.Column(
        db.Float,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "mobile": self.mobile,
        "address": self.address,
        "opening_balance": self.opening_balance
    }