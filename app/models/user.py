import uuid
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key= True,
        default= uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(30),
        unique= True,
        nullable= False
    )

    password: Mapped[str] = mapped_column(
        String(500),
        nullable= False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone= True),
        server_default= func.now(),
        nullable= False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone= True),
        server_default= func.now(),
        onupdate= func.now(),
        nullable= False
    )