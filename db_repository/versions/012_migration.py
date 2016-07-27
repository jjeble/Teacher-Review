from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
    Column('teacher', VARCHAR(length=140)),
    Column('teacher_id', INTEGER),
)

teacher = Table('teacher', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('subject', String(length=120)),
    Column('grade', String(length=5)),
    Column('rating', String(length=5)),
    Column('college', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['teacher'].drop()
    post_meta.tables['teacher'].columns['grade'].create()
    post_meta.tables['teacher'].columns['rating'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['teacher'].create()
    post_meta.tables['teacher'].columns['grade'].drop()
    post_meta.tables['teacher'].columns['rating'].drop()
