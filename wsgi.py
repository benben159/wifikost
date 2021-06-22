#!/user/bin/env python
import click

from app import create_app, db, models, forms
from tests import test_app
from getpass import getpass
app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()


@app.cli.command()
@click.confirmation_option(prompt='Drop all database tables?')
def drop_db():
    """Drop the current database."""
    db.drop_all()

@app.cli.command()
@click.argument('username')
def add_superadmin(username):
    user = models.User()
    passwd1 = getpass("enter password:")
    passwd2 = getpass("confirm password:")
    if passwd1 != passwd2:
        print("password do not match. exiting...")
        exit(1)
    user.username = username
    user.password = passwd1
    user.is_superadmin = True
    user.save()
    print("user {} created".format(username))

if __name__ == '__main__':
    app.run()
