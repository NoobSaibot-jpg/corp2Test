#!/usr/bin/env python3
"""
Миграция для добавления колонки ЕДРПО в таблицу customer
"""
import sqlite3
import os

def migrate():
    # Путь к базе данных
    db_path = 'instance/app.db'
    
    if not os.path.exists(db_path):
        print(f"База данных не найдена: {db_path}")
        return
    
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем, существует ли уже колонка edrpou
        cursor.execute("PRAGMA table_info(customer)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'edrpou' not in columns:
            print("Добавляем колонку 'edrpou' в таблицу 'customer'...")
            cursor.execute("ALTER TABLE customer ADD COLUMN edrpou TEXT")
            conn.commit()
            print("✅ Колонка 'edrpou' успешно добавлена!")
        else:
            print("✅ Колонка 'edrpou' уже существует в таблице 'customer'")
        
        # Показываем структуру таблицы
        print("\nСтруктура таблицы 'customer':")
        cursor.execute("PRAGMA table_info(customer)")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка при миграции: {e}")
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Запуск миграции для добавления колонки ЕДРПО...")
    migrate()
    print("✅ Миграция завершена!") 