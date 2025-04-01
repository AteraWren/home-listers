"""Initial migration

Revision ID: d59b164ebf32
Revises: 9c3e680dde59
Create Date: 2025-03-27 20:25:38.588115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd59b164ebf32'
down_revision = '9c3e680dde59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=500),
               existing_nullable=False)
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('location',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.String(length=500),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('title',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###
