from ellar.common import command, EllarTyper

db = EllarTyper(name='db')


@db.command()
def create_migration():
    """Creates Database Migration"""


@command()
def whatever_you_want():
    """Whatever you want"""
