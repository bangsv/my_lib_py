from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter
import random
import time
import re
import math 

# Функции с названием ex релаизуют задания.
# Функции с иным названием реализуют вспомогательные функции для решения задач
# они находятся над функциями ex

def ex_1(): # Задание 1  ✓
    N = (bin(int(input('Введите число:')))[-3:]).count('0') == 3  # Вводим число превращаем в bin и считаем кол-во нулей
    print('Yes' if N else 'No') # Выводим ответ 

def ex_2(number):  # Задание 2  ✓
    if bin(number)[-3:].count('0') == 3: # Проверяем кол-во нулей в бинарном представлении числа
        return 8 # Возвращаем ответ 
    elif bin(number)[-5:].count('00000') == 5: # Проверяем кол-во нулей в бинарном представлении числа
        return 32 # Возвращаем ответ
    elif bin(number)[-4:].count('0000') == 4:
        return 16
    elif bin(number)[-2:].count('00') == 2: 
        return 4 
    elif bin(number)[:-1].count('0') == 0:
        return 2 
    else:
        return 0

def ex_3(): # Задание 3  ✓
    try:
        a = int(input()) # Вводим число 
    except ValueError:  # Проверяем на ошибку 
        return print('Неверный ввод') 
    except ZeroDivisionError: 
        return print('Введенем ноль')
    finally: 
        if isinstance(a , int) and len(str(a) and abs(a)) == 10:
            return print("Answer: ", ex_2(a))
        else:
            return print('Неверный ввод')


def ex_4(): # Задание 4  ✓
    numbers = [[1, 2,4j], [5.0, 7j, 8.0], [9j, 11j, 12]] # Задаем массив
    # Первый цикл для перебора подсписков, во втором цикле перебор элементов подсписка и проверка на тип из numbers в sublist, sublist из в x и проверям тип
    complex_numbers = [x for sublist in numbers for x in sublist if type(x) == complex] 
    # Переводим в кортеж  и Возвращаем кортеж           
    return  tuple(complex_numbers)                                   

def fibonacci_sequence(n): # Функция для вычисления чисел Фибоначчи 
    if n == 0:  # Проверяем на 0
        return []
    elif n == 1:  # Проверяем на 1
        return [0]
    elif n == 2:  # Проверяем на 2
        return [0,1] 
    else: 
        array_ret = [0,1]  # Создаем пустой массив 
        array_ret.extend(array_ret[i-1] + array_ret[i-2] for i in range(2,n)) # Добавляем в массив числа Фибоначчи
    return array_ret  # Возвращаем массив 

def summ_fib(number):  # Функция для вычисления суммы чисел Фибоначчи
    return [sum(fibonacci_sequence(x)) for x in range (1, number)] # Возвращаем массив с суммами чисел Фибоначчи

def number_inter(pos): # Функция для вычисления кол-ва цифр в числе Фибоначчи
    return len(str(summ_fib(pos+1)[-1])) # Возвращаем кол-во цифр в числе Фибоначчи 


def ex_5():  # Задание 5  ✓ 
    number = int(input('Введите номер элемента:')) # Вводим номер элемента
    return number_inter(number)  # Возвращаем кол-во цифр в числе Фибоначчи 

def fn(x): # Функция для вычисления значения функции 
        return round(math.sin(x)) # Возвращаем значение функции


def ex_6(): # Задание 6  ✓ 
    print("Введите нижний конец интервала") 
    min_int = float(input()) # Вводим верхний конец интервала
    print("Введите верхний конец интервала") 
    max_int = float(input()) # Вводим верхний конец интервала

    for i in range(int(min_int), int(max_int)): # Цикл для вычисления нулей функции
        if fn(i) == 0: # Проверяем равна ли функция 0 в точке x = gran
            print("Функция равна 0 в точке x = ", i) # Выводим ответ
   
    return 0

def ex_7(): # Задание 7 ✓ 
    text = "Петя пил воду воду видя водоем и рыбу" # Начальный текст
    print("Заданный текст:\n", text, "\n")  # Выводим текст
    words = text.split() # Разбиваем текст на слова 
    # Выбираем слова начинающиеся с буквы в из words в word и проверяем на условие, если условие верно, то добавляем в массив words_starting_with_v
    words_starting_with_v = [word for word in words if word[0].lower() == 'в'] 
    words_starting_with_v.sort() # Сортируем массив 
    return set(words_starting_with_v) # Возвращаем массив 

def scraping(url): # Функция для парсинга сайта 
    html = urlopen(url).read() # Читаем сайт
    soup = BeautifulSoup(html, features="html.parser")  # Парсим сайт при помощи модуля BeautifulSoup 
    # soup(["script", "style"]) - находим все скрипты и стили на сайте 
    for script in soup(["script", "style"]):  # Удаляем скрипты и стили которые могут мешать парсингу 
        script.extract()   

    text = soup.get_text() # Получаем текст 
   
    #splitlines - разбивает текст на строки и , strip - удаляет пробелы в начале и конце строки
    lines = (line.strip() for line in text.splitlines()) # Разбиваем текст на строки
    # Разбиваем строки на фразы, удаляем пустые строки
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # Разбиваем строки на фразы
    # '\n'.join - объединяет строки в одну строку
    text = '\n'.join(chunk for chunk in chunks if chunk) # Собираем фразы в текст 
    return text  # Возвращаем текст 


def ex_8():  # Задание 8  ✓
    url = "https://habr.com/ru/post/335994/" # Задаем сайт 
    text = Counter(scraping(url).split()) # Подсчитываем кол-во слов в тексте
    print("Кол-во слов:\n", text, "\nСайт: ", url, ) # Выводим кол-во слов и сайт 

def ret_time_base(numbers):
    start = time.time() # Засекаем время
    result = [] # Создаем пустой массив
    for _ in range(10): # Цикл для выбора 10 случайных чисел
        index = random.randint(0, len(numbers) - 1) # Выбираем случайный индекс
        result.append(list(numbers)[index]) # Добавляем в массив число по индексу
    end = time.time() # Засекаем время 
    return  end - start # Выводим время

def ret_time_with_choice(numbers):
    start = time.time() # Засекаем время 
    result = [random.choice(list(numbers)) for _ in range(10)] # Выбираем 10 случайных чисел
    end = time.time() # Засекаем время 
    return end - start # Выводим время 

def ret_time_with_sample(numbers):
    start = time.time() # Засекаем время 
    result = random.sample(numbers, 10) # Выбираем 10 случайных чисел
    end = time.time() # Засекаем время
    return end - start # Выводим время 

def ex_9(): # Задание 9 
    numbers = set(random.randint(1, 10000) for _ in range(10000)) # Генерируем 10000 чисел от 1 до 10000

    start = time.time() # Засекаем время
    result = [] # Создаем пустой массив
    for _ in range(10): # Цикл для выбора 10 случайных чисел
        index = random.randint(0, len(numbers) - 1) # Выбираем случайный индекс
        result.append(list(numbers)[index]) # Добавляем в массив число по индексу
    end = time.time() # Засекаем время 
    print("Not return: ", end - start) # Выводим время
    print("Return: ", ret_time_base(numbers)) # Выводим время 
    
    start = time.time() # Засекаем время 
    result = random.sample(numbers, 10) # Выбираем 10 случайных чисел
    end = time.time() # Засекаем время
    print("Random.sample NOT return: ", end - start) # Выводим время 
    print("Random.sample return: ", ret_time_with_sample(numbers)) # Выводим время 

    start = time.time() # Засекаем время 
    result = [random.choice(list(numbers)) for _ in range(10)] # Выбираем 10 случайных чисел
    end = time.time() # Засекаем время 
    print("Random.choice NOT return:", end - start) # Выводим время 
    print("Random.choice return:", ret_time_with_choice(numbers)) # Выводим время

def regx(text): # Функция для поиска слова в тексте 
    text = re.findall(r'[\w]?право[\w]+', text)
    print(text) # Выводим текст
    return len(text) # Возвращаем кол-во слова 

def ex_10(): # Задание 10 
    url = "https://www.novopashina.ru/law/gk1.shtml" # Задаем сайт 
    text = str(scraping(url)) # Парсим сайт и разбиваем текст на слова
    return print("Кол-во слова 'право': ", regx(text), 
        "\nСайт: ", url) # Выводим кол-во слова и сайт 

def ex_11(): # ✓ 
    class Frac: # Создаем класс Frac, который будет представлять дробь
        def __init__(self, num, den): # Инициализируем дробь 
            self.num = num # Числитель
            self.den = den # Знаменатель 

        def __add__(self, other): # Переопределяем оператор сложения 
            return Frac(self.num * other.den + self.den * other.num, self.den * other.den) 

        def __mul__(self, other): # Переопределяем оператор умножения
            return Frac(self.num * other.num, self.den * other.den) 

        def __repr__(self): # Переопределяем метод __repr__
            return f"{self.num}/{self.den}"

        def __del__(self): # Переопределяем метод __del__ 
            print("Clearing memory... ") 
        
        def __truediv__ (self, other):
            return Frac(self.num * other.den, self.den * other.num)

    a = Frac(1, 2) # Создаем дробь 
    b = Frac(1, 2) # Создаем дробь 
    res_add = a + b  # Складываем дроби 
    res_mul = a * b  # Умножаем дроби 
    print(res_add, res_mul) # Выводим результаты 
    print(a / b) # Деление дробей
        


def help(): # Функция для вывода справки 
    print("============================================================\n\
        1) Напишите, не используя арифметические операции,\nкод из двух-трех строк, выдающий ответ «да»,\
        если введенное 10-значное натуральное число делится на 8.\
        \n============================================================\n\
        2) Напишите модуль для нахождения НОД числа 8 и заданного 10-значного\
        \nчисла, не используя арифметические операции, но с использованием функций\
        пользователя.\
        \n============================================================\n\
        3) Допишите модуль из упражнения 2, добавив исключения.\
        \n============================================================\n\
        4) Создайте произвольный двухуровневый список из целых, вещественных и\
        \nкомплексных чисел. Выберите из него только комплексные числа и запишите их в\
        кортеж.\
        \n============================================================\n\
        5) Создайте множество из 100 первых элементов последовательности частичных\n\
        сумм ряда Фибоначчи. Выведите число значащих цифр у элемента\
        последовательности с заданным номером.\
        \n============================================================\n\
        6)Создайте короткий скрипт, находящий все нули заданной алгебраической\
         \n============================================================\n\
        7)Напишите скрипт для выборки из заданного текста всех слов,\nначинающихся\
        на «в», и сортировки их в алфавитном порядке.\
        \n============================================================\n\
        8) Скачайте любую статью (например, с Habr.ru) и сформируйте из нее строку.\n\
        Посчитайте частотности для всех слов, содержащихся в ней.\
        \n============================================================\n\
        9) Создайте множество из случайных натуральных чисел размером в 10000\n\
        элементов. Осуществите из него случайную выборку 10 элементов без возвращения,\n\
        а затем с возвращением, не используя методы sample и choice.\nЗафиксируйте время\
        выполнения.\nСделайте то же самое с использованием указанных методов модуля\
        random и сравните скорости выполнения.\
         \n============================================================\n\
        10) С помощью регулярных выражений определите сколько раз, с учетом\n\
        словообразований, в Гражданском кодексе РФ содержится слово «право».\n\
        \n============================================================\n\
        11) Создайте класс Frac, типичный экземпляр которого является обыкновенной\n\
        дробью. Опишите методы обращения, сложения и умножения.\
        \n============================================================\n")