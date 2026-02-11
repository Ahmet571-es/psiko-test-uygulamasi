from database import SessionLocal, Student, Test, CompletedTest, Base, engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine, and_
from sqlalchemy.orm import relationship
from datetime import date

# --- TABLO TANIMLARI ---
class StudentAnalysis(Base):
    __tablename__ = 'student_analysis'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    test_combination = Column(String) # Hangi testlerin analizi (Örn: "Enneagram,VARK")
    report_text = Column(Text)        # Rapor metni
    created_at = Column(String)       # Tarih (String olarak tutalım: YYYY-MM-DD)

Base.metadata.create_all(bind=engine)

# --- KAYIT VE GİRİŞ ---
def register_student(name, username, password, age, gender):
    session = SessionLocal()
    try:
        existing = session.query(Student).filter_by(username=username).first()
        if existing:
            return False, "Bu kullanıcı adı alınmış."
        new_student = Student(name=name, username=username, password=password, age=age, gender=gender, login_count=1)
        session.add(new_student)
        session.commit()
        session.refresh(new_student)
        return True, new_student
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()

def login_student(username, password):
    session = SessionLocal()
    try:
        student = session.query(Student).filter_by(username=username, password=password).first()
        if student:
            student.login_count += 1
            session.commit()
            session.refresh(student)
            return True, student
        return False, None
    except:
        return False, None
    finally:
        session.close()

def get_student_details(student_id):
    session = SessionLocal()
    try:
        return session.query(Student).filter_by(id=student_id).first()
    finally:
        session.close()

# --- TEST İŞLEMLERİ ---
def check_test_completed(student_id, test_name):
    session = SessionLocal()
    try:
        test = session.query(Test).filter_by(name=test_name).first()
        if not test: return False
        exists = session.query(CompletedTest).filter(and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)).first()
        return exists is not None
    finally:
        session.close()

def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    session = SessionLocal()
    try:
        test = session.query(Test).filter_by(name=test_name).first()
        if not test:
            test = Test(name=test_name)
            session.add(test)
            session.commit()
            session.refresh(test)
        
        exists = session.query(CompletedTest).filter(and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)).first()
        if exists: return True

        new_record = CompletedTest(
            student_id=student_id, test_id=test.id, completion_date=date.today(),
            raw_answers=raw_answers, scores=scores, individual_report=report_text
        )
        session.add(new_record)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

# --- ANALİZ RAPORU İŞLEMLERİ (YENİLENEN KISIM) ---

def save_holistic_analysis(student_id, test_names_list, report_text):
    """Analiz raporunu kaydeder."""
    session = SessionLocal()
    try:
        combo_key = " + ".join(sorted(test_names_list)) # İsimleri daha şık birleştirelim
        today_str = date.today().strftime("%Y-%m-%d")

        existing = session.query(StudentAnalysis).filter(
            and_(StudentAnalysis.student_id == student_id, StudentAnalysis.test_combination == combo_key)
        ).first()
        
        if existing:
            existing.report_text = report_text
            existing.created_at = today_str
        else:
            new_analysis = StudentAnalysis(
                student_id=student_id,
                test_combination=combo_key,
                report_text=report_text,
                created_at=today_str
            )
            session.add(new_analysis)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def get_student_analysis_history(student_id):
    """
    Bir öğrenciye ait TÜM kayıtlı analiz raporlarını liste olarak getirir.
    Senin istediğin 'Kayıtlı Raporları Getir' butonu için bu fonksiyonu kullanacağız.
    """
    session = SessionLocal()
    try:
        results = session.query(StudentAnalysis).filter_by(student_id=student_id).all()
        # Veriyi sözlük listesine çevirip dönelim
        history = []
        for r in results:
            history.append({
                "combination": r.test_combination,
                "date": r.created_at,
                "report": r.report_text
            })
        return history
    finally:
        session.close()

# --- VERİ ÇEKME ---
def get_all_students_with_results():
    session = SessionLocal()
    try:
        students = session.query(Student).all()
        data = []
        for s in students:
            student_tests = []
            for t in s.tests:
                student_tests.append({
                    "test_name": t.test.name,
                    "date": t.completion_date,
                    "report": t.individual_report,
                    "scores": t.scores,
                    "raw_answers": t.raw_answers
                })
            data.append({"info": s, "tests": student_tests})
        return data
    finally:
        session.close()

# --- SİLME ---
def reset_database():
    session = SessionLocal()
    try:
        session.query(StudentAnalysis).delete()
        session.query(CompletedTest).delete()
        session.query(Student).delete()
        session.query(Test).delete()
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def delete_specific_students(student_names_list):
    session = SessionLocal()
    try:
        if not student_names_list: return False
        session.query(Student).filter(Student.name.in_(student_names_list)).delete(synchronize_session=False)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()
