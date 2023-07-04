"""initial

Revision ID: 60e6bfc3b917
Revises: 
Create Date: 2023-07-04 05:30:45.353630

"""

import sqlalchemy as sa

from pathlib import Path

from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '60e6bfc3b917'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_path = Path(__file__).parent.parent.absolute() / 'schema.dump'

    with open(dump_path, 'r') as sql_reader:
       op.execute(text(sql_reader.read()))

    op.execute(text('SET search_path = public'))


def downgrade() -> None:
    pass
