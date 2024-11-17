from datetime import datetime
from typing import Literal, Optional

from sqlalchemy import Date, DateTime, ForeignKey, create_engine, event, func, update
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


engine = create_engine(
    "sqlite:///:memory:",
)


class Base(DeclarativeBase):
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            # skip _sa_instance_state
            f"({','.join(f'{k}={v}' for k, v in self.__dict__.items() if k != "_sa_instance_state")})"
        )


class User(Base):
    """
    User model representing a user in the system.

    Attributes:
        id (int): Primary key of the user.
        created_at (datetime): Timestamp when the user was created and last updated.
        full_name (str): Full name of the user, must be unique.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    full_name: Mapped[str] = mapped_column(unique=True)


class Reagent(Base):
    """
    Reagent model representing a reagent entity in the database.

    Attributes:
        id (int): Primary key of the reagent.
        name (str): Name of the reagent.
        lot (str): Unique lot number of the reagent.
        created_at (datetime): Timestamp when the reagent was created.
        created_by (int): ID of the user who created the reagent.
        created_by_user (User): User object representing the creator of the reagent.
        updated_at (datetime): Timestamp when the reagent was last updated.
        updated_by (int): ID of the user who last updated the reagent.
        processes (list[Process] | None): List of processes associated with the reagent.
    """

    __tablename__ = "reagents"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    lot: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by_user: Mapped[User] = relationship("User", foreign_keys=[created_by])
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    updated_by_user: Mapped[User] = relationship("User", foreign_keys=[updated_by])
    processes: Mapped[Optional[list["Process"]]] = relationship(
        secondary="reagent_process_association", back_populates="reagents"
    )


class Process(Base):
    """
    Represents a process in the system.

    Attributes:
        id (int): Primary key of the process.
        name (str): Name of the process.
        reagent_id (int): Foreign key referencing the reagent associated with the process.
        created_by (int): Foreign key referencing the user who created the process.
        created_by_user (User): Relationship to the User who created the process.
        created_at (datetime): Timestamp when the process was created.
        updated_at (datetime): Timestamp when the process was last updated.
        updated_by (int): Foreign key referencing the user who last updated the process.
        updated_by_user (User): Relationship to the User who last updated the process.
        process_type (Literal["pre", "post"]): Type of the process, either 'pre' or 'post'.
    """

    __tablename__ = "processes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by_user: Mapped[User] = relationship("User", foreign_keys=[created_by])
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    updated_by_user: Mapped[User] = relationship("User", foreign_keys=[updated_by])
    process_type: Mapped[Literal["pre", "post"]]
    reagents: Mapped[Optional[list[Reagent]]] = relationship(
        secondary="reagent_process_association", back_populates="processes"
    )


class ReagentProcessAssociation(Base):
    """
    Represents the association between a reagent and a process.

    Attributes:
        reagent_id (int): Foreign key referencing the reagent.
        process_id (int): Foreign key referencing the process.
    """

    __tablename__ = "reagent_process_association"
    reagent_id: Mapped[int] = mapped_column(ForeignKey("reagents.id"), primary_key=True)
    process_id: Mapped[int] = mapped_column(
        ForeignKey("processes.id"), primary_key=True
    )
