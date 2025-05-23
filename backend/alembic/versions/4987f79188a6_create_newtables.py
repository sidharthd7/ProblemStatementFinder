"""create_newtables

Revision ID: 4987f79188a6
Revises: 
Create Date: 2025-05-02 05:38:40.431629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4987f79188a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.drop_table('team_members')
    op.drop_table('problem_tech_stack')
    op.drop_table('tech_stacks')
    op.add_column('problems', sa.Column('tech_stack', sa.JSON(), nullable=False))
    op.add_column('problems', sa.Column('match_score', sa.Integer(), nullable=True))
    op.add_column('problems', sa.Column('source_file', sa.String(), nullable=False))
    op.create_index(op.f('ix_problems_id'), 'problems', ['id'], unique=False)
    op.drop_column('problems', 'updated_at')
    op.drop_column('problems', 'category')
    op.drop_column('problems', 'requirements')
    op.drop_column('problems', 'difficulty_level')
    op.drop_column('problems', 'source')
    op.add_column('teams', sa.Column('name', sa.String(), nullable=False))
    op.add_column('teams', sa.Column('tech_skills', sa.JSON(), nullable=False))
    op.add_column('teams', sa.Column('experience_level', sa.String(), nullable=False))
    op.add_column('teams', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.alter_column('teams', 'deadline',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)
    op.create_foreign_key(None, 'teams', 'users', ['owner_id'], ['id'])
    op.drop_column('teams', 'preferred_domains')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('preferred_domains', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.alter_column('teams', 'deadline',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('teams', 'owner_id')
    op.drop_column('teams', 'experience_level')
    op.drop_column('teams', 'tech_skills')
    op.drop_column('teams', 'name')
    op.add_column('problems', sa.Column('source', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('problems', sa.Column('difficulty_level', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('problems', sa.Column('requirements', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('problems', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('problems', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_problems_id'), table_name='problems')
    op.drop_column('problems', 'source_file')
    op.drop_column('problems', 'match_score')
    op.drop_column('problems', 'tech_stack')
    op.create_table('tech_stacks',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tech_stacks_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tech_stacks_pkey'),
    sa.UniqueConstraint('name', name='tech_stacks_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('problem_tech_stack',
    sa.Column('problem_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tech_stack_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], name='problem_tech_stack_problem_id_fkey'),
    sa.ForeignKeyConstraint(['tech_stack_id'], ['tech_stacks.id'], name='problem_tech_stack_tech_stack_id_fkey')
    )
    op.create_table('team_members',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('skill', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('proficiency_level', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name='team_members_team_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='team_members_pkey')
    )
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
