from datetime import date
from app.models import Messages

def test_create_new_message(sample_message):
    """
    GIVEN a Message model
    WHEN a new Message is created
    THEN check the fields are defined correctly
    """
    assert sample_message.id is not None
    assert sample_message.first_name == "John"
    assert sample_message.last_name == "Doe"
    assert sample_message.company == "Kaliber Solutions"
    assert sample_message.email == "john.doe@example.com"
    assert sample_message.message.startswith("Interested in your services")
    assert sample_message.date == date(2025, 10, 25)

def test_delete_message(session, sample_message):
    """
    GIVEN a Message model
    WHEN a Message is deleted
    THEN check the Message is removed from the database
    """
    msg_id = sample_message.id

    message = session.get(Messages, msg_id)
    session.delete(message)
    session.commit()

    deleted = session.get(Messages, msg_id)
    assert deleted is None
