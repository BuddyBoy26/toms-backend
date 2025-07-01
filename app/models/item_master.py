from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ItemMaster(Base):
    __tablename__ = "item_master"

    item_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("product_master.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_description = Column(Text, nullable=False)
    hs_code = Column(String(20), nullable=False, index=True)

    product = relationship("ProductMaster", back_populates="items")
    order_items = relationship(
        "OrderItemDetail",
        back_populates="item_master",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<ItemMaster("
            f"item_id={self.item_id!r}, "
            f"product_id={self.product_id!r}, "
            f"item_description={self.item_description!r}, "
            f"hs_code={self.hs_code!r})>"
        )
