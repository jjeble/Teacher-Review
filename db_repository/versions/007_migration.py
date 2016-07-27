from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
teacher = Table('teacher', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('subject', String(length=120)),
    Column('college', String(length=120)),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('teacher', String(length=140)),
    Column('user_id', Integer),
    Column('teacher_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['teacher'].create()
    post_meta.tables['post'].columns['teacher'].create()
    post_meta.tables['post'].columns['teacher_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['teacher'].drop()
    post_meta.tables['post'].columns['teacher'].drop()
    post_meta.tables['post'].columns['teacher_id'].drop()
