import modul 
import requests, fake_useragent
from bs4 import BeautifulSoup 
from matplotlib import pyplot as plt
from dsmltf import *
import re 
from collections import OrderedDict

# Делаем запросы с разными User-Agent
user = fake_useragent.UserAgent().random 
# Заголовки
headers = {'User-Agent': user}

# Парсинг городов 1.5.1
def parsing(url):
    # Создаем сессию для запроса 
    request_session = requests.Session()
    # Делаем запрос
    request = request_session.get(url, headers=headers)
    # Проверяем статус запроса
    if request.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга
        soup = BeautifulSoup(request.content, 'lxml') # lxml - парсер
        # Ищем нужные данные
        class_temp = list(soup.find_all('td', class_='first_in_group'))[::2]
        # Возвращаем данные 
        return [data.text for data in class_temp]

def ex_1(sity, name_sity):
    # Список для хранения данных
    data_temp = []
    # Цикл для парсинга данных
    for i in range(1,13):
        # Ссылка на страницу
        url = f'https://www.gismeteo.ru/diary/{str(sity)}/2022/{str(i)}/'
        # Добавляем данные в список
        data_temp.append(parsing(url))
    # Удаляем пустые строки 
    for data in data_temp:
        for i in data:
            if i == '':
                data.remove(i)
            else:
                data[data.index(i)] = int(i)
    for data in data_temp:
        for i in data:
            data[data.index(i)] = int(i)

    # Считаем стандартное отклонение
    st_dev = [standard_deviation(data) for data in data_temp]
    # Выводим график
    grafik(st_dev, name_sity)


def grafik(st_dev, city):
    # Список месяцев
    month = [1,2,3,4,5,6,7,8,9,10,11,12]
    plt.plot(month,st_dev, color='red', marker='o', linestyle='solid')
    plt.title(f'График стандартного отклонения температуры в {city}')
    plt.show()

# ====================================================================================================

# Парсинг стран 1.5.2 
def pars_2(url):
    # Создаем сессию для запроса
    request_session = requests.Session()
    # Делаем запрос
    request = request_session.get(url, headers=headers)
    # Проверяем статус запроса
    if request.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга
        soup = BeautifulSoup(request.content, 'lxml') # lxml - парсер
        for script in soup(["script", "style"]):  # Удаляем скрипты и стили которые могут мешать парсингу 
            # Удаляем скрипты и стили 
            script.extract() # extract() - удаляет теги 
        
    text_html_clear = soup.get_text() # Получаем текст 
   
    #splitlines - разбивает текст на строки и , strip - удаляет пробелы в начале и конце строки
    lines = (line.strip() for line in text_html_clear.splitlines()) # Разбиваем текст на строки
    # Разбиваем строки на фразы, удаляем пустые строки
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # Разбиваем строки на фразы
    # '\n'.join - объединяет строки в одну строку
    text_html_clear = '\n'.join(chunk for chunk in chunks if chunk) # Собираем фразы в текст 
    
    # re.findall - находит все совпадения по регулярному выражению и возвращает их в виде списка 
    # Обрабатываем полученные данные для подходящего формата, чтобы с ними можно было работать
    text_html_clear = list(re.findall('(\d{4})\s+(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', text_html_clear))
    text_html_clear = [[int(i[0]), int(i[1].replace(',', ''))] for i in text_html_clear]
    text_html_clear = [i[1] for i in text_html_clear if i[0] in [2000, 2010, 2020]]
    return list(OrderedDict.fromkeys(text_html_clear)) # Удаляем дубликаты 

# Генератор для парсинга стран
def generator_url_2(url):
    # Ссылка на страницу 
    return pars_2(f'https://www.worldometers.info/world-population/{url}-population/') 
    
def ex_2():
    # Список стран
    country = ['india', 'china', 'us', 'russia', 'germany'] 
    # Список для хранения данных
    data = [[]]
    # Цикл для парсинга данных
    data.extend(generator_url_2(i) for i in country)
    # Срез данных
    ar_2020 = [i[0] for i in data[1:]] 
    ar_2010 = [i[1] for i in data[1:]] 
    ar_2000 = [i[2] for i in data[1:]]
    country = [i.capitalize() for i in country]
    # Вывод графика на котором будут сразу 3 года
    # plt.bar(country, ar_2020, color='red', label=2020) 
    # plt.bar(country, ar_2010, color='blue', label=2010)
    # plt.bar(country, ar_2000, color='green', label=2000)
    # plt.ylabel('Численность населения')
    # plt.xlabel('Страна')
    # plt.title(f'График численности населения в 2000, 2010, 2020 годах')
    # plt.legend()
    # plt.show()
    # Вызов функции для отображения графиков
    show_graphic(2020, ar_2020, country, 'red')
    show_graphic(2010, ar_2010, country, 'blue')   
    show_graphic(2000, ar_2000, country, 'green')

# Функция для отображения графиков
def show_graphic(year, data ,country, color_graf):
    plt.bar(country, data, color= color_graf, label=year)
    plt.ylabel('Численность населения')
    plt.xlabel('Страна')
    plt.title(f'График численности населения в {year} году')
    plt.legend()
    plt.show()
# ====================================================================================================

# 1.5.3

def ex_3():
    # Списки для хранения данных
    moth = [1,2,3,4,5,6,7,8,9,10,11,12]
    count_inc = [2,14,11,3,1,4,3,21,15,9,4,3]
    middle_ysh = [100,12,15,45,32,21,33,67,87,56,91,115]
    # Цикл для отображения точек на графике
    for moth, count_inc, middle_ysh in zip(moth, count_inc, middle_ysh):
        if middle_ysh <= 23 and middle_ysh >= 0:
            plt.scatter(moth, count_inc, color='blue', marker='.', linestyle='solid', s = 34, alpha=0.5) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 46 and middle_ysh >= 24:
            plt.scatter(moth, count_inc, color='green', marker='.', linestyle='solid', s = 42,alpha=0.6) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 69 and middle_ysh >= 47:
            plt.scatter(moth, count_inc, color='orange', marker='.', linestyle='solid', s = 66,alpha=0.7) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 92 and middle_ysh >= 70:
            plt.scatter(moth, count_inc, color='red', marker='.', linestyle='solid', s = 78,alpha=0.8) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 115 and middle_ysh >= 93:
            plt.scatter(moth, count_inc, color='black', marker='.', linestyle='solid', s=150) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')

    plt.title('Рассеяния количества инцидентов')
    plt.xlabel('Месяц')
    plt.ylabel('Количество инцидентов')
    plt.legend(['93-115', '70-92', '47-69','24-46', '0-23'])
    plt.show()

def ex_3_2(): # Вариант 2 круговая диаграмма
    moth = [1,2,3,4,5,6,7,8,9,10,11,12]
    count_inc = [2,14,11,3,1,4,3,21,15,9,4,3]
    middle_ysh = [100,12,15,45,32,21,33,67,87,56,91,115]
    Employee = ['Малый', 'Ниже среднего', 'Средний','Выше сред.', 'Высокий']
    Count_check = [0,0,0,0,0]
    for moth, count_inc, middle_ysh in zip(moth, count_inc, middle_ysh):
        if middle_ysh <= 23 and middle_ysh >= 0:
            Count_check[0] += 1
        elif middle_ysh <= 46 and middle_ysh >= 24:
            Count_check[1] += 1
        elif middle_ysh <= 69 and middle_ysh >= 47:
            Count_check[2] += 1
        elif middle_ysh <= 92 and middle_ysh >= 70:
            Count_check[3] += 1
        elif middle_ysh <= 115 and middle_ysh >= 93:
            Count_check[4] += 1
    
    # Цвета для круговой диаграммы
    color = ['#FF0000', '#0000FF', '#FFFF00', '#ADFF2F', '#FFA500']
    # Размер круговой диаграммы
    plt.pie(Count_check, colors= color, labels=Employee,autopct='%1.1f%%', pctdistance=0.85)
    # Добавляем круг внутри круговой диаграммы
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    # Получаем текущую фигуру
    fig = plt.gcf()
    
    fig.gca().add_artist(centre_circle)
    
    plt.title('Оценка ущерба за год')
    
    plt.show()



# ====================================================================================================
# 2.1.1
def hprod(u, v):
    result = 0.0
    for i in range(len(u)): # 
        result += u[i] * v[i].conjugate() 
    return result

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
    # Минор 
    def minor(self,i,j):
        return [row[:j] + row[j+1:] for row in (self.matrix[:i]+self.matrix[i+1:])]

    # определитель матрицы 2.1.2
    def det(self): 
        if len(self.matrix) == 2: # если матрица 2х2, то определитель вычисляется по формуле a*d-b*c 
            return self.matrix[0][0]*self.matrix[1][1]-self.matrix[0][1]*self.matrix[1][0] 
        determinant = 0 # инициализация определителя
        for c in range(len(self.matrix)): # перебор столбцов
            # вычисление определителя по формуле: a*det(a11,a12,...,a1n) - b*det(a21,a22,...,a2n) + ... + (-1)^n*a*det(an1,an2,...,ann)
            determinant += ((-1)**c)*self.matrix[0][c]*Matrix(self.minor(0,c)).det()
        return determinant # возвращение определителя 
    
    # ранг матрицы 2.1.3
    def rank(self): 
        matrix = self.matrix # копия матрицы
        rows, cols = len(matrix), len(matrix[0]) # размеры матрицы
        ran_q = rows # ранг матрицы
        for row in range(rows): # перебор строк
            for col in range(cols): # перебор столбцов
                if matrix[row][col] == 0: # если элемент равен нулю, то переходим к следующему
                    continue # переход к следующей итерации цикла
                for i in range(row + 1, rows): # перебор строк
                    if matrix[i][col] != 0: # если элемент не равен нулю, то это строка, которую нужно привести к нулю      
                        factor = matrix[i][col] / matrix[row][col]  # коэффициент, на который нужно умножить строку, чтобы привести ее к нулю
                        for j in range(col, cols): # перебор столбцов
                            matrix[i][j] -= factor * matrix[row][j] # приведение строки к нулю
                break # переход к следующей итерации цикла
            else: # если не было перехода к следующей итерации цикла, то ранг матрицы уменьшается на 1
                ran_q -= 1 # уменьшение ранга матрицы
        return ran_q # возвращение ранга матрицы 

    # решение системы линейных уравнений методом Гаусса 2.1.4
    def gaussian_elimination(self, vector):
        n = len(self.matrix) 
        for i in range(n):
            if self.matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if self.matrix[j][i] != 0:
                        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
                        break
                else:
                    raise ValueError("Matrix is singular")
            pivot = self.matrix[i][i]
            for j in range(i + 1, n):
                factor = self.matrix[j][i] / pivot
                vector[j] -= factor * vector[i]
                for k in range(i, n):
                    self.matrix[j][k] -= factor * self.matrix[i][k]
        solution = [0] * n
        for i in range(n - 1, -1, -1):
            solution[i] = vector[i]
            for j in range(i + 1, n):
                solution[i] -= self.matrix[i][j] * solution[j]
            solution[i] /= self.matrix[i][i]
        return solution

    def __repr__(self):
        return f"{self.matrix}"

   