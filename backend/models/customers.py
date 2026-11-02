from extensions import db
from datetime import datetime, timedelta

def indian_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

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
        db.Numeric(10, 2),
        default=0.00
    )

    is_deleted = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=indian_time
    )

    updated_at = db.Column(
        db.DateTime,
        default=indian_time,
        onupdate=indian_time
    )

    # add customer name in milk entries 
    milk_entries = db.relationship(
        "MilkEntry",
        backref = "customer",
        lazy = True
    )

    # add customer name in payment entries 
    payment_entries = db.relationship(
        "Payment",
        backref = "customer",
        lazy = True
    )

    # add customer name in bill entries 
    bill_entries = db.relationship(
        "Bill",
        backref = "customer",
        lazy = True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "address": self.address,
            "opening_balance": float(self.opening_balance),
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %I:%M:%S %p")
        }