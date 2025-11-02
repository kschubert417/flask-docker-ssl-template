import click
from flask.cli import with_appcontext
from app import db
from app.models import User

def init_auth_commands(app):
    """Initialize auth-related CLI commands.
    From inside container, run:
    docker exec -it container_name flask create-admin
    """
    
    @app.cli.command()
    @click.option('--email', prompt='Admin Email', help='Email for the admin user')
    @click.option('--firstname', prompt='First Name', help='Name for the admin user')
    @click.option('--lastname', prompt='Last Name', help='Name for the admin user')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the admin user')
    @with_appcontext
    def create_admin(email, firstname, lastname, password):
        """Create an admin user."""
        print(f"Creating adming user with the folliwing details")
        print(f"\tEmail: {email}\n\tFirst Name: {firstname}\n\tLast Name: {lastname}\n\tPassword: {password}")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            click.echo(f'Admin user with email {email} already exists.')
            return

        user = User(email=email, first_name=firstname, last_name=lastname, role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f'Admin user {email} created successfully.')
