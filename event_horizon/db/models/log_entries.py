import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from event_horizon.db.models.base import Base, ModelWithTimeStamp
from event_horizon.db.models.job import Job


class LogEntry(Base, ModelWithTimeStamp):
    __tablename__ = "log_entry"

    log_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job.job_id", ondelete="CASCADE"),
        nullable=False
    )

    message: Mapped[str] = mapped_column(Text, nullable=False)
    job: Mapped[Job] = relationship(back_populates="log_entries")