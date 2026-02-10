from sqlalchemy import create_engine, Column, Integer, String, Date, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)       # Ad Soyad
    username = Column(String, unique=True) # Kullanıcı Adı
    password = Column(String)   # Şifre
    age = Column(Integer)       # Yaş
    gender = Column(String)     # Cinsiyet
    login_count = Column(Integer, default=0) # Faz takibi için giriş sayısı

    # Cascade delete: Öğrenci silinirse testleri de silinir
    tests = relationship("CompletedTest", back_populates="student", cascade="all, delete-orphan")

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    completed_tests = relationship("CompletedTest", back_populates="test")

class CompletedTest(Base):
    __tablename__ = 'completed_tests'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    test_id = Column(Integer, ForeignKey('tests.id'))
    completion_date = Column(Date)
    raw_answers = Column(JSON)
    scores = Column(JSON)
    individual_report = Column(String)

    student = relationship("Student", back_populates="tests")
    test = relationship("Test", back_populates="completed_tests")

# Veritabanı Bağlantısı (SQLite)
DATABASE_URL = "sqlite:///psiko_test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
