"""init chema

Revision ID: c58645865cd2
Revises: 
Create Date: 2022-02-22 19:56:34.856248

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'c58645865cd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
    END;
    $$ language 'plpgsql';
    """)

    op.execute("""
    CREATE TABLE departments(
        id UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
        name VARCHAR(30) NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
        updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
    );
    """)

    op.execute("""
    CREATE TRIGGER departments_updated_at_trigger
    BEFORE UPDATE ON departments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)

    op.create_table(
        "positions",
        sa.Column("id", UUID, primary_key=True, server_default=sa.func.uuid_generate_v1()),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.execute("""
    CREATE TRIGGER positions_updated_at_trigger
    BEFORE UPDATE ON positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)

    op.create_table(
        "skills",
        sa.Column("id", UUID, primary_key=True, server_default=sa.func.uuid_generate_v1()),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.execute("""
    CREATE TRIGGER skills_updated_at_trigger
    BEFORE UPDATE ON skills
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)

    op.create_table(
        "workers",
        sa.Column("id", UUID, primary_key=True, server_default=sa.func.uuid_generate_v1()),
        sa.Column("surname", sa.String, nullable=True),
        sa.Column("name", sa.String, nullable=True),
        sa.Column(
            "department_id",
            UUID,
            ForeignKey("departments.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "position_id",
            UUID,
            ForeignKey("positions.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("birth_date", sa.DateTime, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.execute("""
    CREATE TRIGGER workers_updated_at_trigger
    BEFORE UPDATE ON workers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)

    op.create_table(
        "worker_skills",
        sa.Column(
            "worker_id",
            UUID,
            ForeignKey("workers.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            "skill_id",
            UUID,
            ForeignKey("skills.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("worker_skills")

    op.execute("""DROP FUNCTION IF EXISTS worker_updated_at_trigger;""")
    op.drop_table("worker")

    op.execute("""DROP FUNCTION IF EXISTS skills_updated_at_trigger;""")
    op.drop_table("skills")

    op.execute("""DROP FUNCTION IF EXISTS positions_updated_at_trigger;""")
    op.drop_table("positions")

    op.drop_table("departments")
    op.execute("""DROP TRIGGER IF EXISTS departments_updated_at_trigger ON departments;""")
    op.execute("""DROP FUNCTION IF EXISTS update_updated_at_column;""")
