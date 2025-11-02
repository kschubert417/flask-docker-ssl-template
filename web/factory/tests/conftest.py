# tests/conftest.py
import pytest
from datetime import date
from app import create_app, db
from app.config import TestConfig
from app.models import User, Messages


# -----------------------------------------------------------------------------
# App + Database Setup
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for the test session."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Provide a test client for sending HTTP requests."""
    return app.test_client()


@pytest.fixture(scope="function")
def session(app):
    """Provide a clean database session per test."""
    with app.app_context():
        yield db.session
        db.session.rollback()
        db.session.close()

@pytest.fixture(scope="function")
def authenticated_admin_client(client, sample_admin_user):
    """Provide a client authenticated as admin user."""
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpassword',
        'remember_me': False
    })
    return client

# -----------------------------------------------------------------------------
# Common Test Data
# -----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def sample_admin_user(session):
    """Create a sample admin user for authentication tests."""
    user = User(
        email="test@example.com",
        first_name="FName",
        last_name="LName",
        role="admin",
    )
    user.set_password("testpassword")
    session.add(user)
    session.commit()
    return user


@pytest.fixture(scope="function")
def sample_message(session):
    """Create a sample message record."""
    msg = Messages(
        first_name="John",
        last_name="Doe",
        company="Kaliber Solutions",
        email="john.doe@example.com",
        message="Interested in your services.",
        date=date(2025, 10, 25),
    )
    session.add(msg)
    session.commit()
    return msg
