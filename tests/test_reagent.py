from datetime import datetime
from turtle import update

from sqlalchemy import select
from sqlalchemy.orm import Session

from logger.model import Reagent, User


class TestOneReagent:
    def test_reagent_creation(self, class_session: Session):
        user = User(full_name="User 1")
        class_session.add(user)
        class_session.commit()

        reagent = Reagent(
            name="Reagent A",
            lot="12345",
            created_by=user.id,
            updated_by=user.id,
        )
        class_session.add(reagent)
        class_session.commit()

        retrieved_reagent = class_session.query(Reagent).filter_by(lot="12345").first()
        assert retrieved_reagent is not None
        assert retrieved_reagent.name == "Reagent A"
        assert retrieved_reagent.lot == "12345"
        assert retrieved_reagent.created_by == user.id
        assert retrieved_reagent.updated_by == user.id
        assert isinstance(retrieved_reagent.created_at, datetime)
        assert isinstance(retrieved_reagent.updated_at, datetime)
        assert retrieved_reagent.created_by_user.full_name == "User 1"
        assert retrieved_reagent.updated_by_user.full_name == "User 1"
        assert retrieved_reagent.processes == []

    def test_reagent_update(self, class_session: Session):
        update_user = User(full_name="User 2")
        class_session.add(update_user)
        class_session.commit()

        create_user = (
            class_session.query(User).filter(User.full_name == "User 1").first()
        )
        assert create_user is not None
        updated_reagent = (
            class_session.query(Reagent)
            .filter(Reagent.id == 1)
            .update({"name": "Reagent B", "lot": "67890", "updated_by": update_user.id})
        )
        class_session.commit()

        updated_reagent: Reagent = (
            class_session.query(Reagent).filter(Reagent.id == 1).first()
        )
        assert isinstance(updated_reagent, Reagent)
        assert updated_reagent.name == "Reagent B"
        assert updated_reagent.lot == "67890"
        assert updated_reagent.created_by == create_user.id
        assert updated_reagent.updated_by == update_user.id
        assert updated_reagent.created_by_user == create_user
        assert updated_reagent.updated_by_user == update_user
        assert updated_reagent.processes == []

    def test_reagent_deletion(self, class_session: Session):
        reagent = class_session.query(Reagent).filter(Reagent.id == 1).first()
        class_session.delete(reagent)
        class_session.commit()

        deleted_reagent = class_session.query(Reagent).filter(Reagent.id == 1).first()
        assert deleted_reagent is None
