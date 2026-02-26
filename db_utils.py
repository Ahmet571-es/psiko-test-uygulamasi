import json
import hashlib
import pandas as pd
from datetime import datetime
import os
import streamlit as st

# ============================================================
# 🗄️ VERİTABANI BAĞLANTI YÖNETİMİ
# ============================================================
# Supabase (PostgreSQL) bağlantısı varsa onu kullanır.
# Yoksa SQLite ile çalışır (lokal geliştirme / fallback).
# ============================================================

try:
    import psycopg2
    import psycopg2.extras
    DB_ENGINE = "postgresql"
except ImportError:
    DB_ENGINE = "sqlite"
    import sqlite3

# SQLite fallback DB adı
SQLITE_DB_NAME = "school_data.db"


def get_db_url():
    """
    Supabase PostgreSQL bağlantı URL'sini alır.
    Öncelik: st.secrets → ortam değişkeni
    Bulunamazsa None döner (SQLite fallback).
    """
    try:
        if "SUPABASE_DB_URL" in st.secrets:
            return st.secrets["SUPABASE_DB_URL"]
    except Exception:
        pass

    env_url = os.getenv("SUPABASE_DB_URL")
    if env_url:
        return env_url

    return None


def get_connection():
    """
    Veritabanı bağlantısı döndürür.
    - Supabase URL varsa → PostgreSQL bağlantısı
    - Yoksa → SQLite fallback (lokal geliştirme)
    """
    db_url = get_db_url()

    if db_url and DB_ENGINE == "postgresql":
        try:
            conn = psycopg2.connect(db_url, connect_timeout=10)
            conn.autocommit = False
            return conn, "postgresql"
        except Exception as e:
            print(f"PostgreSQL bağlantı hatası, SQLite'a geçiliyor: {e}")

    # SQLite Fallback
    if DB_ENGINE == "sqlite":
        conn = sqlite3.connect(SQLITE_DB_NAME)
        return conn, "sqlite"

    # psycopg2 yüklü ama bağlantı başarısız → SQLite fallback
    import sqlite3 as sq3
    conn = sq3.connect(SQLITE_DB_NAME)
    return conn, "sqlite"


def is_using_sqlite():
    """Veritabanı SQLite mi kullanıyor? (Kalıcılık uyarısı için)"""
    return get_db_url() is None


def get_placeholder(engine):
    """SQL placeholder: PostgreSQL=%s, SQLite=?"""
    return "%s" if engine == "postgresql" else "?"


# ============================================================
# SINIF TANIMLAMALARI
# ============================================================

class Student:
    """login_student fonksiyonunun döndürdüğü öğrenci nesnesi."""
    def __init__(self, data, login_count):
        self.id          = data[0]
        self.name        = data[1]
        self.username    = data[2]
        self.password    = data[3]
        self.age         = data[4]
        self.gender      = data[5]
        self.grade       = data[6]  # Sınıf numarası (5-12)
        self.login_count = login_count


class StudentInfo:
    """get_all_students_with_results fonksiyonunun döndürdüğü öğrenci nesnesi."""
    def __init__(self, data):
        self.id          = data[0]
        self.name        = data[1]
        self.username    = data[2]
        self.password    = data[3]
        self.age         = data[4]
        self.gender      = data[5]
        self.grade       = data[6]  # Sınıf numarası (5-12)
        self.login_count = data[7]


# ============================================================
# ŞİFRE YARDIMCI FONKSİYONU
# ============================================================

def hash_password(password: str) -> str:
    """SHA-256 ile şifre hash'ler."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ============================================================
# VERİTABANI BAŞLATMA
# ============================================================

def init_db():
    """
    Veritabanı tablolarını oluşturur.
    PostgreSQL ve SQLite uyumlu.
    """
    conn, engine = get_connection()
    c = conn.cursor()

    try:
        if engine == "postgresql":
            # --- PostgreSQL Tabloları ---
            c.execute('''CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name TEXT,
                username TEXT UNIQUE,
                password TEXT,
                age INTEGER,
                gender TEXT,
                grade INTEGER,
                login_count INTEGER DEFAULT 0,
                secret_word TEXT
            )''')

            # Mevcut tablo varsa grade sütunu ekle (migration)
            try:
                c.execute("ALTER TABLE students ADD COLUMN grade INTEGER")
            except Exception:
                pass

            c.execute('''CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                test_name TEXT,
                raw_answers TEXT,
                scores TEXT,
                report TEXT,
                date TIMESTAMP DEFAULT NOW()
            )''')

            c.execute('''CREATE TABLE IF NOT EXISTS analysis_history (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
                combination TEXT,
                ai_report TEXT,
                date TIMESTAMP DEFAULT NOW()
            )''')

            c.execute('''CREATE INDEX IF NOT EXISTS idx_results_student_test 
                         ON results(student_id, test_name)''')

        else:
            # --- SQLite Tabloları ---
            c.execute('''CREATE TABLE IF NOT EXISTS students
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT, username TEXT, password TEXT,
                          age INTEGER, gender TEXT, grade INTEGER,
                          login_count INTEGER DEFAULT 0,
                          secret_word TEXT)''')

            try:
                c.execute("ALTER TABLE students ADD COLUMN secret_word TEXT")
            except Exception:
                pass

            try:
                c.execute("ALTER TABLE students ADD COLUMN grade INTEGER")
            except Exception:
                pass

            c.execute('''CREATE TABLE IF NOT EXISTS results
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          student_id INTEGER,
                          test_name TEXT,
                          raw_answers TEXT,
                          scores TEXT,
                          report TEXT,
                          date TIMESTAMP)''')

            c.execute('''CREATE TABLE IF NOT EXISTS analysis_history
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          student_id INTEGER,
                          combination TEXT,
                          ai_report TEXT,
                          date TIMESTAMP)''')

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"init_db hatası: {e}")
    finally:
        conn.close()


# ============================================================
# ÖĞRENCİ KİMLİK / KAYIT İŞLEMLERİ
# ============================================================

def register_student(name, username, password, age, gender, secret_word="", grade=None):
    """Yeni öğrenci kaydeder."""
    init_db()

    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        c.execute(f"SELECT id FROM students WHERE username={ph}", (username,))
        if c.fetchone():
            return False, "Bu e-posta adresi zaten kayıtlı."

        hashed_pw = hash_password(password)
        hashed_secret = hash_password(secret_word) if secret_word else ""
        c.execute(
            f"INSERT INTO students (name, username, password, age, gender, grade, secret_word) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})",
            (name, username, hashed_pw, age, gender, grade, hashed_secret)
        )
        conn.commit()
        return True, "Kayıt Başarılı"

    except Exception as e:
        conn.rollback()
        return False, f"Kayıt sırasında hata: {e}"

    finally:
        conn.close()


def login_student(username, password):
    """Öğrenci girişi doğrular."""
    init_db()

    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        hashed_pw = hash_password(password)

        c.execute(
            f"SELECT id, name, username, password, age, gender, grade, login_count FROM students WHERE username={ph} AND password={ph}",
            (username, hashed_pw)
        )
        user = c.fetchone()

        if user:
            new_count = (user[7] or 0) + 1
            c.execute(f"UPDATE students SET login_count={ph} WHERE id={ph}", (new_count, user[0]))
            conn.commit()
            return True, Student(user, new_count)

        return False, None

    except Exception as e:
        conn.rollback()
        print(f"Login hatası: {e}")
        return False, None

    finally:
        conn.close()


def reset_student_password(username, secret_word, new_password):
    """Öğrenci şifresini sıfırlar."""
    init_db()

    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        c.execute(f"SELECT id, secret_word FROM students WHERE username={ph}", (username,))
        user_data = c.fetchone()

        if not user_data:
            return False, "Sistemde böyle bir e-posta adresi bulunamadı."

        user_id = user_data[0]
        stored_secret = user_data[1]

        if not stored_secret:
            return False, "Bu hesaba ait kurtarma kelimesi bulunmuyor (Eski kayıt olabilir). Lütfen yeni hesap açın."

        # Hash'li karşılaştırma (yeni kayıtlar)
        hashed_input = hash_password(secret_word.lower().strip())
        if stored_secret == hashed_input:
            pass  # Eşleşti — devam et
        elif stored_secret.lower().strip() == secret_word.lower().strip():
            # Eski kayıt (düz metin) — eşleşti, hash'e yükselt
            c.execute(f"UPDATE students SET secret_word={ph} WHERE id={ph}", (hashed_input, user_id))
        else:
            return False, "Girilen kurtarma kelimesi yanlış!"

        new_hashed_pw = hash_password(new_password)
        c.execute(f"UPDATE students SET password={ph} WHERE id={ph}", (new_hashed_pw, user_id))
        conn.commit()

        return True, "Şifreniz başarıyla yenilendi."

    except Exception as e:
        conn.rollback()
        return False, f"Şifre sıfırlama hatası: {e}"

    finally:
        conn.close()


# ============================================================
# TEST KAYIT İŞLEMLERİ
# ============================================================

def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    """Test sonucunu veritabanına kaydeder. Varsa eski kaydı günceller."""
    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        c.execute(
            f"DELETE FROM results WHERE student_id={ph} AND test_name={ph}",
            (student_id, test_name)
        )

        c.execute(
            f"INSERT INTO results (student_id, test_name, raw_answers, scores, report, date) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})",
            (
                student_id,
                test_name,
                json.dumps(raw_answers, ensure_ascii=False),
                json.dumps(scores, ensure_ascii=False),
                report_text,
                datetime.now()
            )
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Test kayıt hatası: {e}")
        return False

    finally:
        conn.close()


def check_test_completed(student_id, test_name):
    """Öğrencinin belirli bir testi tamamlayıp tamamlamadığını kontrol eder."""
    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        c.execute(
            f"SELECT id FROM results WHERE student_id={ph} AND test_name={ph}",
            (student_id, test_name)
        )
        data = c.fetchone()
        return data is not None
    except Exception:
        return False
    finally:
        conn.close()


# ============================================================
# ÖĞRETMEN VERİ ÇEKME İŞLEMLERİ
# ============================================================

def get_all_students_with_results():
    """Tüm öğrencileri ve test sonuçlarını döndürür."""
    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        c.execute("SELECT id, name, username, password, age, gender, grade, login_count FROM students ORDER BY name")
        students_raw = c.fetchall()

        all_data = []
        for s in students_raw:
            c.execute(
                f"SELECT test_name, scores, raw_answers, date, report FROM results WHERE student_id={ph} ORDER BY date DESC",
                (s[0],)
            )
            tests_raw = c.fetchall()

            tests_list = []
            for t in tests_raw:
                try:
                    score_json = json.loads(t[1]) if t[1] else {}
                except (json.JSONDecodeError, TypeError):
                    score_json = {}

                tests_list.append({
                    "test_name": t[0],
                    "scores": score_json,
                    "raw_answers": t[2],
                    "date": str(t[3]) if t[3] else "",
                    "report": t[4]
                })

            all_data.append({
                "info": StudentInfo(s),
                "tests": tests_list
            })

        return all_data

    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return []

    finally:
        conn.close()


def get_student_analysis_history(student_id):
    """Öğrencinin AI analiz arşivini döndürür."""
    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        c.execute(
            f"SELECT combination, ai_report, date FROM analysis_history WHERE student_id={ph} ORDER BY date DESC",
            (student_id,)
        )
        rows = c.fetchall()

        history = []
        for r in rows:
            history.append({
                "combination": r[0],
                "report": r[1],
                "date": str(r[2]) if r[2] else ""
            })
        return history

    except Exception:
        return []

    finally:
        conn.close()


def save_holistic_analysis(student_id, combination_list, report_text):
    """AI analiz raporunu arşive kaydeder."""
    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)
    comb_str = " + ".join(combination_list)

    try:
        c.execute(
            f"INSERT INTO analysis_history (student_id, combination, ai_report, date) VALUES ({ph}, {ph}, {ph}, {ph})",
            (student_id, comb_str, report_text, datetime.now())
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Analiz kayıt hatası: {e}")

    finally:
        conn.close()


def delete_specific_students(names_list):
    """Belirtilen öğrencilerin tüm verilerini siler."""
    conn, engine = get_connection()
    c = conn.cursor()
    ph = get_placeholder(engine)

    try:
        for name in names_list:
            c.execute(f"SELECT id FROM students WHERE name={ph}", (name,))
            sid = c.fetchone()
            if sid:
                c.execute(f"DELETE FROM analysis_history WHERE student_id={ph}", (sid[0],))
                c.execute(f"DELETE FROM results WHERE student_id={ph}", (sid[0],))
                c.execute(f"DELETE FROM students WHERE id={ph}", (sid[0],))
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Silme hatası: {e}")
        return False

    finally:
        conn.close()


def reset_database():
    """
    Tüm veritabanını sıfırlar.
    PostgreSQL: Tabloları DROP eder ve yeniden oluşturur.
    SQLite: Dosyayı siler ve yeniden oluşturur.
    """
    conn, engine = get_connection()
    c = conn.cursor()

    try:
        if engine == "postgresql":
            c.execute("DROP TABLE IF EXISTS analysis_history CASCADE")
            c.execute("DROP TABLE IF EXISTS results CASCADE")
            c.execute("DROP TABLE IF EXISTS students CASCADE")
            conn.commit()
        else:
            conn.close()
            conn = None
            if os.path.exists(SQLITE_DB_NAME):
                os.remove(SQLITE_DB_NAME)

        init_db()
        return True

    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        print(f"Sıfırlama hatası: {e}")
        return False

    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


def repair_database():
    """
    Veritabanını onarmaya çalışır.
    Eksik tabloları yeniden oluşturur (varsa dokunmaz).
    """
    try:
        init_db()
        return True
    except Exception:
        return False
