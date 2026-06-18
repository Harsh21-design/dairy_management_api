from extensions import db
from datetime import datetime, timedelta

def indian_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class Payment(db.Model):

    __tablename__ = "payments"

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

    payment_date = db.Column(
        db.Date,
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
        default=indian_time

    )

    updated_at = db.Column(
        db.DateTime,
        default=indian_time,
        onupdate=indian_time
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id":self.customer_id,
            "customer_name":self.customer.name,
            "product_id":self.product_id,
            "product": self.product.name,

            "payment_date":self.payment_date.strftime("%Y-%m-%d"),
            "amount": float(self.amount),
            "is_deleted": self.is_deleted,
            
            "created_at": self.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %I:%M:%S %p")
        }