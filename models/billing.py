import calendar
from extensions import db
from datetime import datetime, timedelta

def indian_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class Bill(db.Model):

    __tablename__ = "bills"

    id = db.Column(db.Integer, primary_key=True)
    
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    # total_payment = db.Column(
    #     db.Numeric(10,2),
    #     nullable=False
    # )

    # current_due = db.Column(
    #     db.Numeric(10,2),
    #     nullable=False
    # )

    bill_month = db.Column(
        db.Integer,
        nullable=False
    )

    bill_year = db.Column(
        db.Integer,
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

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id":self.customer_id,
            "customer_name":self.customer.name,
            "bill_month": calendar.month_name[self.bill_month],
            "bill_year": self.bill_year,
            "total_amount": self.total_amount,
            # "total_payment": self.total_payment,
            # "current_due": self.current_due,
            "is_deleted": self.is_deleted,         
            "created_at": self.created_at.strftime("%Y-%m-%d %I:%M:%S %p")
        }
