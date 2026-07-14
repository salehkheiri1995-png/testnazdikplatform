"""مدل علاقه‌مندی‌ها (Favorite/Bookmark)."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Favorite(Base, TimestampMixin):
    """جدول علاقه‌مندی‌ها (نشانک‌ها)."""

    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # نوع مورد علاقه‌مندی
    entity_type: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, comment="provider, store, service, product"
    )
    entity_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, comment="ID مورد علاقه‌مندی"
    )
    
    # Relations
    user: Mapped["User"] = relationship("User", back_populates="favorites")

    def __repr__(self) -> str:
        return f"<Favorite user_id={self.user_id} {self.entity_type}:{self.entity_id}>"
