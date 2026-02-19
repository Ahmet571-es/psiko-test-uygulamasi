import sqlite3
import json
import hashlib
import pandas as pd
from datetime import datetime
import streamlit as st
import os

DB_NAME = "school_data.db"


# ============================================================
# DÜZELTME: class tanımları döngü/fonksiyon dışına taşındı.
# Eskiden her login/her öğrenci döngüsünde yeniden yaratılıyordu.
# ============================================================

class Student:
    """login_student fonksiyonunun döndürdüğü öğrenci nesnesi."""
    def __init__(self, data, login_count):
        self.id         = data[0]
        self.name       = data[1]
        self.username   = data[2]
        self.password   = data[3]
        self.age        = data[4]
        self.gender     = data[5]
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
        self.login_count = data[6]


# ============================================================
# ŞİFRE YARDIMCI FONKSİYONU
# DÜZELTME: Şifreler artık SHA-256 hash olarak saklanıyor.
# ⚠️ ÖNEMLİ: Bu değişiklikten önce kayıtlı tüm öğrenciler
# yeniden kayıt olmalı VEYA DB sıfırlanmalı.
# ============================================================

def hash_password(password: str) -> str:
    """SHA-256 ile şifre hash'ler."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    """Veritabanı tablolarını oluşturur."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Öğrenciler Tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, username TEXT, password TEXT, 
                  age INTEGER, gender TEXT, 
                  login_count INTEGER DEFAULT 0)''')
    
    # 2. Test Sonuçları Tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  student_id INTEGER, 
                  test_name TEXT, 
                  raw_answers TEXT, 
                  scores TEXT, 
                  report TEXT,
                  date TIMESTAMP)''')
    
    # 3. Öğretmen AI Analiz Arşivi Tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS analysis_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  combination TEXT,
                  ai_report TEXT,
                  date TIMESTAMP)''')
    
    conn.commit()
    conn.close()


# --- ÖĞRENCİ İŞLEMLERİ ---

def register_student(name, username, password, age, gender):
    """
    Yeni öğrenci kaydeder.
    DÜZELTME: Şifre SHA-256 hash olarak saklanıyor.
    """
    init_db()
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Bu kullanıcı adı zaten alınmış."
    
    # DÜZELTME: Şifre hash'lenerek saklanıyor
    hashed_pw = hash_password(password)
    c.execute(
        "INSERT INTO students (name, username, password, age, gender) VALUES (?, ?, ?, ?, ?)",
        (name, username, hashed_pw, age, gender)
    )
    conn.commit()
    conn.close()
    return True, "Kayıt Başarılı"


def login_student(username, password):
    """
    Öğrenci girişi doğrular.
    DÜZELTME: Şifre karşılaştırması hash üzerinden yapılıyor.
    DÜZELTME: except bloğunda c = conn.cursor() eksikti, eklendi.
    """
    init_db()
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    hashed_pw = hash_password(password)
    
    try:
        c.execute(
            "SELECT * FROM students WHERE username=? AND password=?",
            (username, hashed_pw)
        )
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()  # DÜZELTME: Yeni conn için cursor yenileniyor
        c.execute(
            "SELECT * FROM students WHERE username=? AND password=?",
            (username, hashed_pw)
        )

    user = c.fetchone()
    
    if user:
        new_count = user[6] + 1
        c.execute("UPDATE students SET login_count=? WHERE id=?", (new_count, user[0]))
        conn.commit()
        conn.close()
        return True, Student(user, new_count)
    
    conn.close()
    return False, None


# --- TEST KAYIT İŞLEMLERİ ---

def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    """
    Test sonucunu veritabanına kaydeder.
    DÜZELTME: raw_answers artık str() değil json.dumps() ile kaydediliyor.
    str() Python repr formatı üretir ({1: 'a'}) ve geçerli JSON değildir.
    json.dumps() geçerli JSON üretir ({"1": "a"}) ve geri okunabilir.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    try:
        c.execute(
            "DELETE FROM results WHERE student_id=? AND test_name=?",
            (student_id, test_name)
        )
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "DELETE FROM results WHERE student_id=? AND test_name=?",
            (student_id, test_name)
        )
    
    # DÜZELTME: str(raw_answers) → json.dumps(raw_answers)
    c.execute(
        "INSERT INTO results (student_id, test_name, raw_answers, scores, report, date) VALUES (?, ?, ?, ?, ?, ?)",
        (
            student_id,
            test_name,
            json.dumps(raw_answers, ensure_ascii=False),   # DÜZELTME
            json.dumps(scores, ensure_ascii=False),
            report_text,
            datetime.now()
        )
    )
    conn.commit()
    conn.close()
    return True


def check_test_completed(student_id, test_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "SELECT id FROM results WHERE student_id=? AND test_name=?",
            (student_id, test_name)
        )
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        return False
        
    data = c.fetchone()
    conn.close()
    return data is not None


# --- ÖĞRETMEN VERİ ÇEKME İŞLEMLERİ ---

def get_all_students_with_results():
    """
    Tüm öğrencileri ve test sonuçlarını döndürür.
    DÜZELTME: StudentInfo class'ı artık döngü dışında tanımlı.
    DÜZELTME: Bare except → spesifik exception türleri kullanılıyor.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM students")
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM students")

    students_raw = c.fetchall()
    all_data = []
    
    for s in students_raw:
        # DÜZELTME: StudentInfo artık döngü dışında tanımlı (modül seviyesinde)
        
        try:
            c.execute(
                "SELECT test_name, scores, raw_answers, date, report FROM results WHERE student_id=?",
                (s[0],)
            )
        except sqlite3.OperationalError:
            init_db()
            c.execute(
                "SELECT test_name, scores, raw_answers, date, report FROM results WHERE student_id=?",
                (s[0],)
            )
            
        tests_raw = c.fetchall()
        
        tests_list = []
        for t in tests_raw:
            try:
                score_json = json.loads(t[1]) if t[1] else {}
            except (json.JSONDecodeError, TypeError) as e:
                # DÜZELTME: Bare except yerine spesifik exception
                score_json = {}
                
            tests_list.append({
                "test_name": t[0],
                "scores": score_json,
                "raw_answers": t[2],
                "date": t[3],
                "report": t[4]
            })
            
        all_data.append({
            "info": StudentInfo(s),
            "tests": tests_list
        })
    
    conn.close()
    return all_data


def get_student_analysis_history(student_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "SELECT combination, ai_report, date FROM analysis_history WHERE student_id=? ORDER BY date DESC",
            (student_id,)
        )
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        return []
        
    rows = c.fetchall()
    conn.close()
    
    history = []
    for r in rows:
        history.append({
            "combination": r[0],
            "report": r[1],
            "date": r[2]
        })
    return history


def save_holistic_analysis(student_id, combination_list, report_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    comb_str = " + ".join(combination_list)
    
    try:
        c.execute(
            "INSERT INTO analysis_history (student_id, combination, ai_report, date) VALUES (?, ?, ?, ?)",
            (student_id, comb_str, report_text, datetime.now())
        )
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO analysis_history (student_id, combination, ai_report, date) VALUES (?, ?, ?, ?)",
            (student_id, comb_str, report_text, datetime.now())
        )
        
    conn.commit()
    conn.close()


def delete_specific_students(names_list):
    """
    Belirtilen öğrencilerin tüm verilerini siler.
    DÜZELTME 1: except + pass → rollback() + connection close + hata dönüşü
    DÜZELTME 2: Kısmi silme durumunda rollback ile veri tutarsızlığı önleniyor.
    Not: İsim bazlı silme korundu (teacher_view.py ile uyum için).
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        for name in names_list:
            c.execute("SELECT id FROM students WHERE name=?", (name,))
            sid = c.fetchone()
            if sid:
                c.execute("DELETE FROM students WHERE id=?", (sid[0],))
                c.execute("DELETE FROM results WHERE student_id=?", (sid[0],))
                c.execute("DELETE FROM analysis_history WHERE student_id=?", (sid[0],))
        conn.commit()
    except Exception as e:
        # DÜZELTME: Kısmi silme geri alınıyor, hata loglanıyor
        conn.rollback()
        conn.close()
        print(f"Silme hatası: {e}")
        return False
    conn.close()
    return True


def reset_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    init_db()
    return True
