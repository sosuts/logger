from sqlalchemy import select
from sqlalchemy.orm import Session

from logger.model import User


class TestOneUser:
    def test_create_one(self, class_session):
        user = User(
            full_name="Test User",
        )
        class_session.add(user)
        class_session.commit()
        assert user.id == 1

    def test_update_one(self, class_session: Session):
        stmt = select(User).filter_by(full_name="Test User")
        user = class_session.scalars(stmt).one()
        user.full_name = "Update"
        assert user in class_session.dirty
        class_session.commit()

    def test_delete_one(self, class_session: Session):
        stmt = select(User).filter_by(full_name="Update")
        user = class_session.scalars(stmt).one()
        class_session.delete(user)
        class_session.commit()
        assert user not in class_session


class TestManyUser:
    def test_create_many(self, class_session: Session):
        users = [
            User(full_name="User 1"),
            User(full_name="User 2"),
            User(full_name="User 3"),
        ]
        class_session.add_all(users)
        class_session.commit()
        assert len(users) == 3

    def test_update_many(self, class_session: Session):
        stmt = select(User).filter(User.full_name.like("User%"))
        users = class_session.scalars(stmt).all()
        for i, user in enumerate(users):
            user.full_name = f"Update {i}"
        assert all(user in class_session.dirty for user in users)
        class_session.commit()
        stmt = select(User)
        users = class_session.scalars(stmt).all()
        assert [user.full_name for user in users] == [
            "Update 0",
            "Update 1",
            "Update 2",
        ]

    def test_delete_many(self, class_session: Session):
        stmt = select(User).filter(User.full_name.like("Update%"))
        users = class_session.scalars(stmt).all()
        assert len(users) == 3
        for user in users:
            class_session.delete(user)
        class_session.commit()
        # check if users are deleted and no users left
        stmt = select(User)
        users = class_session.scalars(stmt).all()
        assert len(users) == 0
