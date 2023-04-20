import requests, fake_useragent
from bs4 import BeautifulSoup 
import re
import dsmltf

# Делаем запросы с разными User-Agent
user = fake_useragent.UserAgent().random 
# Заголовки
headers = {'User-Agent': user}

# Парсим данные за квартал 
def pars(url):
    request_session = requests.Session() # Создаем сессию 
    request = request_session.get(url, headers=headers)  # Делаем запрос
    soup = BeautifulSoup(request.content, 'lxml') # Парсим
    # Получаем днные 1 - сутки 2 - неделя 3 - месяц 4 - квартал
    data = soup.find_all('li', id = 'textli4') 
    regex = r'<td>(\d+.\d+)<\/td>'
    match = re.findall(regex, str(data))
    return  [float(i) for i in match]

def percent(number, percent):
    return int(round(number * (percent / 100),0))

def percentile(arr, p):
    """
    Вычисляет перцентиль заданного уровня для заданного массива значений.
    :arr: Массив значений.
    :p: Уровень перцентиля.
    :return: Значение перцентиля.
    """
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    # Нахождение индекса элемента, соответствующего перцентилю p.
    # Формула использует длину списка sorted_arr и заданный уровень перцентиля p.
    idx = (p / 100) * (n - 1)
    # Проверка, является ли индекс целым числом.
    if idx.is_integer():
        return sorted_arr[int(idx)]
    
    k = int(idx)
    f = idx - k
    #  Возвращается значение перцентиля, которое вычисляется по формуле 
    # линейной интерполяции между элементами с индексами k и k + 1 в списке sorted_arr.
    return (1 - f) * sorted_arr[k] + f * sorted_arr[k + 1]

if __name__ == '__main__':
    
    url = 'https://cryptocharts.ru/bitcoin/' # Рубль к битку
    data_bit_rub = pars(url) 
   
    #Статистика
    print('Ex_1\n')
    print('Максимальная цена: {:.2f}'.format(max(data_bit_rub))) 
    print('Минимальная цена: {:.2f}'.format(min(data_bit_rub)))
    print('Средняя цена: {:.2f}'.format(dsmltf.mean(data_bit_rub)))
    print('Медиана: {:.2f}'.format(dsmltf.median(data_bit_rub)))
    print('Стандартное отклонение: {:.2f}'.format(dsmltf.standard_deviation(data_bit_rub)))
    print('Размах: {:.2f}'.format(dsmltf.data_range(data_bit_rub)))
    print('Дисперсия: {:.2f}'.format(dsmltf.variance(data_bit_rub)))
    print('Интерквантильный размах: {:.2f}'.format(dsmltf.interquantile_range(data_bit_rub)))
    print('Выбросы: ', dsmltf.interquantile_range(data_bit_rub) < dsmltf.data_range(data_bit_rub))
    
    # Евро к битку
    print('\nEx_2\n')
    url = f'{url[:-1]}-euro/' 
    data_bit_eur = pars(url)
    # Статистика
    print('Корреляция: {:.2f}'.format(dsmltf.correlation(data_bit_rub, data_bit_eur)))

    # Задание 3
    print('\nEx_3\n')
    percent_40 = percent(len(data_bit_rub),40)  # 40% от кол-ва элементов
    data_rub_first = data_bit_rub[:percent_40]  # Берем первые 40% элементов
    data_rub_second = data_bit_rub[percent_40:] # Берем последние 40% элемента

    mid_price_1 = sum(data_rub_first)/len(data_rub_first)
    standart_otkl_1 = dsmltf.standard_deviation(data_rub_first)

    print('Средняя цена 1-ой выборки: {:.2f}'.format(mid_price_1))
    print('Стандартное отклонение 1-ой выборки: {:.2f}'.format(standart_otkl_1))

    z = 1.95  # для 95% доверительного интервала
    value = mid_price_1 + z * standart_otkl_1

    print("Значение, выше которого курс не должен подниматься во второй выборке: {:.2f}".format(value))
    print("Максимальное значение во второй выборке:",max(data_rub_second))
    print("Сбылось ли условие: ", max(data_rub_second) < value)

    mid_price_2 = dsmltf.mean(data_rub_second)
    standart_otkl_2 = dsmltf.standard_deviation(data_rub_second)
    print('\n')
    print('Средняя цена 2-ой выборки: {:.2f}'.format(mid_price_2))
    print('Стандартное отклонение 2-ой выборки: {:.2f}'.format(standart_otkl_2))

    value_2 = mid_price_2 + z * standart_otkl_2
    print("Значение, выше которого курс не должен подниматься в первой выборке: {:.2f}".format(value_2))
    print("Максимальное значение в первой выборке:",max(data_rub_first))
    print("Сбылось ли условие: ", max(data_rub_first) < value_2)
    
    print('\nПосле устранения выбросов')
    # Устраняем выбросы из второй выборки по уровню 75%
    data_75 = percentile(data_rub_second,75)  
    filtered_rub_second = [ data for data in data_rub_second if data <= data_75]

    filter_mid_price_2 = sum(filtered_rub_second)/len(filtered_rub_second)
    filter_standart_otkl_2 = dsmltf.standard_deviation(filtered_rub_second)
    print('Средняя цена 2-ой выборки: {:.2f}'.format(filter_mid_price_2))
    print('Стандартное отклонение 2-ой выборки: {:.2f}'.format(filter_standart_otkl_2))
    
    filter_value = filter_mid_price_2 + z * filter_standart_otkl_2
    print("Значение, выше которого курс не должен подниматься в первой выборке: {:.2f}".format(filter_value))
    print("Максимальное значение в 2-ой выборке: {:.2f}".format(max(filtered_rub_second)))
    print("Сбылось ли условие: ", max(filtered_rub_second) < filter_value)

    print('\nПосле устранения выбросов 1-ой')
    # Устраняем выбросы из второй выборки по уровню 75%
    data_75 = percentile(data_rub_first,75)  
    filtered_rub_first = [ data for data in data_rub_first if data <= data_75]

    filter_mid_price_1 = sum(filtered_rub_first)/len(filtered_rub_first)
    filter_standart_otkl_1 = dsmltf.standard_deviation(filtered_rub_first)
    print('Средняя цена 1-ой выборки: {:.2f}'.format(filter_mid_price_1))
    print('Стандартное отклонение 1-ой выборки: {:.2f}'.format(filter_standart_otkl_1))
    
    filter_value = filter_mid_price_1 + z * filter_standart_otkl_1
    print("Значение, выше которого курс не должен подниматься в первой выборке: {:.2f}".format(filter_value))
    print("Максимальное значение в 1-ой выборке: {:.2f}".format(max(filtered_rub_first)))
    print("Сбылось ли условие: ", max(filtered_rub_first) < filter_value)