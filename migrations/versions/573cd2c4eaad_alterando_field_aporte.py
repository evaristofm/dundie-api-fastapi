"""alterando field aporte

Revision ID: 573cd2c4eaad
Revises: 5438375a44ea
Create Date: 2024-05-26 04:59:49.035463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '573cd2c4eaad'
down_revision: Union[str, None] = '5438375a44ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plano', 'aporte',
               existing_type=sa.VARCHAR(),
               type_=sa.Numeric(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plano', 'aporte',
               existing_type=sa.Numeric(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
