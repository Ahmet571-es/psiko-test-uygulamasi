from database import SessionLocal, Student, Test, CompletedTest
from datetime import date
from sqlalchemy import and_

def get_or_create_student(name):
    """Öğrenci varsa getirir, yoksa yeni oluşturur."""
    session = SessionLocal()
    try:
        student = session.query(Student).filter_by(name=name).first()
        if not student:
            student = Student(name=name)
            session.add(student)
            session.commit()
            session.refresh(student)
        return student.id, student.name
    finally:
        session.close()

def check_daily_limit(student_id):
    """Günlük limit kontrolü (Max 2 test)."""
    session = SessionLocal()
    try:
        today = date.today()
        count = session.query(CompletedTest).filter(
            and_(CompletedTest.student_id == student_id, CompletedTest.completion_date == today)
        ).count()
        return count < 200 # Test rahat olsun diye limiti artırdım, istersen 2 yap.
    finally:
        session.close()

def check_test_completed(student_id, test_name):
    """Öğrenci bu testi daha önce çözmüş mü?"""
    session = SessionLocal()
    try:
        test = session.query(Test).filter_by(name=test_name).first()
        if not test: return False
        
        exists = session.query(CompletedTest).filter(
            and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)
        ).first()
        return exists is not None
    finally:
        session.close()

def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    """Test sonucunu ve raporu kaydeder."""
    session = SessionLocal()
    try:
        test = session.query(Test).filter_by(name=test_name).first()
        if test:
            # Çift kayıt kontrolü
            exists = session.query(CompletedTest).filter(
                and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)
            ).first()
            
            if exists:
                return True

            new_record = CompletedTest(
                student_id=student_id,
                test_id=test.id,
                completion_date=date.today(),
                raw_answers=raw_answers,
                scores=scores,
                individual_report=report_text
            )
            session.add(new_record)
            session.commit()
            return True
    except Exception as e:
        session.rollback()
        print(f"Kayıt Hatası: {e}")
        return False
    finally:
        session.close()

def get_all_results():
    """Öğretmen paneli için tüm sonuçları çeker."""
    session = SessionLocal()
    try:
        results = session.query(CompletedTest).join(Student).join(Test).all()
        data = []
        for r in results:
            data.append({
                "Öğrenci": r.student.name,
                "Test": r.test.name,
                "Tarih": r.completion_date,
                "Rapor": r.individual_report,
                "Ham Cevaplar": r.raw_answers,
                "Puanlar": r.scores
            })
        return data
    finally:
        session.close()