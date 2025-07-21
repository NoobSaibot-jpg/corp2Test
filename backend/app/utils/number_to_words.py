from num2words import num2words

def number_to_words_ua(number):
    """Переводит число в слова на украинском языке с использованием библиотеки num2words"""
    try:
        # Получаем целую и дробную части
        integer_part = int(number)
        decimal_part = round((number - integer_part) * 100)
        
        # Переводим целую часть
        if integer_part == 0:
            result = "нуль"
        else:
            result = num2words(integer_part, lang='uk')
        
        # Добавляем валюту
        result += " грн"
        
        # Добавляем копейки, если они есть
        if decimal_part > 0:
            result += " " + num2words(decimal_part, lang='uk') + " коп"
        
        return result
        
    except Exception as e:
        # В случае ошибки возвращаем число как есть
        return f"{number:.2f} грн" 