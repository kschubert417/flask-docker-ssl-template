from app.models import User

# -----------------------------------------------------------------------------
# Model Creation and Persistence
# -----------------------------------------------------------------------------
def test_create_new_admin_user(sample_admin_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    assert sample_admin_user.email == "test@example.com"
    assert sample_admin_user.check_password('testpassword')
    assert sample_admin_user.role == 'admin'
    assert sample_admin_user.first_name == 'FName'
    assert sample_admin_user.last_name == 'LName'

def test_update_multiple_user_fields(session, sample_admin_user):
    """
    GIVEN a User model
    WHEN a User is updated
    THEN check the new email, hashed_password, and role fields are defined correctly
    """
    sample_admin_user.first_name = 'UpdatedName'
    sample_admin_user.last_name = 'UpdatedLastName'
    sample_admin_user.email = 'update@example.com'
    sample_admin_user.role = 'user'
    sample_admin_user.set_password('newpassword')
    session.commit()

    assert sample_admin_user.first_name == 'UpdatedName'
    assert sample_admin_user.last_name == 'UpdatedLastName'
    assert sample_admin_user.email == 'update@example.com'
    assert sample_admin_user.role == 'user'
    assert sample_admin_user.check_password('newpassword')

def test_delete_user(session, sample_admin_user):
    """
    GIVEN a User model
    WHEN a User is deleted
    THEN check the User is removed from the database
    """
    user_id = sample_admin_user.id

    user = session.get(User, user_id)
    session.delete(user)
    session.commit()

    deleted = session.get(User, user_id)
    assert deleted is None
