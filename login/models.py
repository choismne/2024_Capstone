from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=True)
    total_miso = Column(Integer, default=0)

    moods = relationship("Mood", back_populates="User")
    poses = relationship("Pose", back_populates="User")

class Mood(Base):
    __tablename__ = 'moods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), ForeignKey('users.username'))
    lovely_count = Column(Integer, default=0)
    cheerful_count = Column(Integer, default=0)
    cute_count = Column(Integer, default=0)
    playful_count = Column(Integer, default=0)
    harmonious_count = Column(Integer, default=0)
    scary_count = Column(Integer, default=0)

    user = relationship("User", back_populates="moods")

class Pose(Base):
    __tablename__ = 'poses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), ForeignKey('users.username'))
    v_pose_count = Column(Integer, default=0)
    flower_pose_count = Column(Integer, default=0)
    heart_pose_count = Column(Integer, default=0)
    arms_crossed_count = Column(Integer, default=0)
    kiss_pose_count = Column(Integer, default=0)
    thumbs_up_count = Column(Integer, default=0)
    wink_count = Column(Integer, default=0)

    user = relationship("User", back_populates="poses")

 