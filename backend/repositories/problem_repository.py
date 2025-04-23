from sqlalchemy.orm import Session
from models.database import Problem, TechStack
from models.schema import ProblemStatement
from typing import List, Optional

class ProblemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_problem(self, problem: ProblemStatement) -> Problem:
        # Create or get tech stack entries
        tech_stacks = []
        for tech in problem.tech_stack:
            tech_stack = self.db.query(TechStack).filter(TechStack.name == tech).first()
            if not tech_stack:
                tech_stack = TechStack(name=tech)
                self.db.add(tech_stack)
            tech_stacks.append(tech_stack)
        
        # Create problem
        db_problem = Problem(
            title=problem.title,
            description=problem.description,
            category=problem.category,
            difficulty_level=problem.difficulty_level,
            source=problem.source,
            requirements=problem.requirements.dict() if problem.requirements else None,
            tech_stacks=tech_stacks
        )
        
        self.db.add(db_problem)
        self.db.commit()
        self.db.refresh(db_problem)
        return db_problem

    def get_all_problems(self) -> List[Problem]:
        return self.db.query(Problem).all()

    def get_problem_by_id(self, problem_id: int) -> Optional[Problem]:
        return self.db.query(Problem).filter(Problem.id == problem_id).first()

    def update_problem(self, problem_id: int, problem_data: ProblemStatement) -> Optional[Problem]:
        db_problem = self.get_problem_by_id(problem_id)
        if not db_problem:
            return None
            
        # Update fields
        for key, value in problem_data.dict(exclude_unset=True).items():
            if key == 'tech_stack':
                # Handle tech stack updates
                tech_stacks = []
                for tech in value:
                    tech_stack = self.db.query(TechStack).filter(TechStack.name == tech).first()
                    if not tech_stack:
                        tech_stack = TechStack(name=tech)
                        self.db.add(tech_stack)
                    tech_stacks.append(tech_stack)
                db_problem.tech_stacks = tech_stacks
            else:
                setattr(db_problem, key, value)
        
        self.db.commit()
        self.db.refresh(db_problem)
        return db_problem
