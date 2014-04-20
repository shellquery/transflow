"""create_table

Revision ID: 148d8d2c3265
Revises: None
Create Date: 2014-04-13 15:50:42.731766

"""

# revision identifiers, used by Alembic.
revision = '148d8d2c3265'
down_revision = None

from alembic import op
import sqlalchemy as sa
from transflow.core.sqlalchemy.types import JSONType

from sqlalchemy.dialects.postgresql import ENUM


def upgrade():
    sa.Sequence('task_id_seq').create(bind=op.get_bind())
    sa.Sequence('cross_id_seq').create(bind=op.get_bind())
    sa.Sequence('project_id_seq').create(bind=op.get_bind())
    sa.Sequence('user_id_seq').create(bind=op.get_bind())
    sa.Sequence('staff_id_seq').create(bind=op.get_bind())
    sa.Sequence('member_id_seq').create(bind=op.get_bind())
    sa.Sequence('company_id_seq').create(bind=op.get_bind())
    sa.Sequence('document_id_seq').create(bind=op.get_bind())
    sa.Sequence('email_temp_id_seq').create(bind=op.get_bind())
    op.create_table(
        'user_entity_properties',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('properties', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'meta_properties',
        sa.Column('table_name', sa.String(length=256), nullable=False),
        sa.Column('defines', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('table_name')
    )
    op.create_table(
        'cross_in_task',
        sa.Column('cross_id', sa.String(length=40), nullable=False),
        sa.Column('task_id', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('cross_id', 'task_id')
    )
    op.create_table(
        'project_entity_properties',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('properties', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'member_entity_properties',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('properties', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'cross_document',
        sa.Column('cross_id', sa.String(length=40), nullable=False),
        sa.Column('document_id', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('cross_id', 'document_id')
    )
    op.create_table(
        'task_out_cross',
        sa.Column('task_id', sa.String(length=40), nullable=False),
        sa.Column('cross_id', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('task_id', 'cross_id')
    )
    op.create_table(
        'member',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('user_id', sa.String(length=40), nullable=False),
        sa.Column('project_id', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'task_entity_properties',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('properties', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'task',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('is_ready', sa.Boolean(),
                  server_default='false', nullable=False),
        sa.Column('is_finished', sa.Boolean(),
                  server_default='false', nullable=False),
        sa.Column('progress', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.Column('user_id', sa.String(length=40), nullable=False),
        sa.Column('project_id', sa.String(length=40), nullable=False),
        sa.Column('name', sa.Unicode(length=256), nullable=False),
        sa.Column('description', sa.Unicode(length=256), nullable=True),
        sa.Column('date_start', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column('date_end', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'project',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('company_id', sa.String(length=40), nullable=False),
        sa.Column('manage_user_id', sa.String(length=40), nullable=False),
        sa.Column('name', sa.Unicode(length=256), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column('members_count', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.Column('tasks_count', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.Column('crosses_count', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.Column('documents_count', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'cross',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('project_id', sa.String(length=40), nullable=False),
        sa.Column('is_start', sa.Boolean(),
                  server_default='false', nullable=False),
        sa.Column('is_end', sa.Boolean(),
                  server_default='false', nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'staff_entity_properties',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('properties', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'company_entity_properties',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('properties', JSONType(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'document',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('project_id', sa.String(length=40), nullable=False),
        sa.Column('name', sa.Unicode(length=256), nullable=False),
        sa.Column('url', sa.Unicode(length=1024), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('realname', sa.Unicode(length=128), nullable=False),
        sa.Column('introduction', sa.Unicode(length=1024), nullable=True),
        sa.Column('password_hash', sa.CHAR(length=40), nullable=False),
        sa.Column('gender', sa.Enum(u'male', u'femail', u'unknown',
                                    name='user_gender_enum'), nullable=True),
        sa.Column('avatar', sa.String(length=1024), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column('date_last_signed_in', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'email_temp_model',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('random_code', sa.String(length=64), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'staff',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('user_id', sa.String(length=40), nullable=False),
        sa.Column('company_id', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'company',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('name', sa.Unicode(length=256), nullable=False),
        sa.Column('admin_user_id', sa.String(length=40), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True),
                  server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column('staffs_count', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.Column('projects_count', sa.Integer(),
                  server_default=u'0', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'property_key',
        sa.Column('key', sa.String(length=256), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('column_type', sa.String(length=64), nullable=False),
        sa.Column('parameters', JSONType(), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=True),
        sa.PrimaryKeyConstraint('key', 'column_type')
    )


def downgrade():
    op.drop_table('property_key')
    op.drop_table('company')
    op.drop_table('staff')
    op.drop_table('email_temp_model')
    op.drop_table('user')
    op.drop_table('document')
    op.drop_table('company_entity_properties')
    op.drop_table('staff_entity_properties')
    op.drop_table('cross')
    op.drop_table('project')
    op.drop_table('task')
    op.drop_table('task_entity_properties')
    op.drop_table('member')
    op.drop_table('task_out_cross')
    op.drop_table('cross_document')
    op.drop_table('member_entity_properties')
    op.drop_table('project_entity_properties')
    op.drop_table('cross_in_task')
    op.drop_table('meta_properties')
    op.drop_table('user_entity_properties')
    sa.Sequence('task_id_seq').drop(bind=op.get_bind())
    sa.Sequence('cross_id_seq').drop(bind=op.get_bind())
    sa.Sequence('project_id_seq').drop(bind=op.get_bind())
    sa.Sequence('user_id_seq').drop(bind=op.get_bind())
    sa.Sequence('staff_id_seq').drop(bind=op.get_bind())
    sa.Sequence('member_id_seq').drop(bind=op.get_bind())
    sa.Sequence('company_id_seq').drop(bind=op.get_bind())
    sa.Sequence('document_id_seq').drop(bind=op.get_bind())
    sa.Sequence('email_temp_id_seq').drop(bind=op.get_bind())
    ENUM(name='user_gender_enum').drop(op.get_bind(), checkfirst=False)
