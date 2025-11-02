from app import create_app, db
from app.config import TestConfig
from app.models import User
from sqlalchemy import select

def run_tests():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        print("=======================================================================")
        print("=========== Testing User Model ===================================")
        print("=======================================================================")
        # Create a test admin user
        testemail = "test@example.com"
        print("Creating user.............")
        user = User(email=testemail, first_name='FName', last_name='Lname', role='admin')
        user.set_password('testpassword')
        print("Password Valid?", user.check_password('testpassword'))
        db.session.add(user)
        db.session.commit()
        print("User created successfully: ", user)

        print("\nFetching user..............")
        stmt = select(User).where(User.email == testemail)
        user = db.session.scalar(stmt)
        print(f"{user} found:\n\tUser email: {user.email}\n\tPassword Hash: {user.password_hash}\n\tRole: {user.role}\n\tFirst Name: {user.first_name}\n\tLast Name: {user.last_name}")
        

        print("\nUpdating User...............")
        user.first_name = 'UpdatedFName'
        user.last_name = 'UpdatedLName'
        db.session.commit()
        print("User updated successfully: ", user)
        stmt = select(User).where(User.email == testemail)
        user = db.session.scalar(stmt)
        print(f"User found:\n\tUser email: {user.email}\n\tLast Name: {user.last_name}\n\tRole: {user.role}\n\tFirst Name: {user.first_name}\n\tLast Name: {user.last_name}")

        print("\nDeleting User ...............")
        stmt = select(User).where(User.email == testemail)
        user = db.session.scalar(stmt)
        if user:
            user = db.session.delete(user)
            db.session.commit()
            print("User deleted successfully.")
        else:
            print("User not found")

if __name__ == '__main__':
    run_tests()