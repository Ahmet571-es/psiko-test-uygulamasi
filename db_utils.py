from database import SessionLocal, Student, Test, CompletedTest
from datetime import date
from sqlalchemy import and_

# --- ÖĞRENCİ KAYIT VE GİRİŞ İŞLEMLERİ ---

def register_student(name, username, password, age, gender):
    """
    Yeni bir öğrenci kaydı oluşturur.
    Başarılı olursa (True, student_obj) döner.
    Hata olursa (False, "Hata Mesajı") döner.
    """
    session = SessionLocal()
    try:
        # Kullanıcı adı kontrolü
        existing = session.query(Student).filter_by(username=username).first()
        if existing:
            return False, "Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane deneyin."
        
        new_student = Student(
            name=name,
            username=username,
            password=password,
            age=age,
            gender=gender,
            login_count=1 # İlk kayıt = 1. Faz
        )
        session.add(new_student)
        session.commit()
        session.refresh(new_student) # Yeni öğrencinin ID'sini almak için yenile
        return True, new_student
    except Exception as e:
        session.rollback()
        return False, f"Kayıt sırasında hata oluştu: {str(e)}"
    finally:
        session.close()

def login_student(username, password):
    """
    Öğrenci girişi yapar.
    Başarılı girişte 'login_count' (giriş sayısı) değerini 1 artırır.
    """
    session = SessionLocal()
    try:
        student = session.query(Student).filter_by(username=username, password=password).first()
        if student:
            student.login_count += 1
            session.commit()
            session.refresh(student)
            return True, student
        return False, None
    except Exception as e:
        return False, None
    finally:
        session.close()

def get_student_details(student_id):
    """ID'si verilen öğrencinin tüm kişisel bilgilerini getirir."""
    session = SessionLocal()
    try:
        return session.query(Student).filter_by(id=student_id).first()
    finally:
        session.close()

# --- TEST YÖNETİM İŞLEMLERİ ---

def check_test_completed(student_id, test_name):
    """Öğrencinin belirtilen testi daha önce çözüp çözmediğini kontrol eder."""
    session = SessionLocal()
    try:
        test = session.query(Test).filter_by(name=test_name).first()
        if not test: 
            return False
        
        exists = session.query(CompletedTest).filter(
            and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)
        ).first()
        
        return exists is not None
    finally:
        session.close()

def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    """Tamamlanan test sonucunu kaydeder."""
    session = SessionLocal()
    try:
        test = session.query(Test).filter_by(name=test_name).first()
        if not test:
            test = Test(name=test_name)
            session.add(test)
            session.commit()
            session.refresh(test)

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
        print(f"Veritabanı Kayıt Hatası: {e}")
        return False
    finally:
        session.close()

# --- ÖĞRETMEN PANELİ VERİ ÇEKME İŞLEMLERİ ---

def get_all_students_with_results():
    """Öğretmen paneli için hiyerarşik veri yapısı döndürür."""
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
            data.append({
                "info": s,
                "tests": student_tests
            })
        return data
    finally:
        session.close()

# --- SİLME VE SIFIRLAMA İŞLEMLERİ ---

def reset_database():
    """TÜM veriyi siler."""
    session = SessionLocal()
    try:
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
    """Seçilen öğrencileri siler."""
    session = SessionLocal()
    try:
        if not student_names_list:
            return False
        session.query(Student).filter(Student.name.in_(student_names_list)).delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()
