#!/usr/bin/env python3
"""
Скрипт для установки зависимостей проекта
"""
import subprocess
import sys

def install_dependencies():
    print("🚀 Установка зависимостей...")
    
    try:
        # Устанавливаем num2words
        print("📦 Устанавливаем num2words...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "num2words==0.5.14"])
        print("✅ num2words установлен успешно!")
        
        # Устанавливаем все зависимости из requirements.txt
        print("📦 Устанавливаем все зависимости из requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Все зависимости установлены!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при установке: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 Установка зависимостей для wholesale trading system...")
    if install_dependencies():
        print("✅ Установка завершена успешно!")
    else:
        print("❌ Установка завершена с ошибками!") 