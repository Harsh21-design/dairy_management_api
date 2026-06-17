from extensions import db
from datetime import datetime

class MilkEntry(db.Model):

    __tablename__ = "milk_entries"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    entry_date = db.Column(
        db.Date,
        nullable=False
    )

    morning_qty = db.Column(
        db.Numeric(10,2),
        default=0.00
    )

    evening_qty = db.Column(
        db.Numeric(10,2),
        default=0.00
    )

    total_qty = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    rate = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    is_deleted = db.Column(
        db.Boolean,
        default=False
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
            "customer_id":self.customer_id,
            "customer_name":self.customer.name,
            "product_id":self.product_id,
            "product": self.product.name,

            "entry_date":self.entry_date.strftime("%Y-%m-%d"),
            "morning_qty": float(self.morning_qty),
            "evening_qty": float(self.evening_qty),

            "total_qty": float(self.total_qty),
            "rate": float(self.rate),
            "amount": float(self.amount),

            "is_deleted": self.is_deleted,

            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    