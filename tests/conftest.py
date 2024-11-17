from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from logger.model import Base


@pytest.fixture(scope="class")
def class_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        db = Session(engine)
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()


@pytest.fixture(scope="function")
def func_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        db = Session(engine)
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()
