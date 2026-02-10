from database import SessionLocal, Student, Test, CompletedTest
from datetime import date
from sqlalchemy import and_

# --- ÖĞRENCİ KAYIT VE GİRİŞ İŞLEMLERİ ---

def register_student(name, username, password, age, gender):
    """
    Yeni bir öğrenci kaydı oluşturur.
    Kullanıcı adı benzersiz olmalıdır.
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
            login_count=1 # İlk kayıt oluştuğunda 1. giriş sayılır (Faz 1)
        )
        session.add(new_student)
        session.commit()
        return True, "Kayıt başarıyla oluşturuldu! Giriş sekmesinden giriş yapabilirsiniz."
    except Exception as e:
        session.rollback()
        return False, f"Kayıt sırasında hata oluştu: {str(e)}"
    finally:
        session.close()

def login_student(username, password):
    """
    Öğrenci girişi yapar.
    Başarılı girişte 'login_count' (giriş sayısı) değerini 1 artırır.
    Bu sayede öğrencinin kaçıncı aşamada olduğunu (Faz) takip ederiz.
    """
    session = SessionLocal()
    try:
        student = session.query(Student).filter_by(username=username, password=password).first()
        if student:
            # Giriş başarılı, faz takibi için sayacı artır
            student.login_count += 1
            session.commit()
            
            # Güncel veriyi döndürmek için refresh yapabiliriz veya direkt objeyi döneriz
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
    """
    Öğrencinin belirtilen testi daha önce çözüp çözmediğini kontrol eder.
    """
    session = SessionLocal()
    try:
        # Önce testin ID'sini bul
        test = session.query(Test).filter_by(name=test_name).first()
        if not test: 
            return False # Test veritabanında hiç yoksa, çözülmemiştir.
        
        # Eşleşen kayıt var mı bak
        exists = session.query(CompletedTest).filter(
            and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)
        ).first()
        
        return exists is not None
    finally:
        session.close()

def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    """
    Tamamlanan test sonucunu, puanları ve üretilen raporu veritabanına kaydeder.
    """
    session = SessionLocal()
    try:
        # Test tablosunda bu test tanımlı mı? Yoksa oluştur.
        test = session.query(Test).filter_by(name=test_name).first()
        if not test:
            test = Test(name=test_name)
            session.add(test)
            session.commit()
            session.refresh(test)

        # Mükerrer kayıt kontrolü (Aynı testi tekrar kaydetmesin)
        exists = session.query(CompletedTest).filter(
            and_(CompletedTest.student_id == student_id, CompletedTest.test_id == test.id)
        ).first()
        
        if exists:
            return True # Zaten kayıtlı

        # Yeni kaydı oluştur
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
    """
    Öğretmen paneli için hiyerarşik veri yapısı döndürür.
    Her öğrenci için: Kişisel Bilgiler + Çözdüğü Testler Listesi.
    """
    session = SessionLocal()
    try:
        students = session.query(Student).all()
        data = []
        for s in students:
            # Öğrencinin testlerini bir liste haline getir
            student_tests = []
            for t in s.tests:
                student_tests.append({
                    "test_name": t.test.name,
                    "date": t.completion_date,
                    "report": t.individual_report,
                    "scores": t.scores,
                    "raw_answers": t.raw_answers
                })
            
            # Ana listeye ekle
            data.append({
                "info": s, # Student objesi (isim, yaş, şifre vb.)
                "tests": student_tests
            })
        return data
    finally:
        session.close()

# --- SİLME VE SIFIRLAMA İŞLEMLERİ ---

def reset_database():
    """
    DİKKAT: Veritabanındaki TÜM tabloları (Öğrenciler, Testler, Sonuçlar) siler.
    Fabrika ayarlarına döndürür.
    """
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
    """
    Öğretmen panelinden seçilen belirli öğrencileri siler.
    Cascade özelliği sayesinde, öğrenci silinince ona ait test sonuçları da otomatik silinir.
    """
    session = SessionLocal()
    try:
        if not student_names_list:
            return False
            
        # İsim listesindeki öğrencileri bul ve sil
        session.query(Student).filter(Student.name.in_(student_names_list)).delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Silme Hatası: {e}")
        return False
    finally:
        session.close()
