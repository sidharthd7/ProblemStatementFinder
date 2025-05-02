from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between problems and tech stack
problem_tech_stack = Table(
    'problem_tech_stack',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id')),
    Column('tech_stack_id', Integer, ForeignKey('tech_stacks.id'))
)

class Problem(Base):
    __tablename__ = 'problems'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String)
    difficulty_level = Column(String, default="Medium")
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with tech stack
    tech_stacks = relationship("TechStack", secondary=problem_tech_stack, back_populates="problems")
    
    # Project requirements as JSON
    requirements = Column(JSON)

class TechStack(Base):
    __tablename__ = 'tech_stacks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    problems = relationship("Problem", secondary=problem_tech_stack, back_populates="tech_stacks")

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    team_size = Column(Integer, nullable=False)
    preferred_domains = Column(JSON)  # Store as JSON array
    deadline = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with team members
    members = relationship("TeamMember", back_populates="team")

class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    skill = Column(String, nullable=False)
    proficiency_level = Column(String, nullable=False)
    
    team = relationship("Team", back_populates="members")
