import re
from datetime import datetime

from logger.model import Process, Reagent, User


class TestOneProcess:
    def test_process_creation(self, class_session):
        user = User(full_name="Test User")
        class_session.add(user)
        class_session.commit()

        reagent = Reagent(
            name="Test Reagent", lot="12345", created_by=user.id, updated_by=user.id
        )
        class_session.add(reagent)
        class_session.commit()

        process = Process(
            name="Test Process",
            created_by=user.id,
            updated_by=user.id,
            process_type="pre",
        )
        class_session.add(process)
        class_session.commit()

        assert reagent.processes == []
        reagent.processes.append(process)
        class_session.commit()

        retrieved_process = (
            class_session.query(Process).filter_by(name="Test Process").first()
        )
        assert retrieved_process is not None
        assert retrieved_process.name == "Test Process"
        assert retrieved_process.created_by == user.id
        assert retrieved_process.updated_by == user.id
        assert retrieved_process.process_type == "pre"
        assert len(retrieved_process.reagents) == 1
        assert retrieved_process.reagents[0].name == "Test Reagent"

    def test_process_update(self, class_session):
        user = class_session.query(User).filter_by(id=1).first()
        updated_process = (
            class_session.query(Process)
            .filter(Process.id == 1)
            .update({"name": "Updated Process", "updated_by": user.id})
        )
        class_session.commit()

        updated_process = class_session.query(Process).filter(Process.id == 1).first()
        assert updated_process is not None
        assert updated_process.name == "Updated Process"
        assert updated_process.updated_by == user.id
        assert updated_process.process_type == "pre"
        assert isinstance(updated_process.created_at, datetime)

    def test_process_deletion(self, class_session):
        process = class_session.query(Process).filter_by(id=1).first()
        class_session.delete(process)
        class_session.commit()

        process = class_session.query(Process).filter_by(id=1).first()
        assert process is None
