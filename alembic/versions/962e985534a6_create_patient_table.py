"""create patient table

Revision ID: 962e985534a6
Revises: 
Create Date: 2026-11-13 22:24:30.362887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '962e985534a6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'patient',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('middle_name', sa.String(length=100), nullable=True),
        sa.Column('date_birth', sa.Date(), nullable=False),
        sa.Column('card_number', sa.String(length=50), nullable=False),
        sa.Column('rating', sa.Float(), server_default='0', nullable=False),
        sa.Column('positive', sa.Text(), nullable=True),
        sa.Column('negativity', sa.Text(), nullable=True),
        sa.Column('attention', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('rating >= 0 AND rating <= 10', name='ck_patient_rating_range'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_patient_last_name'), 'patient', ['last_name'], unique=False)
    op.create_index(op.f('ix_patient_first_name'), 'patient', ['first_name'], unique=False)
    op.create_index(op.f('ix_patient_card_number'), 'patient', ['card_number'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_patient_card_number'), table_name='patient')
    op.drop_index(op.f('ix_patient_first_name'), table_name='patient')
    op.drop_index(op.f('ix_patient_last_name'), table_name='patient')
    op.drop_table('patient')