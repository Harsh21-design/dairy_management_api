from extensions import db

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    unit = db.Column(
        db.String(20),
        nullable=False
        )

    rate = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    is_deleted = db.Column(
        db.Boolean,
        default=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "rate": float(self.rate),
            "is_deleted": self.is_deleted
        }