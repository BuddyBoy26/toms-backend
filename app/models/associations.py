from sqlalchemy import Column, Integer, ForeignKey, Table
from ..database import Base

# Association (junction) table for many-to-many relationship
company_product = Table(
    "company_product",
    Base.metadata,
    Column(
        "company_id",
        Integer,
        ForeignKey("company_master.company_id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("product_master.product_id", ondelete="CASCADE"),
        primary_key=True
    )
)
