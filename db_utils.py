import sqlite3
import json
import pandas as pd
from datetime import datetime
import streamlit as st

DB_NAME = "school_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Öğrenciler Tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, username TEXT, password TEXT, 
                  age INTEGER, gender TEXT, 
                  login_count INTEGER DEFAULT 0)''')
    
    # Test Sonuçları Tablosu
    # report sütunu: Python kodunun ürettiği otomatik rapor
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  student_id INTEGER, 
                  test_name TEXT, 
                  raw_answers TEXT, 
                  scores TEXT, 
                  report TEXT,
                  date TIMESTAMP)''')
    
    # Öğretmen AI Analiz Arşivi Tablosu
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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Bu kullanıcı adı zaten alınmış."
    
    c.execute("INSERT INTO students (name, username, password, age, gender) VALUES (?, ?, ?, ?, ?)",
              (name, username, password, age, gender))
    conn.commit()
    conn.close()
    return True, "Kayıt Başarılı"

def login_student(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    
    if user:
        # Giriş sayısını artır
        new_count = user[6] + 1
        c.execute("UPDATE students SET login_count=? WHERE id=?", (new_count, user[0]))
        conn.commit()
        
        # Nesneye çevir
        class Student:
            def __init__(self, data):
                self.id = data[0]
                self.name = data[1]
                self.username = data[2]
                self.password = data[3]
                self.age = data[4]
                self.gender = data[5]
                self.login_count = new_count
        
        conn.close()
        return True, Student(user)
    
    conn.close()
    return False, None

# --- TEST KAYIT İŞLEMLERİ ---
def save_test_result_to_db(student_id, test_name, raw_answers, scores, report_text):
    """
    Öğrencinin bitirdiği testi kaydeder.
    Eğer aynı test daha önce yapılmışsa günceller (veya yeni ekler, tercihe bağlı).
    Burada her seferinde yeni kayıt ekliyoruz ki gelişim görülsün.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Önce aynı testten varsa silelim (yer tasarrufu ve son sonucu tutmak için)
    # İstenirse bu satır silinip tarihçe tutulabilir.
    c.execute("DELETE FROM results WHERE student_id=? AND test_name=?", (student_id, test_name))
    
    c.execute("INSERT INTO results (student_id, test_name, raw_answers, scores, report, date) VALUES (?, ?, ?, ?, ?, ?)",
              (student_id, test_name, str(raw_answers), json.dumps(scores, ensure_ascii=False), report_text, datetime.now()))
    conn.commit()
    conn.close()
    return True

def check_test_completed(student_id, test_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM results WHERE student_id=? AND test_name=?", (student_id, test_name))
    data = c.fetchone()
    conn.close()
    return data is not None

# --- ÖĞRETMEN VERİ ÇEKME İŞLEMLERİ ---
def get_all_students_with_results():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tüm öğrencileri al
    c.execute("SELECT * FROM students")
    students_raw = c.fetchall()
    
    all_data = []
    
    for s in students_raw:
        class StudentInfo:
            def __init__(self, data):
                self.id = data[0]
                self.name = data[1]
                self.username = data[2]
                self.password = data[3]
                self.age = data[4]
                self.gender = data[5]
                self.login_count = data[6]
        
        # Bu öğrencinin testlerini al
        c.execute("SELECT test_name, scores, raw_answers, date, report FROM results WHERE student_id=?", (s[0],))
        tests_raw = c.fetchall()
        
        tests_list = []
        for t in tests_raw:
            try:
                score_json = json.loads(t[1]) if t[1] else {}
            except:
                score_json = {}
                
            tests_list.append({
                "test_name": t[0],
                "scores": score_json,
                "raw_answers": t[2],
                "date": t[3],
                "report": t[4] # Rapor metnini de listeye ekledik
            })
            
        all_data.append({
            "info": StudentInfo(s),
            "tests": tests_list
        })
    
    conn.close()
    return all_data

def get_student_analysis_history(student_id):
    """Öğretmenin yaptığı AI analizlerini getirir."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT combination, ai_report, date FROM analysis_history WHERE student_id=? ORDER BY date DESC", (student_id,))
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
    """Öğretmenin yaptığı yeni AI analizini kaydeder."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    comb_str = " + ".join(combination_list)
    
    c.execute("INSERT INTO analysis_history (student_id, combination, ai_report, date) VALUES (?, ?, ?, ?)",
              (student_id, comb_str, report_text, datetime.now()))
    conn.commit()
    conn.close()

def delete_specific_students(names_list):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for name in names_list:
        # ID'yi bul
        c.execute("SELECT id FROM students WHERE name=?", (name,))
        sid = c.fetchone()
        if sid:
            # Öğrenciyi sil
            c.execute("DELETE FROM students WHERE id=?", (sid[0],))
            # Testlerini sil
            c.execute("DELETE FROM results WHERE student_id=?", (sid[0],))
            # Analizlerini sil
            c.execute("DELETE FROM analysis_history WHERE student_id=?", (sid[0],))
    conn.commit()
    conn.close()
    return True

def reset_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS students")
    c.execute("DROP TABLE IF EXISTS results")
    c.execute("DROP TABLE IF EXISTS analysis_history")
    conn.commit()
    conn.close()
    init_db()
    return True
