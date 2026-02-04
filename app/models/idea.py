from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserProfile(Base):
    """Store user profiles for idea generation."""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    skills = Column(JSON, nullable=False)  # ["Python", "JavaScript"]
    interests = Column(JSON, nullable=False)  # ["AI/ML", "Web Dev"]
    experience_level = Column(String(50), nullable=False)  # beginner/intermediate/advanced
    goal = Column(String(100), nullable=False)  # learn/portfolio/startup/hackathon
    time_available = Column(String(50), nullable=False)  # "1 week", "1 month"
    preferences = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to generated ideas
    ideas = relationship("GeneratedIdea", back_populates="user_profile")


class GeneratedIdea(Base):
    """Store generated project ideas."""
    __tablename__ = "generated_ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    
    # Project idea details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), nullable=False)
    estimated_time = Column(String(100), nullable=False)
    
    # Detailed breakdown (stored as JSON)
    features = Column(JSON, nullable=True)
    tech_stack = Column(JSON, nullable=True)
    roadmap = Column(JSON, nullable=True)
    learning_path = Column(JSON, nullable=True)
    
    # Metadata
    is_selected = Column(Integer, default=0)  # 0 = not selected, 1 = selected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user_profile = relationship("UserProfile", back_populates="ideas")
