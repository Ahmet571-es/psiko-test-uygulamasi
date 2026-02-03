from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, ForeignKey, Text, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
import datetime

# Veritabanı Dosyası Adı
DB_FILE = "data.db"

# Veritabanı Motoru
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

# --- TABLO MODELLERİ ---

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    completed_tests = relationship("CompletedTest", back_populates="student")

class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

class CompletedTest(Base):
    __tablename__ = "completed_tests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    completion_date = Column(Date, nullable=False, default=datetime.date.today)
    completion_timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now)
    raw_answers = Column(JSON, nullable=False)
    scores = Column(JSON, nullable=True)
    individual_report = Column(Text, nullable=True)

    __table_args__ = (UniqueConstraint('student_id', 'test_id', name='unique_student_test'),)

    student = relationship("Student", back_populates="completed_tests")
    test = relationship("Test")

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Sabit Test Listesi (Senin listendekiyle birebir aynı)
    TEST_NAMES = [
        "Enneagram Kişilik Testi", 
        "d2 Dikkat Testi", 
        "Burdon Dikkat Testi",
        "Çoklu Zeka Testi (Gardner)", 
        "Holland Mesleki İlgi Envanteri (RIASEC)",
        "VARK Öğrenme Stilleri Testi", 
        "Sağ-Sol Beyin Dominansı Testi",
        "Çalışma Davranışı Ölçeği (Baltaş)", 
        "Sınav Kaygısı Ölçeği (DuSKÖ)"
    ]
    
    session = SessionLocal()
    try:
        for t_name in TEST_NAMES:
            exists = session.query(Test).filter_by(name=t_name).first()
            if not exists:
                session.add(Test(name=t_name))
        session.commit()
    except Exception as e:
        print(f"Veritabanı Başlatma Hatası: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()