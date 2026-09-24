from datetime import datetime, timezone
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SearchLog(Base):
    __tablename__ = "search_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=True)
    company_name: Mapped[str] = mapped_column(String(500), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    pain_points: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string
    generated_pitch: Mapped[str] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = relationship("User", back_populates="search_logs")

    def __repr__(self):
        return f"<SearchLog(id={self.id}, url={self.target_url})>"
