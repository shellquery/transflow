"""create_tables

Revision ID: 48aea8937167
Revises: None
Create Date: 2014-03-08 21:30:11.875898

"""

# revision identifiers, used by Alembic.
revision = '48aea8937167'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    sa.Sequence('user_id_seq').create(bind=op.get_bind())
    op.create_table(
        'account',
        sa.Column('id', sa.String(length=12), nullable=False),
        sa.Column('email', sa.String(length=256), unique=True,
                  index=True, nullable=False),
        sa.Column('realname', sa.Unicode(length=128),
                  index=True, nullable=False),
        sa.Column('unikey', sa.String(length=256),
                  unique=True, index=True, nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(),
                  index=True, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('account')
    sa.Sequence('user_id_seq').drop(bind=op.get_bind())
