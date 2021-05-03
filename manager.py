  
from super_nft import create_app
from super_nft.extensions import db
from super_nft.blueprints.public.models import User

from flask_script import Manager, Server, Shell
import click
app = create_app()
banner = r"""

 ____                                                    __  __      ____     ______
/\  _`\                                                 /\ \/\ \    /\  _`\  /\__  _\
\ \,\L\_\    __  __   _____      __    _ __             \ \ `\\ \   \ \ \L\_\\/_/\ \/
 \/_\__ \   /\ \/\ \ /\ '__`\  /'__`\ /\`'__\            \ \ , ` \   \ \  _\/   \ \ \
   /\ \L\ \ \ \ \_\ \\ \ \L\ \/\  __/ \ \ \/              \ \ \`\ \   \ \ \/     \ \ \
   \ `\____\ \ \____/ \ \ ,__/\ \____\ \ \_\               \ \_\ \_\   \ \_\      \ \_\
    \/_____/  \/___/   \ \ \/  \/____/  \/_/                \/_/\/_/    \/_/       \/_/
                        \ \_\
                         \/_/
"""

manager = Manager(app)


def make_shell_context():
    return {
        "app": app,
    }

manager.add_command("runserver", Server(host="127.0.0.1", port=5000, use_debugger=True))
manager.add_command("shell", Shell(banner=banner, make_context=make_shell_context))

@manager.command
def reset_local_db():
    """Reset local databases."""
    click.confirm('This operation will delete the local database, do you want to continue?', abort=True)
    db.drop_all(bind=None)
    click.echo('Drop local tables.')
    db.create_all(bind=None)
    click.echo('Reset local database.')

@manager.command
def reset_server_db():
    """Reset server databases."""
    click.confirm('This operation will delete the server database, do you want to continue?', abort=True)
    db.drop_all(bind="userserver")
    click.echo('Drop local tables.')
    db.create_all(bind="userserver")
    click.echo('Success create server databases.')
    click.echo('Reset server database.')
    admin = User(
        username='admin',
        email='admin@admin.com',
        is_admin=True,
        active=True,
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')


@manager.command
def reset_db():
    """Reset all databases."""
    click.confirm('This operation will delete all database, do you want to continue?', abort=True)
    db.drop_all()
    click.echo('Drop all tables.')
    db.create_all()
    click.echo('Reset all database.')
    admin = User(
        username='admin',
        email='admin@admin.com',
        is_admin=True,
        active=True,
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')



@manager.command
def init_local_db():
    """Initialized local databases."""
    db.create_all(bind=None)
    click.echo('Initialized local database.')


@manager.command
def init_server_db():
    """Initialized server databases."""
    db.create_all(bind="userserver")
    click.echo('Initialized server database.')
    admin = User(
        username='admin',
        email='admin@admin.com',
        is_admin=True,
        active=True,
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')

@manager.command
def init_db():
    """Initialized all databases."""
    db.create_all()
    click.echo('Initialized all database.')
    admin = User(
        username='admin',
        email='admin@admin.com',
        is_admin=True,
        active=True,
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')

@manager.command
def set_user(username, email, password, active=True):
    """Add A New User."""
    if User.query.filter(User.username==username).first() and User.query.filter(User.email==email).first() and active:
        user = User.query.filter(User.username==username).first()
        user.active = True
        click.echo('Success Update A New User to Active')
    else:
        user = User(username=username, email=email, active=active, id=None)
        # add a User(active = False)
        user.set_password(password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit(user)
        click.echo("Success Add A New Active User.")

if __name__ == "__main__":
    manager.run()
