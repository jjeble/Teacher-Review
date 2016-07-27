from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
teacher = Table('teacher', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('subject', VARCHAR(length=120)),
    Column('college', VARCHAR(length=120)),
    Column('grade', VARCHAR(length=5)),
    Column('rating', VARCHAR(length=5)),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('teacher_id', Integer),
    Column('grade', String(length=5)),
    Column('rating', String(length=5)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['teacher'].columns['grade'].drop()
    pre_meta.tables['teacher'].columns['rating'].drop()
    post_meta.tables['post'].columns['grade'].create()
    post_meta.tables['post'].columns['rating'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['teacher'].columns['grade'].create()
    pre_meta.tables['teacher'].columns['rating'].create()
    post_meta.tables['post'].columns['grade'].drop()
    post_meta.tables['post'].columns['rating'].drop()
