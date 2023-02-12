import modul 
import requests, fake_useragent
from bs4 import BeautifulSoup 
from matplotlib import pyplot as plt
from dsmltf import *
import re 
from collections import OrderedDict

user = fake_useragent.UserAgent().random 
headers = {'User-Agent': user}

# Парсинг городов 1.5.1
def parsing(url):
    request_session = requests.Session()
    request = request_session.get(url, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')
        class_temp = list(soup.find_all('td', class_='first_in_group'))[::2]
        return [data.text for data in class_temp]


def ex_1(sity, name_sity):
    data_temp = []
    for i in range(1,13):
        url = f'https://www.gismeteo.ru/diary/{str(sity)}/2022/{str(i)}/'
        data_temp.append(parsing(url))

    for data in data_temp:
        for i in data:
            if i == '':
                data.remove(i)
            else:
                data[data.index(i)] = int(i)

    for data in data_temp:
        for i in data:
            data[data.index(i)] = int(i)

    st_dev = [standard_deviation(data) for data in data_temp]

    grafik(st_dev, name_sity)


def grafik(st_dev, city):
    month = [1,2,3,4,5,6,7,8,9,10,11,12]
    plt.plot(month,st_dev, color='red', marker='o', linestyle='solid')
    plt.title(f'График стандартного отклонения температуры в {city}')
    plt.show()

# ====================================================================================================

# Парсинг стран 1.5.2 
def pars_2(url):
    request_session = requests.Session()
    request = request_session.get(url, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')
        for script in soup(["script", "style"]):  # Удаляем скрипты и стили которые могут мешать парсингу 
            script.extract()   
        
    text_html_clear = soup.get_text() # Получаем текст 
   
    #splitlines - разбивает текст на строки и , strip - удаляет пробелы в начале и конце строки
    lines = (line.strip() for line in text_html_clear.splitlines()) # Разбиваем текст на строки
    # Разбиваем строки на фразы, удаляем пустые строки
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # Разбиваем строки на фразы
    # '\n'.join - объединяет строки в одну строку
    text_html_clear = '\n'.join(chunk for chunk in chunks if chunk) # Собираем фразы в текст 
    
    text_html_clear = list(re.findall('(\d{4})\s+(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', text_html_clear))
    text_html_clear = [[int(i[0]), int(i[1].replace(',', ''))] for i in text_html_clear]
    text_html_clear = [i[1] for i in text_html_clear if i[0] in [2000, 2010, 2020]]
    return list(OrderedDict.fromkeys(text_html_clear))

def generator_url_2(url):
    return pars_2(f'https://www.worldometers.info/world-population/{url}-population/') 
    
def ex_2():
    country = ['india', 'china', 'us', 'russia', 'germany'] # Список стран
    data = [[]]
    data.extend(generator_url_2(i) for i in country)
    ar_2020 = [i[0] for i in data[1:]]
    ar_2010 = [i[1] for i in data[1:]]
    ar_2000 = [i[2] for i in data[1:]]
    country = [i.capitalize() for i in country]
    # plt.bar(country, ar_2020, color='red', label=2020) 
    # plt.bar(country, ar_2010, color='blue', label=2010)
    # plt.bar(country, ar_2000, color='green', label=2000)
    # plt.ylabel('Численность населения')
    # plt.xlabel('Страна')
    # plt.title(f'График численности населения в 2000, 2010, 2020 годах')
    # plt.legend()
    # plt.show()
    show_graphic(2020, ar_2020, country, 'red')
    show_graphic(2010, ar_2010, country, 'blue')   
    show_graphic(2000, ar_2000, country, 'green')


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
    moth = [1,2,3,4,5,6,7,8,9,10,11,12]
    count_inc = [2,14,11,3,1,4,3,21,15,9,4,3]
    middle_ysh = [100,12,15,45,32,21,33,67,87,56,91,115]

    for moth, count_inc, middle_ysh in zip(moth, count_inc, middle_ysh):
        if middle_ysh <= 23 and middle_ysh >= 0:
            plt.scatter(moth, count_inc, color='blue', marker='1', linestyle='solid', s = 34, alpha=0.5) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 46 and middle_ysh >= 24:
            plt.scatter(moth, count_inc, color='green', marker='_', linestyle='solid', s = 42,alpha=0.6) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 69 and middle_ysh >= 47:
            plt.scatter(moth, count_inc, color='orange', marker='.', linestyle='solid', s = 66,alpha=0.7) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 92 and middle_ysh >= 70:
            plt.scatter(moth, count_inc, color='red', marker='*', linestyle='solid', s = 78,alpha=0.8) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')
        elif middle_ysh <= 115 and middle_ysh >= 93:
            plt.scatter(moth, count_inc, color='black', marker='+', linestyle='solid', s=150) 
            plt.annotate(middle_ysh, xy = (moth, count_inc), xytext = (-5,5), textcoords='offset points')

    plt.title('Рассеяния количества инцидентов')
    plt.xlabel('Месяц')
    plt.ylabel('Количество инцидентов')
    plt.legend(['93-115', '70-92', '47-69','24-46', '0-23'])
    plt.show()