import sqlite3
import json
import pandas as pd
from datetime import datetime
import streamlit as st
import os

DB_NAME = "school_data.db"

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
    # Kayıt öncesi DB kontrolü
    init_db()
    
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
    # Giriş öncesi DB kontrolü
    init_db()
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Hata koruması: Tablo yoksa oluştur
    try:
        c.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))

    user = c.fetchone()
    
    if user:
        new_count = user[6] + 1
        c.execute("UPDATE students SET login_count=? WHERE id=?", (new_count, user[0]))
        conn.commit()
        
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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tablo kontrolü
    try:
        c.execute("DELETE FROM results WHERE student_id=? AND test_name=?", (student_id, test_name))
    except sqlite3.OperationalError:
        # Tablo yoksa oluştur ve tekrar dene
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM results WHERE student_id=? AND test_name=?", (student_id, test_name))
    
    c.execute("INSERT INTO results (student_id, test_name, raw_answers, scores, report, date) VALUES (?, ?, ?, ?, ?, ?)",
              (student_id, test_name, str(raw_answers), json.dumps(scores, ensure_ascii=False), report_text, datetime.now()))
    conn.commit()
    conn.close()
    return True

def check_test_completed(student_id, test_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM results WHERE student_id=? AND test_name=?", (student_id, test_name))
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        return False # Tablo yeni oluştuysa test çözülmemiştir
        
    data = c.fetchone()
    conn.close()
    return data is not None

# --- ÖĞRETMEN VERİ ÇEKME İŞLEMLERİ (HATA BURADAYDI - DÜZELTİLDİ) ---
def get_all_students_with_results():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # -----------------------------------------------------------
    # KRİTİK DÜZELTME: Kendi Kendini Onaran Sorgu
    # -----------------------------------------------------------
    try:
        c.execute("SELECT * FROM students")
    except sqlite3.OperationalError:
        # HATA YAKALANDI: "no such table: students"
        # ÇÖZÜM: Veritabanını hemen oluştur ve tekrar dene
        conn.close()
        init_db() 
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM students") # Tekrar sorgula
    # -----------------------------------------------------------

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
        
        # Test sonuçlarını al (Hata olursa tabloyu oluştur)
        try:
            c.execute("SELECT test_name, scores, raw_answers, date, report FROM results WHERE student_id=?", (s[0],))
        except sqlite3.OperationalError:
            init_db()
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
        c.execute("SELECT combination, ai_report, date FROM analysis_history WHERE student_id=? ORDER BY date DESC", (student_id,))
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        return [] # Tablo yoksa geçmiş de yoktur
        
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
        c.execute("INSERT INTO analysis_history (student_id, combination, ai_report, date) VALUES (?, ?, ?, ?)",
                  (student_id, comb_str, report_text, datetime.now()))
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO analysis_history (student_id, combination, ai_report, date) VALUES (?, ?, ?, ?)",
                  (student_id, comb_str, report_text, datetime.now()))
        
    conn.commit()
    conn.close()

def delete_specific_students(names_list):
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
    except:
        pass # Silme hatası önemsiz
    conn.close()
    return True

def reset_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    init_db()
    return True
